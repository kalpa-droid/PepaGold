# Instrucciones Automáticas del Proyecto PepaGold

> 🤖 **Nota para Antigravity / Asistente IA:** Este archivo contiene las instrucciones globales del proyecto. En cualquier conversación nueva dentro de este workspace, ya conoces todo este contexto automáticamente.

---

## 📌 Contexto del Repositorio
- **Directorio local:** `/home/mappo/Kalpagrafica/PepaGold`
- **Repositorio GitHub:** `git@github.com:kalpa-droid/PepaGold.git` (Rama `main`)
- **Dominio web:** `https://pepagold.blog`
- **Admin CMS:** `https://pepagold.blog/admin/`
- **Servidor Local Paper Banana (IA imágenes):** `http://localhost:7860/`

---

## ⚡ COMANDO RÁPIDO: "Procesá el artículo PG-XXX"

Cuando el usuario escriba únicamente:
> `"Procesá el artículo PG-001"` (o cualquier otro ID)

Debes ejecutar **automáticamente y en un solo paso de 0 a 100%** lo siguiente:

1. **Buscar el Borrador:**
   - Busca en `blog/posts/es-ar/` el archivo `.md` con `article_id: PG-XXX`.

2. **Reescritura y SEO:**
   - Optimiza título y descripción para búsquedas reales en Google.
   - Aplica jerarquía semántica estricta (1x `<h1>`, `<h2>` para secciones, `<h3>` para subsecciones).
   - Inyecta bloques interactivos (`:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`, `:::funfact`).
   - Llena `summary`, `faq`, `epigraph` y `related`.

3. **Generar e Inyectar Imágenes con Paper Banana (Script Helper):**
   - Redacta prompts para **Tipo A (Científicas con etiquetas numéricas 1, 2, 3)** y **Tipo B (Fotografía 4K realista sin textura plástica)**.
   - Ejecuta para cada imagen:
     ```bash
     python3 scripts/generate_paper_banana.py --prompt "<PROMPT>" --output "assets/imagenes/blog/{slug}/{nombre}.webp"
     ```
   - El script genera la imagen vía Paper Banana (`http://localhost:7860/`), la convierte a `.webp` y elimina el `.png` pesado.

4. **Traducciones Multilingües (10 Regiones):**
   - Genera y guarda los 10 archivos `.md` (`es-ar`, `es-mx`, `es-es`, `en-us`, `fr-fr`, `de-de`, `it-it`, `pt-br`, `ru-ru`, `zh-hans`).
   - Aplica la **Regla de Fallback Genérico Universal** (*"Viento seco y fuerte"* si no hay equivalente local en China/Alemania).
   - Traduce las referencias numéricas de las imágenes Tipo A en cada idioma.

5. **Sello de Completitud y Deploy:**
   - **Solo al completar el 100% de las 10 regiones e imágenes**, setea `date_ai_processed: "YYYY-MM-DD"`.
   - Ejecuta `./venv/bin/python build_blog.py`.
   - Ejecuta `git add . && git commit -m "feat(blog): procesar artículo PG-XXX con imágenes WebP y 10 idiomas" && git push origin main`.
