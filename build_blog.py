import os
import glob
import yaml
import markdown
import re

base_dir = "."

def extract_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return {}, content

def render_media(media_list):
    if not media_list:
        return '<span>[No Media]</span>'
        
    html = '<div class="media-gallery" style="display: flex; gap: 10px; width: 100%; height: 100%;">'
    for item in media_list:
        if isinstance(item, str):
            src = item
        else:
            # If the user configures list of objects in Sveltia
            src = item.get('file', '')
            
        if src.lower().endswith(('.mp4', '.webm')):
            html += f'<video src="{src}" autoplay muted loop playsinline style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;"></video>'
        else:
            html += f'<img src="{src}" style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;" alt="Blog Media">'
    html += '</div>'
    return html

html_article_template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title} | PepaGold Blog</title>
<meta content="{description}" name="description"/>
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
:root {
    --font-serif: Georgia, "Times New Roman", serif;
    --font-sans: 'Poppins', sans-serif;
    --color-primary: #D48C90;
    --color-primary-hover: #C97A7E;
    --color-accent: #E29578;
    --color-dark: #2A2523;
    --color-dark-muted: #5A524E;
    --bg-primary: #FFFFFF;
    --bg-secondary: #FAF6F5;
    --border-color: rgba(212, 140, 144, 0.2);
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.05);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; padding-top: 50px; }
h1, h2, h3 { font-family: var(--font-serif); color: var(--color-dark); line-height: 1.3; margin-bottom: 20px; }
p { margin-bottom: 20px; }
.container { max-width: 800px; margin: 0 auto; padding: 60px 20px; }
.hero-image-placeholder { width: 100%; min-height: 400px; background: var(--bg-secondary); border-radius: 18px; margin-bottom: 40px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 10px; }
.product-box { background: var(--bg-secondary); padding: 30px; border-radius: 18px; border: 1px solid var(--border-color); margin: 40px 0; text-align: center; box-shadow: var(--shadow-md); }
.product-box img { max-width: 150px; border-radius: 10px; margin-bottom: 20px; }
.btn { display: inline-block; padding: 12px 30px; background: #FFC439; color: var(--color-dark); font-weight: 600; text-decoration: none; border-radius: 30px; margin-top: 15px; transition: transform 0.2s; }
.btn:hover { transform: translateY(-2px); }
.newsletter-box { background: var(--color-primary); color: #fff; padding: 40px; border-radius: 18px; text-align: center; margin: 60px 0; }
.newsletter-box h3 { color: #fff; }
.newsletter-box input { padding: 12px; width: 60%; max-width: 300px; border: none; border-radius: 30px; margin-right: 10px; }
.newsletter-box button { padding: 12px 25px; border: none; background: var(--color-dark); color: #fff; border-radius: 30px; cursor: pointer; font-weight: 600; }
.site-footer { background: var(--color-dark); color: rgba(255, 255, 255, 0.7); padding: 40px 20px; text-align: center; font-size: 0.85rem; margin-top: 80px; }

/* Botones flotantes */
.floating-droplet { position: fixed; top: 65px; left: 20px; width: 56px; height: 56px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.3); border-radius: 0 50% 50% 50%; transform: rotate(45deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(42, 37, 35, 0.08); z-index: 1000; transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.3s ease; }
.floating-droplet:hover { transform: rotate(45deg) scale(1.08); box-shadow: 0 12px 30px rgba(212, 140, 144, 0.25); border-color: var(--color-primary); }
.floating-droplet img { width: 28px; height: 28px; transform: rotate(-45deg); transition: transform 0.3s ease; }
.lang-selector-container { position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: var(--font-sans); }
.lang-selector-btn { display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }
.lang-selector-btn:hover { border-color: var(--color-primary); box-shadow: 0 6px 16px rgba(212, 140, 144, 0.15); transform: translateY(-1px); }
.lang-dropdown-menu { position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); }
.lang-selector-container.is-active .lang-dropdown-menu { opacity: 1; visibility: visible; transform: translateY(0); }
.lang-option { padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; }
.lang-option:hover { background: rgba(212, 140, 144, 0.08); color: var(--color-primary-hover); }
@media (max-width: 600px) {
  .floating-droplet { top: 65px; left: 12px; width: 46px; height: 46px; }
  .floating-droplet img { width: 22px; height: 22px; }
  .lang-selector-container { top: 65px; right: 12px; }
  .lang-selector-btn { padding: 5px 11px; font-size: 12px; }
  .blog-nav-btn-floating { right: 110px !important; }
}
</style>
</head>
<body>

<a href="{blog_url}" class="lang-selector-btn blog-nav-btn-floating" style="position: fixed; top: 65px; right: 130px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">📖</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>

<a href="{home_url}" class="floating-droplet" title="Volver a la Tienda PepaGold">
  <img src="/assets/imagenes/icono.svg" alt="PepaGold Icon" />
</a>

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

<main class="container">
    <h1>{title}</h1>
    
    <div class="hero-image-placeholder">
        {media_html}
    </div>

    <div class="content">
        {content_html}
    </div>
</main>

<footer class="site-footer">
    <p>© 2025–2026 PepaGold. Todos los derechos reservados.</p>
</footer>

<script>
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      container.classList.toggle('is-active');
    });
    document.addEventListener('click', () => {
      container.classList.remove('is-active');
    });
  }
</script>

</body>
</html>
"""

def generate_index(articles, lang):
    index_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PepaGold Blog | Artículos y Guías</title>
<meta content="Explora nuestros artículos sobre cuidado de la barrera cutánea, rutinas minimalistas y ecología." name="description"/>
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
:root {{
    --font-serif: Georgia, "Times New Roman", serif;
    --font-sans: 'Poppins', sans-serif;
    --color-primary: #D48C90;
    --color-primary-hover: #C97A7E;
    --color-accent: #E29578;
    --color-dark: #2A2523;
    --color-dark-muted: #5A524E;
    --bg-primary: #FFFFFF;
    --bg-secondary: #FAF6F5;
    --border-color: rgba(212, 140, 144, 0.2);
    --shadow-sm: 0 4px 15px rgba(42, 37, 35, 0.05);
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.08);
    --shadow-lg: 0 15px 35px rgba(212, 140, 144, 0.15);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; }}
h1, h2, h3 {{ font-family: var(--font-serif); color: var(--color-dark); line-height: 1.2; margin-bottom: 20px; }}
a {{ text-decoration: none; }}

.blog-header {{ text-align: center; padding: 120px 20px 60px; background: var(--bg-secondary); }}
.blog-header h1 {{ font-size: 2.8rem; margin-bottom: 10px; }}
.blog-header p {{ font-size: 1.1rem; max-width: 600px; margin: 0 auto; color: var(--color-dark-muted); }}

.pain-agitation-section {{ background: var(--bg-primary); padding: 90px 20px 70px; text-align: center; position: relative; overflow: hidden; }}
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

/* Floating Buttons */
.floating-droplet {{ position: fixed; top: 65px; left: 20px; width: 56px; height: 56px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.3); border-radius: 0 50% 50% 50%; transform: rotate(45deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(42, 37, 35, 0.08); z-index: 1000; transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.3s ease; }}
.floating-droplet:hover {{ transform: rotate(45deg) scale(1.08); box-shadow: 0 12px 30px rgba(212, 140, 144, 0.25); border-color: var(--color-primary); }}
.floating-droplet img {{ width: 28px; height: 28px; transform: rotate(-45deg); transition: transform 0.3s ease; }}
.lang-selector-container {{ position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: var(--font-sans); }}
.lang-selector-btn {{ display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }}
.lang-selector-btn:hover {{ border-color: var(--color-primary); box-shadow: 0 6px 16px rgba(212, 140, 144, 0.15); transform: translateY(-1px); }}
.lang-dropdown-menu {{ position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); }}
.lang-selector-container.is-active .lang-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
.lang-option {{ padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; }}
.lang-option:hover {{ background: rgba(212, 140, 144, 0.08); color: var(--color-primary-hover); }}
@media (max-width: 768px) {{
  .pain-card-v2 {{ grid-template-columns: 1fr; gap: 30px; }}
  .pain-card-v2:nth-child(even) {{ direction: ltr; }}
  .problem-title {{ font-size: 1.8rem; }}
}}
@media (max-width: 600px) {{
  .floating-droplet {{ top: 65px; left: 12px; width: 46px; height: 46px; }}
  .floating-droplet img {{ width: 22px; height: 22px; }}
  .lang-selector-container {{ top: 65px; right: 12px; }}
  .lang-selector-btn {{ padding: 5px 11px; font-size: 12px; }}
  .blog-nav-btn-floating {{ right: 110px !important; }}
}}
</style>
</head>
<body>

<a href="{f'/blog/' if lang == 'es' else f'/{lang}/blog/'}" class="lang-selector-btn blog-nav-btn-floating" style="position: fixed; top: 65px; right: 130px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">📖</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>

<a href="{f'/' if lang == 'es' else f'/{lang}/'}" class="floating-droplet" title="Volver a la Tienda PepaGold">
  <img src="/assets/imagenes/icono.svg" alt="PepaGold Icon" />
</a>

<div class="lang-selector-container">
  <div class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">{lang.upper()}</span>
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
    <h1>PepaGold Blog</h1>
    <p>Descubre nuestros artículos y guías definitivas.</p>
</header>

<section class="pain-agitation-section">
  <div class="interactive-pain">
"""

    footer = """
  </div>
</section>

<footer style="background: var(--color-dark); color: rgba(255, 255, 255, 0.7); padding: 40px 20px; text-align: center; font-size: 0.85rem;">
    <p>© 2025–2026 PepaGold. Todos los derechos reservados.</p>
</footer>

<script>
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      container.classList.toggle('is-active');
    });
    document.addEventListener('click', () => {
      container.classList.remove('is-active');
    });
  }
</script>
</body>
</html>
"""
    
    out = index_html
    for article in articles:
        media_html = render_media(article.get('media', []))
        
        card = f"""
    <div class="pain-card-v2">
        <div class="card-video">
            {media_html}
        </div>
        <div class="text-content">
            <span class="accent-subtitle">{article.get('category', 'Artículo')}</span>
            <h3 class="problem-title">{article.get('title', 'Sin Título')}</h3>
            <p class="problem-description">{article.get('description', '')}</p>
            <a href="{article['url']}" class="read-btn">Leer Artículo</a>
        </div>
    </div>
"""
        out += card
    out += footer
    
    # Path logic for index
    if lang == 'es':
        index_dir = os.path.join(base_dir, "blog")
    else:
        index_dir = os.path.join(base_dir, f"{lang}/blog")
        
    os.makedirs(index_dir, exist_ok=True)
    with open(os.path.join(index_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
        
    print(f"ZigZag index generated for {lang} at {index_dir}/index.html")

def main():
    # Process all locales dynamically based on folders in blog/posts/
    posts_dir = os.path.join(base_dir, "blog/posts")
    if not os.path.exists(posts_dir):
        return
        
    locales = [d for d in os.listdir(posts_dir) if os.path.isdir(os.path.join(posts_dir, d))]
    
    for lang in locales:
        md_files = glob.glob(os.path.join(posts_dir, f"{lang}/*.md"))
        articles = []
        
        for filepath in md_files:
            filename = os.path.basename(filepath)
            slug = filename.replace(".md", "")
            
            meta, body = extract_frontmatter(filepath)
            content_html = markdown.markdown(body)
            
            # Use 'image' for backwards compatibility, fallback to 'media' list
            media = meta.get("media", [])
            if not media and meta.get("image"):
                media = [meta.get("image")]
                
            # Path logic for individual articles
            if lang == 'es':
                url = f"/blog/{slug}/"
                article_dir = os.path.join(base_dir, f"blog/{slug}")
            else:
                url = f"/{lang}/blog/{slug}/"
                article_dir = os.path.join(base_dir, f"{lang}/blog/{slug}")
                
            os.makedirs(article_dir, exist_ok=True)
            
            title = meta.get("title", slug)
            desc = meta.get("description", "")
            
            media_html = render_media(media)
            
            blog_url = "/blog/" if lang == 'es' else f"/{lang}/blog/"
            home_url = "/" if lang == 'es' else f"/{lang}/"
            
            final_html = html_article_template.replace("{title}", title)\
                .replace("{description}", desc)\
                .replace("{content_html}", content_html)\
                .replace("{media_html}", media_html)\
                .replace("{lang}", lang)\
                .replace("{lang_upper}", lang.upper())\
                .replace("{blog_url}", blog_url)\
                .replace("{home_url}", home_url)
            
            with open(os.path.join(article_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(final_html)
                
            articles.append({
                "url": url,
                "title": title,
                "category": meta.get("category", ""),
                "description": desc,
                "media": media
            })
            print(f"Generated article: {url}")
            
        if articles:
            generate_index(articles, lang)

if __name__ == "__main__":
    main()
