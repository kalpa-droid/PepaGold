#!/usr/bin/env python3
"""
build_blog.py — Generador automático del blog de PepaGold.

Qué hace:
  1. Lee todos los .md de /blog/posts/*.md (ahí los guarda el panel admin Sveltia CMS).
  2. Convierte cada uno a una página HTML de artículo, oculta (sin link desde el
     home), ubicada en {locale}/blog/{slug}/index.html.
  3. Regenera {locale}/blog/index.html con las tarjetas de todos los artículos
     de ese idioma, más chips de categoría para filtrar.
  4. Actualiza sitemap.xml agregando las URLs nuevas (sin duplicar).

Se ejecuta automáticamente en GitHub Actions en cada push que toque
blog/posts/**.md (ver .github/workflows/build-blog.yml). No requiere que
nadie lo corra a mano.
"""

import os
import re
import sys
import glob
import yaml
import markdown
import datetime
from xml.sax.saxutils import escape as xml_escape

SITE_URL = "https://pepagold.blog"
POSTS_DIR = "blog/posts"
SITEMAP_PATH = "sitemap.xml"

# Mismo mapeo de carpetas por idioma que usa compile.py
LOCALE_FOLDERS = {
    "es-ar": "",
    "es-mx": "mx",
    "es-es": "es",
    "en-us": "us",
    "fr-fr": "fr",
    "de-de": "de",
    "it-it": "it",
    "pt-br": "pt",
    "ru-ru": "ru",
    "zh-hans": "zh",
}

HREFLANG_MAP = {
    "es-ar": "es-ar", "es-mx": "es-mx", "es-es": "es-es", "en-us": "en-us",
    "fr-fr": "fr-fr", "de-de": "de-de", "it-it": "it-it", "pt-br": "pt-br",
    "ru-ru": "ru-ru", "zh-hans": "zh-hans",
}

CATEGORY_ORDER = [
    "barrera-cutanea", "sostenibilidad", "rutinas-minimalismo",
    "comparativas-economia", "guias-regionales", "cuidado-producto",
    "testimonios-estilo-vida", "tendencias-skincare",
]

BRAND_HEAD = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | PepaGold Blog</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{cover_image_abs}">
<meta property="og:url" content="{canonical}">
{hreflang_tags}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --color-primary: #D48C90;
    --color-primary-hover: #C97A7E;
    --color-accent: #E29578;
    --color-dark: #2A2523;
    --color-dark-muted: #5A524E;
    --border-color: rgba(212,140,144,0.2);
    --bg-primary: #FFFFFF;
    --bg-secondary: #FAF6F5;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Poppins', sans-serif;
    color: var(--color-dark);
    background: var(--bg-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}
  img {{ max-width: 100%; height: auto; display:block; }}
  a {{ color: var(--color-primary-hover); }}
  .site-header {{
    padding: 20px 24px; border-bottom: 1px solid var(--border-color);
    display:flex; align-items:center; justify-content:space-between;
  }}
  .site-header a.logo {{ font-family: Georgia, 'Times New Roman', serif; font-size:1.3rem; color:var(--color-dark); text-decoration:none; font-weight:600; }}
  .site-header nav a {{ margin-left:20px; font-size:0.9rem; text-decoration:none; color:var(--color-dark-muted); }}
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 40px 24px 80px; }}
  .eyebrow {{ font-size:0.8rem; letter-spacing:.06em; text-transform:uppercase; color:var(--color-accent); font-weight:600; }}
  h1.article-title {{
    font-family: Georgia, 'Times New Roman', serif; font-weight:400;
    font-size: clamp(2rem, 4vw, 2.8rem); line-height:1.2; margin: 10px 0 16px; color: var(--color-dark);
  }}
  .meta-row {{ display:flex; gap:14px; flex-wrap:wrap; color: rgba(42,37,35,0.6); font-size:0.85rem; margin-bottom: 28px; }}
  .cover {{ border-radius: 14px; overflow:hidden; margin-bottom: 32px; box-shadow: 0 15px 40px rgba(212,140,144,0.12); }}
  .article-body h2 {{ font-family: Georgia, 'Times New Roman', serif; font-weight:400; font-size:1.8rem; margin: 40px 0 14px; color: var(--color-dark); }}
  .article-body h3 {{ font-family: Georgia, serif; font-size:1.3rem; margin: 28px 0 10px; color: var(--color-dark); }}
  .article-body p {{ margin-bottom: 18px; color: var(--color-dark-muted); font-size:1.05rem; }}
  .article-body ul, .article-body ol {{ margin: 0 0 18px 22px; color: var(--color-dark-muted); }}
  .article-body li {{ margin-bottom: 8px; }}
  .article-body blockquote {{
    border-left: 3px solid var(--color-primary); padding: 4px 20px; margin: 24px 0;
    background: var(--bg-secondary); border-radius: 0 10px 10px 0; color: var(--color-dark-muted); font-style:italic;
  }}
  .article-body img {{ border-radius: 12px; margin: 24px 0; }}
  .product-cta {{
    margin: 40px 0; padding: 28px; border-radius: 16px; background: var(--bg-secondary);
    border: 1px solid var(--border-color); text-align:center;
  }}
  .product-cta p {{ margin-bottom: 16px; color: var(--color-dark); }}
  .product-cta a.btn {{
    display:inline-block; background: var(--color-primary); color:#fff; text-decoration:none;
    padding: 14px 30px; border-radius: 999px; font-weight:600; font-size:0.95rem;
  }}
  .product-cta a.btn:hover {{ background: var(--color-primary-hover); }}
  .region-tag {{
    display:inline-block; font-size:0.78rem; background: rgba(226,149,120,0.15); color: var(--color-accent);
    padding: 4px 12px; border-radius: 999px; margin-bottom: 12px; font-weight:600;
  }}
  footer.site-footer {{ background: var(--color-dark); color: rgba(255,255,255,0.7); text-align:center; padding: 40px 24px; font-size:0.85rem; margin-top:60px; }}
  footer.site-footer a {{ color: #fff; }}
  .back-link {{ display:inline-block; margin-bottom: 24px; font-size:0.9rem; color: var(--color-dark-muted); text-decoration:none; }}
</style>
{article_schema}
</head>
"""

ARTICLE_TEMPLATE = BRAND_HEAD + """<body>
<header class="site-header">
  <a class="logo" href="{home_url}">PepaGold</a>
  <nav><a href="{blog_index_url}">Blog</a><a href="{home_url}">Producto</a></nav>
</header>
<div class="wrap">
  <a class="back-link" href="{blog_index_url}">&larr; Volver al blog</a>
  {region_tag_html}
  <p class="eyebrow">{category_label}</p>
  <h1 class="article-title">{title}</h1>
  <div class="meta-row"><span>{date_display}</span><span>&middot;</span><span>PepaGold</span></div>
  {cover_html}
  <div class="article-body">
    {body_html}
  </div>
  <div class="product-cta">
    <p><strong>Laska Mini Set</strong> — el set de microfibra que reemplaza discos de algodón, agua micelar y desmaquillante. Solo con agua.</p>
    <a class="btn" href="{home_url}">Conocer el producto &rarr;</a>
  </div>
</div>
<footer class="site-footer">
  <p>&copy; 2025&ndash;2026 PepaGold &middot; Distribuidor independiente autorizado de Greenway Global</p>
</footer>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog | PepaGold</title>
<meta name="description" content="Artículos sobre cuidado de la piel sin químicos, sostenibilidad y skincare consciente.">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{ --color-primary:#D48C90; --color-primary-hover:#C97A7E; --color-accent:#E29578; --color-dark:#2A2523; --color-dark-muted:#5A524E; --border-color:rgba(212,140,144,0.2); --bg-secondary:#FAF6F5; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Poppins', sans-serif; color:var(--color-dark); background:#fff; }}
  .site-header {{ padding: 20px 24px; border-bottom: 1px solid var(--border-color); display:flex; align-items:center; justify-content:space-between; }}
  .site-header a.logo {{ font-family: Georgia, serif; font-size:1.3rem; color:var(--color-dark); text-decoration:none; font-weight:600; }}
  .site-header nav a {{ margin-left:20px; font-size:0.9rem; text-decoration:none; color:var(--color-dark-muted); }}
  .wrap {{ max-width: 1080px; margin:0 auto; padding: 50px 24px 90px; }}
  h1 {{ font-family: Georgia, serif; font-weight:400; font-size: clamp(2rem,4vw,2.8rem); margin-bottom: 10px; }}
  .subtitle {{ color: var(--color-dark-muted); margin-bottom: 34px; max-width: 560px; }}
  .chips {{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom: 36px; }}
  .chips a {{ font-size:0.82rem; padding:7px 16px; border-radius:999px; border:1px solid var(--border-color); color:var(--color-dark-muted); text-decoration:none; }}
  .chips a.active {{ background: var(--color-primary); color:#fff; border-color: var(--color-primary); }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 28px; }}
  .card {{ border:1px solid var(--border-color); border-radius:16px; overflow:hidden; text-decoration:none; color:inherit; box-shadow: 0 4px 12px rgba(42,37,35,0.03); transition: box-shadow .2s; }}
  .card:hover {{ box-shadow: 0 15px 40px rgba(212,140,144,0.15); }}
  .card img {{ width:100%; aspect-ratio: 16/10; object-fit:cover; }}
  .card .card-body {{ padding: 18px; }}
  .card .cat {{ font-size:0.72rem; text-transform:uppercase; letter-spacing:.05em; color:var(--color-accent); font-weight:600; }}
  .card h3 {{ font-family: Georgia, serif; font-weight:400; font-size:1.15rem; margin:8px 0; color:var(--color-dark); }}
  .card p {{ font-size:0.88rem; color:var(--color-dark-muted); }}
  footer.site-footer {{ background: var(--color-dark); color: rgba(255,255,255,0.7); text-align:center; padding: 40px 24px; font-size:0.85rem; }}
</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="{home_url}">PepaGold</a>
  <nav><a href="{home_url}">Producto</a></nav>
</header>
<div class="wrap">
  <h1>Blog PepaGold</h1>
  <p class="subtitle">Ciencia de la piel, sostenibilidad y rutinas conscientes. Sin químicos, sin residuos.</p>
  <div class="chips">{chips_html}</div>
  <div class="grid">{cards_html}</div>
</div>
<footer class="site-footer">
  <p>&copy; 2025&ndash;2026 PepaGold &middot; Distribuidor independiente autorizado de Greenway Global</p>
</footer>
</body>
</html>
"""

CATEGORY_LABELS_DEFAULT = {
    "barrera-cutanea": "Barrera cutánea",
    "sostenibilidad": "Sostenibilidad",
    "rutinas-minimalismo": "Rutinas y minimalismo",
    "comparativas-economia": "Comparativas y economía",
    "guias-regionales": "Guías regionales",
    "cuidado-producto": "Cuidado del producto",
    "testimonios-estilo-vida": "Testimonios y estilo de vida",
    "tendencias-skincare": "Tendencias skincare",
}


def parse_post(path):
    """Separa el frontmatter YAML del cuerpo Markdown de un post."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m:
        raise ValueError(f"{path}: falta el bloque frontmatter '---'")
    meta = yaml.safe_load(m.group(1)) or {}
    body_md = m.group(2)
    meta["_source"] = path
    return meta, body_md


def build_article_schema(meta, canonical, cover_abs):
    faq = meta.get("faq") or []
    blocks = []
    blocks.append({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta["title"],
        "description": meta.get("description", ""),
        "image": [cover_abs] if cover_abs else [],
        "datePublished": str(meta.get("date")),
        "author": {"@type": "Organization", "name": "PepaGold"},
        "publisher": {"@type": "Organization", "name": "PepaGold"},
        "mainEntityOfPage": canonical,
    })
    if faq:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                } for item in faq
            ],
        })
    import json
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
        for b in blocks
    )


def render_article(meta, body_md, hreflang_tags):
    locale = meta["locale"]
    folder = LOCALE_FOLDERS[locale]
    slug = meta["slug"]
    base = f"{folder}/" if folder else ""
    canonical = f"{SITE_URL}/{base}blog/{slug}/"
    home_url = f"/{base}" if folder else "/"
    blog_index_url = f"/{base}blog/"
    cover = meta.get("cover_image", "")
    cover_abs = f"{SITE_URL}{cover}" if cover else ""
    cover_html = f'<div class="cover"><img src="{cover}" alt="{meta["title"]}"></div>' if cover else ""
    region_tag_html = (
        f'<span class="region-tag">{meta["region_label"]}</span><br>'
        if meta.get("region_label") else ""
    )
    body_html = markdown.markdown(body_md, extensions=["extra", "sane_lists"])
    category_label = meta.get("category_label") or CATEGORY_LABELS_DEFAULT.get(meta.get("category"), "")
    date_display = str(meta.get("date"))
    schema = build_article_schema(meta, canonical, cover_abs)

    html = ARTICLE_TEMPLATE.format(
        lang_attr=locale.split("-")[0],
        title=meta["title"],
        description=meta.get("description", ""),
        canonical=canonical,
        cover_image_abs=cover_abs,
        hreflang_tags=hreflang_tags,
        article_schema=schema,
        home_url=home_url,
        blog_index_url=blog_index_url,
        region_tag_html=region_tag_html,
        category_label=category_label,
        date_display=date_display,
        cover_html=cover_html,
        body_html=body_html,
    )
    out_dir = os.path.join(folder, "blog", slug) if folder else os.path.join("blog", slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical


def build_hreflang_tags(concept, posts_by_concept):
    if not concept or concept not in posts_by_concept:
        return ""
    tags = []
    for p in posts_by_concept[concept]:
        loc = p["locale"]
        folder = LOCALE_FOLDERS[loc]
        base = f"{folder}/" if folder else ""
        url = f"{SITE_URL}/{base}blog/{p['slug']}/"
        tags.append(f'<link rel="alternate" hreflang="{HREFLANG_MAP[loc]}" href="{url}" />')
    return "\n".join(tags)


def render_index(locale, posts):
    folder = LOCALE_FOLDERS[locale]
    base = f"{folder}/" if folder else ""
    home_url = f"/{base}" if folder else "/"
    canonical = f"{SITE_URL}/{base}blog/"
    posts_sorted = sorted(posts, key=lambda p: str(p.get("date", "")), reverse=True)
    cats_present = sorted({p.get("category") for p in posts_sorted if p.get("category")})
    chips = ['<a href="#" class="active">Todos</a>']
    for c in cats_present:
        chips.append(f'<a href="#{c}">{CATEGORY_LABELS_DEFAULT.get(c, c)}</a>')
    cards = []
    for p in posts_sorted:
        url = f"/{base}blog/{p['slug']}/"
        cover = p.get("cover_image", "")
        img_tag = f'<img src="{cover}" alt="{p["title"]}">' if cover else ""
        cat_label = CATEGORY_LABELS_DEFAULT.get(p.get("category"), "")
        cards.append(
            f'<a class="card" href="{url}" data-cat="{p.get("category","")}">{img_tag}'
            f'<div class="card-body"><p class="cat">{cat_label}</p>'
            f'<h3>{p["title"]}</h3><p>{p.get("description","")}</p></div></a>'
        )
    html = INDEX_TEMPLATE.format(
        lang_attr=locale.split("-")[0],
        canonical=canonical,
        home_url=home_url,
        chips_html="".join(chips),
        cards_html="".join(cards),
    )
    out_dir = os.path.join(folder, "blog") if folder else "blog"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical


def update_sitemap(new_urls):
    """Agrega URLs nuevas al sitemap.xml existente sin duplicar ni tocar lo demás."""
    if not os.path.exists(SITEMAP_PATH):
        print("sitemap.xml no encontrado, se omite.")
        return
    with open(SITEMAP_PATH, encoding="utf-8") as f:
        content = f.read()
    today = datetime.date.today().isoformat()
    added = 0
    for url in new_urls:
        if f"<loc>{xml_escape(url)}</loc>" in content:
            continue
        block = (
            f'\n  <url>\n    <loc>{xml_escape(url)}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n'
            f'    <changefreq>monthly</changefreq>\n'
            f'    <priority>0.6</priority>\n  </url>\n'
        )
        content = content.replace("</urlset>", block + "</urlset>")
        added += 1
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"sitemap.xml actualizado: {added} URL(s) nueva(s).")


def main():
    md_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
    if not md_files:
        print("No hay posts en blog/posts/. Nada que generar.")
        return

    all_meta = []
    for path in md_files:
        meta, body_md = parse_post(path)
        for required in ("title", "slug", "locale", "date", "category"):
            if required not in meta:
                print(f"ERROR: {path} no tiene el campo obligatorio '{required}'", file=sys.stderr)
                sys.exit(1)
        if meta["locale"] not in LOCALE_FOLDERS:
            print(f"ERROR: {path} tiene locale desconocido '{meta['locale']}'", file=sys.stderr)
            sys.exit(1)
        all_meta.append((meta, body_md))

    # Agrupar por concept para armar los hreflang cruzados entre idiomas
    posts_by_concept = {}
    for meta, _ in all_meta:
        c = meta.get("concept")
        if c:
            posts_by_concept.setdefault(c, []).append(meta)

    new_urls = []
    posts_by_locale = {}
    for meta, body_md in all_meta:
        hreflang_tags = build_hreflang_tags(meta.get("concept"), posts_by_concept)
        canonical = render_article(meta, body_md, hreflang_tags)
        new_urls.append(canonical)
        posts_by_locale.setdefault(meta["locale"], []).append(meta)

    for locale, posts in posts_by_locale.items():
        index_url = render_index(locale, posts)
        new_urls.append(index_url)

    update_sitemap(new_urls)
    print(f"Listo: {len(all_meta)} artículo(s) generado(s) en {len(posts_by_locale)} idioma(s).")


if __name__ == "__main__":
    main()
