import os

# Definir la estructura del blog
blog_structure = [
    {
        "url": "blog/index.html",
        "title": "Blog Oficial PepaGold",
        "h1": "Cuidado de la Piel y Sostenibilidad",
        "description": "Artículos sobre barrera cutánea, rutinas minimalistas y ecología."
    },
    {
        "url": "blog/barrera-cutanea/que-es-la-barrera-cutanea.html",
        "title": "Qué es la Barrera Cutánea | PepaGold",
        "h1": "¿Qué es la barrera cutánea y por qué es tan importante?",
        "description": "Aprende qué es el manto ácido y cómo protegerlo para evitar irritaciones."
    },
    {
        "url": "blog/barrera-cutanea/por-que-arde-la-piel-al-desmaquillarte.html",
        "title": "¿Por qué me arde la piel al desmaquillarme? | PepaGold",
        "h1": "¿Por qué te arde la piel al desmaquillarte?",
        "description": "Descubre las razones científicas del ardor facial y cómo solucionarlo."
    },
    {
        "url": "blog/sostenibilidad/toallitas-biodegradables-la-verdad.html",
        "title": "La verdad sobre las toallitas biodegradables | PepaGold",
        "h1": "Toallitas 'biodegradables': La verdad oculta",
        "description": "Analizamos el impacto real de las toallitas desmaquillantes en el medio ambiente."
    },
    {
        "url": "blog/sostenibilidad/impacto-ambiental-discos-de-algodon.html",
        "title": "Impacto ambiental de los discos de algodón | PepaGold",
        "h1": "El costo oculto del algodón en tu rutina",
        "description": "Cuánta agua se necesita para cultivar los discos de algodón que usas a diario."
    },
    {
        "url": "blog/rutina-minimalista/skinimalismo-que-es.html",
        "title": "Skinimalismo: Qué es y cómo empezar | PepaGold",
        "h1": "Skinimalismo: Menos productos, mejor piel",
        "description": "La tendencia de simplificar tu rutina de belleza para maximizar resultados."
    },
    {
        "url": "blog/rutina-minimalista/laska-vs-agua-micelar-vs-algodon.html",
        "title": "Laska vs Agua Micelar vs Algodón | PepaGold",
        "h1": "Comparativa: Laska vs. Agua Micelar y Algodón",
        "description": "Análisis de costos, beneficios y eficacia del Laska Mini Set contra métodos tradicionales."
    },
    {
        "url": "blog/guias-regionales/viento-zonda-protege-tu-piel.html",
        "title": "Viento Zonda: Cómo proteger tu piel | PepaGold",
        "h1": "Viento Zonda: Cómo proteger tu piel del clima de Salta",
        "description": "Guía definitiva para evitar la deshidratación severa en climas andinos."
    }
]

# Plantilla HTML base (Warm Minimalist)
html_template = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<meta content="{description}" name="description"/>
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
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.05);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; }}
h1, h2, h3 {{ font-family: var(--font-serif); color: var(--color-dark); line-height: 1.3; margin-bottom: 20px; }}
p {{ margin-bottom: 20px; }}
.blog-nav {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); }}
.blog-nav a {{ text-decoration: none; color: var(--color-dark); font-weight: 500; font-size: 1.1rem; }}
.blog-nav a:hover {{ color: var(--color-primary); }}
.container {{ max-width: 800px; margin: 0 auto; padding: 60px 20px; }}
.hero-image-placeholder {{ width: 100%; height: 400px; background: var(--bg-secondary); border-radius: 18px; margin-bottom: 40px; display: flex; align-items: center; justify-content: center; color: var(--color-primary); font-weight: 600; border: 1px dashed var(--color-primary); }}
.product-box {{ background: var(--bg-secondary); padding: 30px; border-radius: 18px; border: 1px solid var(--border-color); margin: 40px 0; text-align: center; box-shadow: var(--shadow-md); }}
.product-box img {{ max-width: 150px; border-radius: 10px; margin-bottom: 20px; }}
.btn {{ display: inline-block; padding: 12px 30px; background: #FFC439; color: var(--color-dark); font-weight: 600; text-decoration: none; border-radius: 30px; margin-top: 15px; transition: transform 0.2s; }}
.btn:hover {{ transform: translateY(-2px); }}
.newsletter-box {{ background: var(--color-primary); color: #fff; padding: 40px; border-radius: 18px; text-align: center; margin: 60px 0; }}
.newsletter-box h3 {{ color: #fff; }}
.newsletter-box input {{ padding: 12px; width: 60%; max-width: 300px; border: none; border-radius: 30px; margin-right: 10px; }}
.newsletter-box button {{ padding: 12px 25px; border: none; background: var(--color-dark); color: #fff; border-radius: 30px; cursor: pointer; font-weight: 600; }}
.site-footer {{ background: var(--color-dark); color: rgba(255, 255, 255, 0.7); padding: 40px 20px; text-align: center; font-size: 0.85rem; margin-top: 80px; }}
</style>
</head>
<body>

<nav class="blog-nav">
    <a href="/index.html">← Volver a la Tienda</a>
    <a href="/blog/index.html">PepaGold Blog</a>
</nav>

<main class="container">
    <h1>{h1}</h1>
    
    <div class="hero-image-placeholder">
        [Aquí va la imagen de portada 800x400]
    </div>

    <div class="content">
        <p><em>Este es un artículo de demostración (Placeholder). Aquí irá el contenido desarrollado sobre: {h1}. Reemplaza este texto con el contenido real.</em></p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        
        <h2>Subtítulo de ejemplo</h2>
        <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

        <!-- Product Box Embebido (BOFU) -->
        <div class="product-box">
            <img src="/assets/imagenes/1.webp" alt="Laska Mini Set">
            <h3>Laska Mini Set</h3>
            <p>Desmaquíllate solo con agua. Sin químicos, sin basura. (4.9 ⭐)</p>
            <a href="https://greenwayglobal.ar/shop/brands/fiber/08093?gw=uZv7Gi0Ep5" class="btn">Comprar Ahora →</a>
        </div>

        <h2>Otro apartado importante</h2>
        <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>

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

</body>
</html>"""

def main():
    base_dir = "/home/mappo/Kalpagrafica/PepaGold"
    
    for page in blog_structure:
        file_path = os.path.join(base_dir, page["url"])
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Format the template with specific data
        content = html_template.format(
            title=page["title"],
            description=page["description"],
            h1=page["h1"]
        )
        
        # Write the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Created: {file_path}")
        
if __name__ == "__main__":
    main()
