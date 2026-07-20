# Protocolo y Flujo de Trabajo del Editor IA de PepaGold

Este documento establece la normativa estricta para la edición, optimización SEO, imágenes y traducción multilingüe de los artículos del blog PepaGold.

---

## 📌 Principios Fundamentales del Flujo

1. **Autoconversión a `.webp` Transparente:**
   - **Toda imagen** que el usuario suba manualmente o que la IA genere se convierte automáticamente en el navegador a `.webp` de alta definición (calidad 85%).
   - Se elimina cualquier requerimiento de botones manuales de optimización.

2. **Imágenes Visualmente Limpias (Sin Textos Incrustados):**
   - Las imágenes generadas (diagramas o fotorrealismo) **no deben incluir palabras ni números escritos en los píxeles de la imagen**.
   - **Toda referencia, número o explicación** se redacta en el texto Markdown del artículo. Esto garantiza que las referencias se traduzcan automáticamente y de forma nativa a los **10 idiomas**.

3. **Respeto a las Imágenes Manuales del Usuario:**
   - Si el usuario sube su propia foto o gráfico a la carpeta `assets/imagenes/blog/{slug}/`, la IA la respeta y redacta las referencias en torno a esa imagen.

---

## 🚀 Pasos de Ejecución Autónoma (Comando "Procesá el artículo PG-XXX")

1. **Lectura y SEO del Borrador `es-ar`:**
   - Optimiza `title` y `description`.
   - Organiza la estructura con `<h1>`, `<h2>`, `<h3>` y bloques (`:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`, `:::funfact`).

2. **Generación e Inyección de Imágenes `.webp`:**
   - Escribe los prompts en `meta.image_prompts`.
   - Genera las imágenes `.webp` con Paper Banana local (`python3 scripts/generate_paper_banana.py`).
   - Inserta la portada y las imágenes en el cuerpo del texto en `es-ar`.

3. **Traducción y Adaptación Multilingüe (10 Idiomas):**
   - Genera los 10 archivos `.md` (`es-ar`, `es-mx`, `es-es`, `en-us`, `fr-fr`, `de-de`, `it-it`, `pt-br`, `ru-ru`, `zh-hans`).
   - Aplica la **Regla de Fallback Genérico Universal** (*"Viento seco y fuerte"* si no hay equivalente local).
   - Traduce todas las explicaciones y leyendas de las imágenes en cada idioma.

4. **Sellado de Estado:**
   - **Únicamente al completar el 100% de las 10 regiones**, setea `date_ai_processed: "YYYY-MM-DD"`.
   - Ejecuta `./venv/bin/python build_blog.py` y `git push origin main`.
