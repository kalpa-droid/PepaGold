# Protocolo y Flujo de Trabajo del Editor IA de PepaGold

Este documento establece la normativa estricta para la edición, optimización SEO, accesibilidad de contraste, imágenes y traducción multilingüe de los artículos del blog PepaGold.

---

## 📌 Principios Fundamentales del Flujo

1. **Alto Contraste y Accesibilidad Obligatorios (Bloques `:::stat`):**
   - **Regla Estricta:** Ningún bloque de texto, cita o estadística debe renderizar texto muted o con opacidad sobre fondos oscuros.
   - Todos los bloques `:::stat` deben usar fondo de alto contraste (`#FDF7F7`) con borde rosa empolvado (`#D48C90`), número grande en `2.6rem` y texto en color oscuro (`#2A2523`) con **ratio de contraste AAA (mínimo 15:1)**.

2. **Flujo Inteligente de Asignación de Imágenes (`✨ Aplicar Imágenes al Artículo`):**
   - **Paso 1 (Planificación IA):** La IA editora redacta el artículo, reserva los espacios para imágenes (Portada `media[0]`, Cuerpo `imagen_1.webp`), escribe las referencias explicativas en el texto Markdown y genera los prompts ultra-detallados de 8K en `meta.image_prompts`.
   - **Paso 2 (Generación Usuario):** El usuario copia el prompt con el botón **`📋 Copiar Prompt`**, genera o busca su foto y la sube en el CMS con **`➕ Subir Imagen (Auto WebP)`**.
   - **Paso 3 (Publicación en 1 Clic):** Al tocar **`✨ Aplicar Imágenes al Artículo y Publicar`**, el CMS asigna automáticamente las imágenes `.webp` subidas a la portada y a los espacios del texto, publica en GitHub y distribuye los cambios a los **10 idiomas del blog**.

3. **Imágenes Visualmente Limpias (Sin Textos Incrustados):**
   - Las imágenes generadas se mantienen **sin textos incrustados dentro del gráfico**.
   - Toda leyenda o explicación se redacta en el cuerpo Markdown para garantizar que se traduzca nativamente a los 10 idiomas.

4. **Regla Estricta de 1 Archivo por Artículo en Cada Idioma (Cero Duplicados):**
   - En cada directorio regional (`blog/posts/{locale}/`), debe existir **únicamente 1 archivo `.md` por cada `article_id`** (ej. `skin-barrier-science-microbiome.md`).
   - Queda estrictamente prohibido dejar copias del archivo con nombre en español en directorios de otros idiomas.
   - Todo el contenido (encabezados, frontmatter, epígrafe, resúmenes, cuerpo, llamados interactivos) debe estar **100% traducido al idioma nativo de la región**.

---

## 🚀 Pasos de Ejecución Autónoma

1. **SEO y Maquetación `es-ar`:**
   - Optimiza `title` y `description`.
   - Incluye bloques de alto contraste (`:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`, `:::funfact`).

2. **Prompts e Inyección:**
   - Escribe los prompts 8K en `meta.image_prompts`.
   - Deja listos los espacios de imágenes en el texto Markdown.

3. **Traducción y Adaptación Multilingüe (10 Idiomas):**
   - Genera los 10 archivos `.md` aplicando la Regla de Fallback Genérico Universal si no hay fenómeno local equivalente.

4. **Publicación y Deploy:**
   - Setea `date_ai_processed: "YYYY-MM-DD"`.
   - Ejecuta `./venv/bin/python build_blog.py` y `git push origin main`.
