#!/usr/bin/env python3
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

# Mismo mapeo de carpetas por idioma
LOCALE_FOLDERS = {
    "es-ar": "", "es-mx": "mx", "es-es": "es", "en-us": "us",
    "fr-fr": "fr", "de-de": "de", "it-it": "it", "pt-br": "pt",
    "ru-ru": "ru", "zh-hans": "zh",
}

HREFLANG_MAP = {
    "es-ar": "es-ar", "es-mx": "es-mx", "es-es": "es-es", "en-us": "en-us",
    "fr-fr": "fr-fr", "de-de": "de-de", "it-it": "it-it", "pt-br": "pt-br",
    "ru-ru": "ru-ru", "zh-hans": "zh-hans",
}

CATEGORY_LABELS_DEFAULT = {
    "barrera-cutanea": "🔬 Ciencia de la Piel",
    "sostenibilidad": "🌱 Sostenibilidad y Ecología",
    "rutinas-minimalismo": "🧘‍♀️ Rutinas y Skinimalismo",
    "comparativas-economia": "⚖️ Comparativas y Economía",
    "guias-regionales": "🏜️ Guías Regionales y Clima",
    "cuidado-producto": "🧼 Uso y Cuidado del Producto",
    "testimonios-estilo-vida": "💬 Testimonios y Estilo de Vida",
    "tendencias-skincare": "📈 Tendencias Globales",
}

def render_media(media_list):
    if not media_list:
        return '<span>[No Media]</span>'
        
    html = '<div class="media-gallery" style="display: flex; gap: 10px; width: 100%; height: 100%;">'
    for item in media_list:
        if isinstance(item, str):
            src = item
        else:
            src = item.get('file', '')
            
        if src.lower().endswith(('.mp4', '.webm')):
            html += f'<video src="{src}" autoplay muted loop playsinline style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;"></video>'
        else:
            html += f'<img src="{src}" style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;" alt="Blog Media">'
    html += '</div>'
    return html

BRAND_HEAD = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | PepaGold Blog</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
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
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.05);
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
  a {{ color: var(--color-primary-hover); text-decoration: none; }}
  
  .site-header {{ padding: 20px 24px; border-bottom: 1px solid var(--border-color); display:flex; align-items:center; justify-content:space-between; }}
  .site-header a.logo {{ font-family: Georgia, 'Times New Roman', serif; font-size:1.3rem; color:var(--color-dark); text-decoration:none; font-weight:600; }}
  .site-header nav a {{ margin-left:20px; font-size:0.9rem; color:var(--color-dark-muted); }}
  
  .wrap {{ max-width: 800px; margin: 0 auto; padding: 40px 24px 80px; }}
  .eyebrow {{ font-size:0.85rem; letter-spacing:.06em; text-transform:uppercase; color:var(--color-accent); font-weight:600; }}
  h1.article-title {{ font-family: Georgia, 'Times New Roman', serif; font-weight:400; font-size: clamp(2rem, 4vw, 2.8rem); line-height:1.2; margin: 10px 0 16px; color: var(--color-dark); }}
  .meta-row {{ display:flex; gap:14px; flex-wrap:wrap; color: rgba(42,37,35,0.6); font-size:0.85rem; margin-bottom: 28px; }}
  
  .hero-image-placeholder {{ width: 100%; min-height: 400px; background: var(--bg-secondary); border-radius: 18px; margin-bottom: 40px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px; box-shadow: var(--shadow-md); }}
  
  .article-body h2 {{ font-family: Georgia, 'Times New Roman', serif; font-weight:400; font-size:1.8rem; margin: 40px 0 14px; color: var(--color-dark); }}
  .article-body h3 {{ font-family: Georgia, serif; font-size:1.3rem; margin: 28px 0 10px; color: var(--color-dark); }}
  .article-body p {{ margin-bottom: 18px; color: var(--color-dark-muted); font-size:1.05rem; }}
  .article-body ul, .article-body ol {{ margin: 0 0 18px 22px; color: var(--color-dark-muted); }}
  .article-body li {{ margin-bottom: 8px; }}
  .article-body blockquote {{ border-left: 3px solid var(--color-primary); padding: 4px 20px; margin: 24px 0; background: var(--bg-secondary); border-radius: 0 10px 10px 0; color: var(--color-dark-muted); font-style:italic; }}
  
  .product-cta {{ margin: 40px 0; padding: 28px; border-radius: 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); text-align:center; }}
  .product-cta p {{ margin-bottom: 16px; color: var(--color-dark); }}
  .product-cta a.btn {{ display:inline-block; background: var(--color-primary); color:#fff; text-decoration:none; padding: 14px 30px; border-radius: 999px; font-weight:600; font-size:0.95rem; }}
  .product-cta a.btn:hover {{ background: var(--color-primary-hover); }}
  
  .region-tag {{ display:inline-block; font-size:0.78rem; background: rgba(226,149,120,0.15); color: var(--color-accent); padding: 4px 12px; border-radius: 999px; margin-bottom: 12px; font-weight:600; }}
  footer.site-footer {{ background: var(--color-dark); color: rgba(255,255,255,0.7); text-align:center; padding: 40px 24px; font-size:0.85rem; margin-top:60px; }}
  
  /* Botones flotantes (Language Selector) */
  .lang-selector-container {{ position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: var(--font-sans); }}
  .lang-selector-btn {{ display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }}
  .lang-selector-btn:hover {{ border-color: var(--color-primary); box-shadow: 0 6px 16px rgba(212, 140, 144, 0.15); transform: translateY(-1px); }}
  .lang-dropdown-menu {{ position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); }}
  .lang-selector-container.is-active .lang-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
  .lang-option {{ padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; }}
  .lang-option:hover {{ background: rgba(212, 140, 144, 0.08); color: var(--color-primary-hover); }}
</style>
{article_schema}
</head>
"""

ARTICLE_TEMPLATE = BRAND_HEAD + """<body>
<header class="site-header">
  <a class="logo" href="{home_url}">PepaGold</a>
  <nav><a href="{blog_index_url}">Blog</a><a href="{home_url}">Producto</a></nav>
</header>

<div class="lang-selector-container">
  <div class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">{lang_upper}</span>
    <span style="font-size: 9px; color: var(--color-primary);">▼</span>
  </div>
  <ul class="lang-dropdown-menu" id="langDropdownMenu">
    <li><a href="/blog/" class="lang-option">🇦🇷 Español (AR)</a></li>
    <li><a href="/mx/blog/" class="lang-option">🇲🇽 Español (MX)</a></li>
    <li><a href="/es/blog/" class="lang-option">🇪🇸 Español (ES)</a></li>
    <li><a href="/us/blog/" class="lang-option">🇺🇸 English</a></li>
  </ul>
</div>

<div class="wrap">
  <a class="back-link" href="{blog_index_url}" style="display:inline-block; margin-bottom:24px; color:var(--color-dark-muted);">&larr; Volver al blog</a><br>
  {region_tag_html}
  <p class="eyebrow">{category_label}</p>
  <h1 class="article-title">{title}</h1>
  <div class="meta-row"><span>{date_display}</span><span>&middot;</span><span>{author}</span></div>
  
  <div class="hero-image-placeholder">
    {media_html}
  </div>
  
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
<script>
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {{
    btn.addEventListener('click', (e) => {{
      e.stopPropagation();
      container.classList.toggle('is-active');
    }});
    document.addEventListener('click', () => {{
      container.classList.remove('is-active');
    }});
  }}
</script>
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
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --font-serif: Georgia, "Times New Roman", serif;
    --font-sans: 'Poppins', sans-serif;
    --color-primary: #D48C90;
    --color-primary-hover: #C97A7E;
    --color-accent: #E29578;
    --color-dark: #2A2523;
    --color-dark-muted: #5A524E;
    --border-color: rgba(212, 140, 144, 0.2);
    --bg-primary: #FFFFFF;
    --bg-secondary: #FAF6F5;
    --shadow-sm: 0 4px 15px rgba(42, 37, 35, 0.05);
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.08);
    --shadow-lg: 0 15px 35px rgba(212, 140, 144, 0.15);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; }}
  h1, h2, h3 {{ font-family: var(--font-serif); color: var(--color-dark); line-height: 1.2; margin-bottom: 20px; }}
  a {{ text-decoration: none; }}

  .site-header {{ padding: 20px 24px; border-bottom: 1px solid var(--border-color); display:flex; align-items:center; justify-content:space-between; }}
  .site-header a.logo {{ font-family: Georgia, serif; font-size:1.3rem; color:var(--color-dark); text-decoration:none; font-weight:600; }}
  .site-header nav a {{ margin-left:20px; font-size:0.9rem; text-decoration:none; color:var(--color-dark-muted); }}

  .blog-header {{ text-align: center; padding: 80px 20px 40px; background: var(--bg-secondary); }}
  .blog-header h1 {{ font-size: 2.8rem; margin-bottom: 10px; }}
  .blog-header p {{ font-size: 1.1rem; max-width: 600px; margin: 0 auto; color: var(--color-dark-muted); }}

  .chips {{ display:flex; gap:10px; flex-wrap:wrap; justify-content: center; margin: -20px auto 40px; max-width: 1000px; padding: 0 20px; }}
  .chips a {{ font-size:0.82rem; padding:7px 16px; border-radius:999px; border:1px solid var(--border-color); color:var(--color-dark-muted); background: var(--bg-primary); text-decoration:none; transition: all 0.2s; }}
  .chips a.active {{ background: var(--color-primary); color:#fff; border-color: var(--color-primary); }}
  .chips a:hover:not(.active) {{ border-color: var(--color-primary); }}

  .pain-agitation-section {{ background: var(--bg-primary); padding: 40px 20px 70px; text-align: center; position: relative; overflow: hidden; }}
  .interactive-pain {{ max-width: 1000px; margin: 0 auto; display: flex; flex-direction: column; gap: 80px; position: relative; z-index: 2; }}
  .pain-card-v2 {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 50px; align-items: center; text-align: left; }}
  .pain-card-v2:nth-child(even) {{ direction: rtl; }}
  .pain-card-v2:nth-child(even) > * {{ direction: ltr; }}

  .card-video {{ width: 100%; max-width: 400px; margin: 0 auto; aspect-ratio: 1 / 1; border-radius: 16px; border: 1px dashed var(--color-primary); box-shadow: var(--shadow-sm); overflow: hidden; position: relative; background-color: var(--bg-secondary); transition: box-shadow 0.4s ease, transform 0.4s ease; display: flex; align-items: center; justify-content: center; padding: 10px; }}
  .card-video:hover {{ box-shadow: var(--shadow-lg); transform: translateY(-5px); }}

  .text-content {{ display: flex; flex-direction: column; gap: 12px; }}
  .accent-subtitle {{ color: var(--color-accent); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; display: flex; align-items: center; gap: 8px; }}
  .problem-title {{ font-family: var(--font-serif); font-size: 2.2rem; line-height: 1.2; color: var(--color-dark); margin: 0; }}
  .problem-description {{ font-family: var(--font-sans); font-size: 1.1rem; line-height: 1.7; color: var(--color-dark-muted); font-weight: 300; margin: 0; }}

  .read-btn {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 15px; font-weight: 600; color: var(--color-primary); font-size: 1.05rem; transition: all 0.3s ease; align-self: flex-start; }}
  .read-btn::after {{ content: '→'; transition: transform 0.3s ease; }}
  .read-btn:hover {{ color: var(--color-primary-hover); }}
  .read-btn:hover::after {{ transform: translateX(5px); }}
  
  footer.site-footer {{ background: var(--color-dark); color: rgba(255,255,255,0.7); text-align:center; padding: 40px 24px; font-size:0.85rem; }}
  
  /* Lang selector */
  .lang-selector-container {{ position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: var(--font-sans); }}
  .lang-selector-btn {{ display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }}
  .lang-dropdown-menu {{ position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s ease; }}
  .lang-selector-container.is-active .lang-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
  .lang-option {{ padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; }}
  
  @media (max-width: 768px) {{
    .pain-card-v2 {{ grid-template-columns: 1fr; gap: 30px; }}
    .pain-card-v2:nth-child(even) {{ direction: ltr; }}
    .problem-title {{ font-size: 1.8rem; }}
  }}
</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="{home_url}">PepaGold</a>
  <nav><a href="{home_url}">Producto</a></nav>
</header>

<div class="lang-selector-container">
  <div class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">{lang_upper}</span>
    <span style="font-size: 9px; color: var(--color-primary);">▼</span>
  </div>
  <ul class="lang-dropdown-menu" id="langDropdownMenu">
    <li><a href="/blog/" class="lang-option">🇦🇷 Español (AR)</a></li>
    <li><a href="/mx/blog/" class="lang-option">🇲🇽 Español (MX)</a></li>
    <li><a href="/es/blog/" class="lang-option">🇪🇸 Español (ES)</a></li>
    <li><a href="/us/blog/" class="lang-option">🇺🇸 English</a></li>
  </ul>
</div>

<header class="blog-header">
    <h1>Blog PepaGold</h1>
    <p>Ciencia de la piel, sostenibilidad y rutinas conscientes. Sin químicos, sin residuos.</p>
</header>
<div class="chips">{chips_html}</div>
<section class="pain-agitation-section">
  <div class="interactive-pain">
    {cards_html}
  </div>
</section>
<footer class="site-footer">
  <p>&copy; 2025&ndash;2026 PepaGold &middot; Distribuidor independiente autorizado de Greenway Global</p>
</footer>
<script>
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {{
    btn.addEventListener('click', (e) => {{
      e.stopPropagation();
      container.classList.toggle('is-active');
    }});
    document.addEventListener('click', () => {{
      container.classList.remove('is-active');
    }});
  }}
</script>
</body>
</html>
"""

def parse_post(path):
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
        "headline": meta.get("title", ""),
        "description": meta.get("description", ""),
        "image": [cover_abs] if cover_abs else [],
        "datePublished": str(meta.get("date", "")),
        "author": {"@type": "Organization", "name": meta.get("author", "PepaGold")},
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
    
    media = meta.get("media", [])
    if not media and meta.get("cover_image"):
        media = [meta.get("cover_image")]
        
    cover_abs = f"{SITE_URL}{media[0]}" if media and isinstance(media[0], str) else ""
    media_html = render_media(media)
    
    region_tag_html = f'<span class="region-tag">{meta["region_label"]}</span><br>' if meta.get("region_label") else ""
    body_html = markdown.markdown(body_md, extensions=["extra", "sane_lists"])
    category_label = meta.get("category_label") or CATEGORY_LABELS_DEFAULT.get(meta.get("category"), "")
    date_display = str(meta.get("date", ""))
    schema = build_article_schema(meta, canonical, cover_abs)

    html = ARTICLE_TEMPLATE.format(
        lang_attr=locale.split("-")[0],
        lang_upper=locale.split("-")[0].upper(),
        title=meta.get("title", ""),
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
        author=meta.get("author", "PepaGold"),
        media_html=media_html,
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
        media = p.get("media", [])
        if not media and p.get("cover_image"):
            media = [p.get("cover_image")]
            
        media_html = render_media(media)
        cat_label = CATEGORY_LABELS_DEFAULT.get(p.get("category"), "")
        
        card = f"""
    <div class="pain-card-v2" data-cat="{p.get("category","")}">
        <div class="card-video">
            {media_html}
        </div>
        <div class="text-content">
            <span class="accent-subtitle">{cat_label}</span>
            <h3 class="problem-title">{p.get('title', 'Sin Título')}</h3>
            <p class="problem-description">{p.get('description', '')}</p>
            <a href="{url}" class="read-btn">Leer Artículo</a>
        </div>
    </div>
"""
        cards.append(card)
        
    html = INDEX_TEMPLATE.format(
        lang_attr=locale.split("-")[0],
        lang_upper=locale.split("-")[0].upper(),
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
        md_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*/*.md"))) # fallback in case they are nested
        if not md_files:
            print("No hay posts en blog/posts/. Nada que generar.")
            return

    all_meta = []
    for path in md_files:
        meta, body_md = parse_post(path)
        # For simplicity, don't strictly crash if missing non-critical fields, use safe gets
        if "locale" not in meta:
            print(f"ERROR: {path} no tiene el campo obligatorio 'locale'. Asumiendo es-ar.", file=sys.stderr)
            meta["locale"] = "es-ar"
            
        if meta["locale"] not in LOCALE_FOLDERS:
            print(f"ERROR: {path} tiene locale desconocido '{meta['locale']}'. Asumiendo es-ar.", file=sys.stderr)
            meta["locale"] = "es-ar"
            
        if "slug" not in meta:
            meta["slug"] = os.path.basename(path).replace(".md", "")
            
        all_meta.append((meta, body_md))

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
