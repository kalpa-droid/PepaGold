import os
import glob
import yaml
import markdown
import re

base_dir = "."

def extract_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Match YAML frontmatter between ---
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return {}, content

html_article_template = """<!DOCTYPE html>
<html lang="es">
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
.hero-image-placeholder { width: 100%; height: 400px; background: var(--bg-secondary); border-radius: 18px; margin-bottom: 40px; display: flex; align-items: center; justify-content: center; color: var(--color-primary); font-weight: 600; border: 1px dashed var(--color-primary); overflow: hidden; }
.hero-image-placeholder img { width: 100%; height: 100%; object-fit: cover; }
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

<a href="/blog/" class="lang-selector-btn blog-nav-btn-floating" style="position: fixed; top: 65px; right: 130px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">📖</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>

<a href="/" class="floating-droplet" title="Volver a la Tienda PepaGold">
  <img src="/assets/imagenes/icono.svg" alt="PepaGold Icon" />
</a>

<div class="lang-selector-container">
  <div class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">ES</span>
    <span style="font-size: 9px; color: var(--color-primary);">▼</span>
  </div>
  <ul class="lang-dropdown-menu" id="langDropdownMenu">
    <li><a href="/" class="lang-option">🇦🇷 Español (AR)</a></li>
    <li><a href="/mx/" class="lang-option">🇲🇽 Español (MX)</a></li>
    <li><a href="/es/" class="lang-option">🇪🇸 Español (ES)</a></li>
    <li><a href="/us/" class="lang-option">🇺🇸 English</a></li>
  </ul>
</div>

<main class="container">
    <h1>{title}</h1>
    
    <div class="hero-image-placeholder">
        {image_html}
    </div>

    <div class="content">
        {content_html}

        <!-- Product Box Embebido (BOFU) -->
        <div class="product-box">
            <img src="/assets/imagenes/1.webp" alt="Laska Mini Set">
            <h3>Laska Mini Set</h3>
            <p>Desmaquíllate solo con agua. Sin químicos, sin basura. (4.9 ⭐)</p>
            <a href="https://greenwayglobal.ar/shop/brands/fiber/08093?gw=uZv7Gi0Ep5" class="btn">Comprar Ahora →</a>
        </div>

        <!-- Newsletter (Lead Magnet) -->
        <div class="newsletter-box">
            <h3>Descarga nuestra Guía Gratuita</h3>
            <p>7 días para reparar tu barrera cutánea. Ingresa tu email para recibir el PDF.</p>
            <form onsubmit="event.preventDefault(); alert('Formulario demo');">
                <input type="email" placeholder="Tu correo electrónico" required>
                <button type="submit">¡Quiero la Guía!</button>
            </form>
        </div>
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

def generate_index(articles):
    # This reads the template we previously wrote in generate_index.py
    index_html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PepaGold Blog | Artículos y Guías</title>
<meta content="Explora nuestros artículos sobre cuidado de la barrera cutánea, rutinas minimalistas y ecología." name="description"/>
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
    --shadow-sm: 0 4px 15px rgba(42, 37, 35, 0.05);
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.08);
    --shadow-lg: 0 15px 35px rgba(212, 140, 144, 0.15);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; }
h1, h2, h3 { font-family: var(--font-serif); color: var(--color-dark); line-height: 1.2; margin-bottom: 20px; }
a { text-decoration: none; }

.blog-header { text-align: center; padding: 120px 20px 60px; background: var(--bg-secondary); }
.blog-header h1 { font-size: 2.8rem; margin-bottom: 10px; }
.blog-header p { font-size: 1.1rem; max-width: 600px; margin: 0 auto; color: var(--color-dark-muted); }

.pain-agitation-section { background: var(--bg-primary); padding: 90px 20px 70px; text-align: center; position: relative; overflow: hidden; }
.interactive-pain { max-width: 1000px; margin: 0 auto; display: flex; flex-direction: column; gap: 80px; position: relative; z-index: 2; }
.pain-card-v2 { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 50px; align-items: center; text-align: left; }
.pain-card-v2:nth-child(even) { direction: rtl; }
.pain-card-v2:nth-child(even) > * { direction: ltr; }

.card-video { width: 100%; max-width: 400px; margin: 0 auto; aspect-ratio: 1 / 1; border-radius: 16px; border: 1px dashed var(--color-primary); box-shadow: var(--shadow-sm); overflow: hidden; position: relative; background-color: var(--bg-secondary); transition: box-shadow 0.4s ease, transform 0.4s ease; display: flex; align-items: center; justify-content: center; }
.card-video:hover { box-shadow: var(--shadow-lg); transform: translateY(-5px); }
.card-video span { color: var(--color-primary); font-weight: 600; text-align: center; padding: 20px; }
.card-video img { width: 100%; height: 100%; object-fit: cover; }

.text-content { display: flex; flex-direction: column; gap: 12px; }
.accent-subtitle { color: var(--color-accent); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; display: flex; align-items: center; gap: 8px; }
.problem-title { font-family: var(--font-serif); font-size: 2.2rem; line-height: 1.2; color: var(--color-dark); margin: 0; }
.problem-description { font-family: var(--font-sans); font-size: 1.1rem; line-height: 1.7; color: var(--color-dark-muted); font-weight: 300; margin: 0; }

.read-btn { display: inline-flex; align-items: center; gap: 8px; margin-top: 15px; font-weight: 600; color: var(--color-primary); font-size: 1.05rem; transition: all 0.3s ease; align-self: flex-start; }
.read-btn::after { content: '→'; transition: transform 0.3s ease; }
.read-btn:hover { color: var(--color-primary-hover); }
.read-btn:hover::after { transform: translateX(5px); }

/* Floating Buttons */
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
@media (max-width: 768px) {
  .pain-card-v2 { grid-template-columns: 1fr; gap: 30px; }
  .pain-card-v2:nth-child(even) { direction: ltr; }
  .problem-title { font-size: 1.8rem; }
}
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

<a href="/blog/" class="lang-selector-btn blog-nav-btn-floating" style="position: fixed; top: 65px; right: 130px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">📖</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>

<a href="/" class="floating-droplet" title="Volver a la Tienda PepaGold">
  <img src="/assets/imagenes/icono.svg" alt="PepaGold Icon" />
</a>

<div class="lang-selector-container">
  <div class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">ES</span>
    <span style="font-size: 9px; color: var(--color-primary);">▼</span>
  </div>
  <ul class="lang-dropdown-menu" id="langDropdownMenu">
    <li><a href="/" class="lang-option">🇦🇷 Español (AR)</a></li>
    <li><a href="/mx/" class="lang-option">🇲🇽 Español (MX)</a></li>
    <li><a href="/es/" class="lang-option">🇪🇸 Español (ES)</a></li>
    <li><a href="/us/" class="lang-option">🇺🇸 English</a></li>
  </ul>
</div>

<header class="blog-header">
    <h1>PepaGold Blog</h1>
    <p>El camino hacia una piel sana empieza por entenderla. Descubre nuestros artículos y guías definitivas.</p>
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
        img_html = f'<img src="{article.get("image")}" alt="{article.get("title")}">' if article.get('image') else f'<span>[Imagen {article.get("title", "")}]</span>'
        
        card = f"""
    <div class="pain-card-v2">
        <div class="card-video">
            {img_html}
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
    
    os.makedirs(os.path.join(base_dir, "blog"), exist_ok=True)
    with open(os.path.join(base_dir, "blog/index.html"), "w", encoding="utf-8") as f:
        f.write(out)
        
    print("ZigZag index generated at blog/index.html")

def main():
    # Only process default locale 'es' for the index for now
    md_files = glob.glob(os.path.join(base_dir, "blog/posts/es/*.md"))
    
    articles = []
    
    for filepath in md_files:
        filename = os.path.basename(filepath)
        slug = filename.replace(".md", "")
        
        meta, body = extract_frontmatter(filepath)
        content_html = markdown.markdown(body)
        
        # Build the individual article HTML
        url = f"/blog/{slug}/index.html"
        article_dir = os.path.join(base_dir, f"blog/{slug}")
        os.makedirs(article_dir, exist_ok=True)
        
        title = meta.get("title", slug)
        desc = meta.get("description", "")
        img = meta.get("image", "")
        
        image_html = f'<img src="{img}" alt="{title}">' if img else "[Aquí va la imagen de portada 800x400]"
        
        final_html = html_article_template.replace("{title}", title).replace("{description}", desc).replace("{content_html}", content_html).replace("{image_html}", image_html)
        
        with open(os.path.join(article_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(final_html)
            
        articles.append({
            "url": f"/blog/{slug}/",
            "title": title,
            "category": meta.get("category", ""),
            "description": desc,
            "image": img
        })
        print(f"Generated article: {url}")
        
    generate_index(articles)

if __name__ == "__main__":
    main()
