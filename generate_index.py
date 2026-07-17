import os

blog_structure = [
    {
        "url": "/blog/barrera-cutanea/que-es-la-barrera-cutanea.html",
        "category": "✨ Ciencia & Piel",
        "title": "¿Qué es la barrera cutánea?",
        "description": "Aprende qué es el manto ácido y cómo protegerlo para evitar irritaciones. El primer paso para una piel sana y resistente."
    },
    {
        "url": "/blog/barrera-cutanea/por-que-arde-la-piel-al-desmaquillarte.html",
        "category": "⚠️ Problemas Comunes",
        "title": "¿Por qué me arde la piel al desmaquillarme?",
        "description": "Descubre las razones científicas del ardor facial. Los desmaquillantes químicos limpian el maquillaje y destruyen tu piel."
    },
    {
        "url": "/blog/sostenibilidad/toallitas-biodegradables-la-verdad.html",
        "category": "🌍 Sostenibilidad",
        "title": "La verdad sobre las toallitas biodegradables",
        "description": "Analizamos el impacto real de las toallitas desmaquillantes en el medio ambiente. Spoiler: no son tan verdes como dicen."
    },
    {
        "url": "/blog/sostenibilidad/impacto-ambiental-discos-de-algodon.html",
        "category": "🌍 Sostenibilidad",
        "title": "Impacto ambiental del algodón",
        "description": "Cuánta agua se necesita para cultivar los discos de algodón que usas a diario y tiras a la basura en 3 segundos."
    },
    {
        "url": "/blog/rutina-minimalista/skinimalismo-que-es.html",
        "category": "🧴 Rutina",
        "title": "Skinimalismo: Qué es",
        "description": "La tendencia de simplificar tu rutina de belleza para maximizar resultados y dejar de asfixiar tu piel."
    },
    {
        "url": "/blog/rutina-minimalista/laska-vs-agua-micelar-vs-algodon.html",
        "category": "⚖️ Comparativas",
        "title": "Laska vs. Agua Micelar",
        "description": "Análisis de costos, beneficios y eficacia del Laska Mini Set contra los métodos tradicionales de limpieza."
    },
    {
        "url": "/blog/guias-regionales/viento-zonda-protege-tu-piel.html",
        "category": "🏜️ Guías Regionales",
        "title": "Viento Zonda y tu Piel",
        "description": "Guía definitiva para evitar la deshidratación severa en climas andinos. Cómo protegerte del Zonda en Salta y Jujuy."
    }
]

html_template = """<!DOCTYPE html>
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

/* Header Hero */
.blog-header { text-align: center; padding: 120px 20px 60px; background: var(--bg-secondary); }
.blog-header h1 { font-size: 2.8rem; margin-bottom: 10px; }
.blog-header p { font-size: 1.1rem; max-width: 600px; margin: 0 auto; color: var(--color-dark-muted); }

/* ZigZag Section */
.pain-agitation-section { background: var(--bg-primary); padding: 90px 20px 70px; text-align: center; position: relative; overflow: hidden; }
.interactive-pain { max-width: 1000px; margin: 0 auto; display: flex; flex-direction: column; gap: 80px; position: relative; z-index: 2; }
.pain-card-v2 { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 50px; align-items: center; text-align: left; }
.pain-card-v2:nth-child(even) { direction: rtl; }
.pain-card-v2:nth-child(even) > * { direction: ltr; }

.card-video { width: 100%; max-width: 400px; margin: 0 auto; aspect-ratio: 1 / 1; border-radius: 16px; border: 1px dashed var(--color-primary); box-shadow: var(--shadow-sm); overflow: hidden; position: relative; background-color: var(--bg-secondary); transition: box-shadow 0.4s ease, transform 0.4s ease; display: flex; align-items: center; justify-content: center; }
.card-video:hover { box-shadow: var(--shadow-lg); transform: translateY(-5px); }
.card-video span { color: var(--color-primary); font-weight: 600; text-align: center; padding: 20px; }

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

<!-- Botón al Blog flotante -->
<a href="/blog/" class="lang-selector-btn blog-nav-btn-floating" style="position: fixed; top: 65px; right: 130px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">📖</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>

<!-- Gota de agua del logo flotante -->
<a href="/" class="floating-droplet" title="Volver a la Tienda PepaGold">
  <img src="/assets/imagenes/icono.svg" alt="PepaGold Icon" />
</a>

<!-- Selector de idiomas flotante -->
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

def main():
    out = html_template
    for article in blog_structure:
        card = f"""
    <div class="pain-card-v2">
        <div class="card-video">
            <span>[Imagen {article['title']}]</span>
        </div>
        <div class="text-content">
            <span class="accent-subtitle">{article['category']}</span>
            <h3 class="problem-title">{article['title']}</h3>
            <p class="problem-description">{article['description']}</p>
            <a href="{article['url']}" class="read-btn">Leer Artículo</a>
        </div>
    </div>
"""
        out += card
    out += footer
    
    os.makedirs("/home/mappo/Kalpagrafica/PepaGold/blog", exist_ok=True)
    with open("/home/mappo/Kalpagrafica/PepaGold/blog/index.html", "w", encoding="utf-8") as f:
        f.write(out)
        
    print("ZigZag index generated at blog/index.html")

if __name__ == "__main__":
    main()
