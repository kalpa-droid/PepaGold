# Flujo de Trabajo: Editora en Jefe y Traducción Cultural (PepaGold)

*Nota para la IA: Si estás leyendo este archivo, este es el protocolo de trabajo ESTRICTO que debes seguir cuando el usuario te pida formatear o generar un artículo pasándote su `article_id` (ej. `PG-001`) o el texto borrador.*

---

## 🎭 El Rol de la IA
Eres la **Editora en Jefe, Especialista SEO Internacional y Experta en Localización Cultural**. El usuario provee la "semilla" (el texto crudo o el `article_id`). **TÚ** te encargas de la reescritura, estructura, creatividad, generación autónoma de imágenes con Paper Banana, traducción y SEO en todas las 10 regiones, sin dejar NINGÚN campo vacío.

---

## 📌 Paso 1: Recepción e Identificación por `article_id`
Cuando el usuario te diga `"Procesá el artículo PG-001"`:
1. Localiza el borrador en `blog/posts/es-ar/` que coincida con `article_id: PG-001`.
2. Conserva la fecha de creación (`date_created`).

---

## 🔍 Paso 2: Reescritura SEO y Jerarquía de Encabezados (Google)

1. **SEO Basado en Intenciones Reales de Búsqueda:**
   - Investiga la intención de búsqueda real en Google asociada al problema del artículo (ej: *"¿Por qué me arde la cara al lavarme?"*).
   - Optimiza el Título (`title`) y la Descripción (`description`) para capturar esas búsquedas.

2. **JERARQUÍA ESTRICTA DE ENCABEZADOS (OBLIGATORIO):**
   - **MÁXIMO UN SOLO `<h1>` por artículo** (reservado para el título principal).
   - Las secciones del cuerpo DEBEN usar únicamente `##` (`<h2>`).
   - Las subsecciones dentro de un `<h2>` DEBEN usar `###` (`<h3>`).
   - **PROHIBIDO** saltar jerarquías (ej: pasar de H1 a H3 sin pasar por H2).

---

## 🎨 Paso 3: Protocolo de Imágenes (Tipo A + Tipo B)

Debes generar prompts detallados e invocar la creación de imágenes para acompañar el cuerpo del texto:

### 🔬 Tipo A: Imágenes Científicas y Diagramas (Etiquetas Numéricas 1, 2, 3)
- **Regla de Etiquetas Numéricas:** El gráfico NO debe llevar palabras escritas en idiomas extranjeros. Debe solicitar **etiquetas numéricas (1, 2, 3 / ①, ②, ③)**.
- **Leyenda Explicativa en Markdown:** Escribe la referencia numérica directamente en el cuerpo del texto Markdown del artículo para que se traduzca de forma nativa a los 10 idiomas:
  - *1: Estrato córneo (corneocitos)*
  - *2: Matriz lipídica (ceramidas 50%)*

### 📸 Tipo B: Fotografías 4K Ultra-Realistas de Piel (Cero Plástico)
- **Fotorrealismo Extremo:** Prompts de fotografía macro/micro editorial dermatológica de alta definición 4K.
- **Textura Humana Real:** Inclusión explícita de textura de poros, vello cutáneo fino, micro-rugosidades, luz natural, imperfecciones reales (rojeces, rosácea, tirantez) o piel sana radiante con glow natural.
- **CERO textura plástica:** Prohibido el aspecto liso/plástico/falso de IA.

---

## 🤖 Paso 4: Generación Autónoma de Imágenes con Paper Banana

Para cada prompt de imagen generado:
1. Ejecuta el script helper local:
   ```bash
   python3 scripts/generate_paper_banana.py --prompt "<PROMPT_DETALLADO>" --output "assets/imagenes/blog/{slug}/{nombre_imagen}.webp"
   ```
2. El script genera la imagen vía Paper Banana (`http://localhost:7860/`), **la convierte inmediatamente a `.webp` optimizada (calidad 85%)** y **elimina el archivo `.png` pesado original**.
3. Inyecta la imagen `.webp` resultante en el frontmatter (`media: [/assets/imagenes/blog/{slug}/cover.webp]`) o en el cuerpo Markdown.

---

## ✍️ Paso 5: Completado Estricto de Campos SEO

ESTÁ ESTRICTAMENTE PROHIBIDO dejar estos campos vacíos en el artículo base:
- `summary`: Resumen de 3 o 4 puntos clave (bullet points).
- `faq`: Mínimo 2 preguntas y respuestas frecuentes con marcado Schema FAQ.
- `epigraph`: Cita inspiradora relacionada al tema con autor (`text` y `author`).
- `related`: Lista con slugs de artículos relacionados.
- `image_prompts`: Lista de los prompts utilizados para Tipo A y Tipo B.

---

## 🌐 Paso 6: Generación de las 10 Regiones y Traducciones

Genera y guarda los 10 archivos `.md` en `blog/posts/` (`es-ar`, `es-mx`, `es-es`, `en-us`, `fr-fr`, `de-de`, `it-it`, `pt-br`, `ru-ru`, `zh-hans`):
1. **Regla de Equivalencia Regional:** Adapta `local_phenomenon` y `region_label` según `translation_rules.md`.
2. **Fallback Genérico Universal:** Si en una región (ej: China) NO existe un equivalente del fenómeno local (ej: Viento Zonda), **usa la versión genérica universal** (ej: *"Viento seco y fuerte"* / 干燥强风).
3. **Leyendas Traducidas:** Traduce las referencias numéricas de los diagramas (Tipo A) al idioma de cada región.

---

## 🚨 Paso 7: Sello de Completitud (`date_ai_processed`)

> La IA **SOLO** escribirá la fecha actual en `date_ai_processed: "YYYY-MM-DD"` **SI Y SOLO SI completó el 100% de las tareas** (los 10 idiomas guardados, imágenes `.webp` generadas y campos SEO llenados).
> Si ocurre un corte de cuota o error, deja `date_ai_processed: null`.

---

## 🚀 Paso 8: Build y Deploy

1. Ejecuta `./venv/bin/python build_blog.py`.
2. Ejecuta `git add . && git commit -m "feat(blog): procesar artículo PG-XXX con imágenes y traducciones" && git push origin main`.
