# Instrucciones Automáticas del Proyecto PepaGold

> 🤖 **Nota para Antigravity / Asistente IA:** Este archivo contiene las instrucciones globales del proyecto. En cualquier conversación nueva dentro de este workspace, ya conoces todo este contexto automáticamente.

---

## 📌 Contexto del Repositorio
- **Directorio local:** `/home/mappo/Kalpagrafica/PepaGold`
- **Repositorio GitHub:** `git@github.com:kalpa-droid/PepaGold.git` (Rama `main`)
- **Dominio web:** `https://pepagold.blog`
- **Admin CMS:** `https://pepagold.blog/admin/`

---

## ⚡ COMANDO RÁPIDO: "Procesá el artículo PG-XXX"

Cuando el usuario escriba únicamente:
> `"Procesá el artículo PG-001"` (o cualquier otro ID)

Debes ejecutar **automáticamente y en un solo paso** los siguientes pasos:

1. **Buscar el Borrador:**
   - Busca en `blog/posts/es-ar/` el archivo `.md` cuyo frontmatter contenga `article_id: PG-XXX`.

2. **Ejecutar el Flujo de Trabajo (EDITOR_WORKFLOW.md):**
   - Reescribe el título y la descripción buscando capturar intenciones reales en Google.
   - Aplica jerarquía semántica estricta de encabezados (1x `<h1>` máximo, `<h2>` para secciones, `<h3>` para subsecciones).
   - Agrega bloques interactivos (`:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`, `:::funfact`).
   - Llena obligatoriamente `summary` (3-4 puntos), `faq` (mínimo 2 preguntas con Schema), `epigraph` y `related`.
   - Genera `image_prompts` detallados en el frontmatter.

3. **Generar las 10 Adaptaciones Regionales (translation_rules.md):**
   - Genera y guarda los 10 archivos `.md` en `blog/posts/es-ar/`, `es-mx/`, `es-es/`, `en-us/`, `fr-fr/`, `de-de/`, `it-it/`, `pt-br/`, `ru-ru/`, `zh-hans/`.
   - Aplica la **Regla de Fallback Genérico Universal** (si en China o Alemania no hay equivalente del fenómeno local, usa la versión genérica universal como *"Viento seco y fuerte"*).

4. **Sello de Completitud (`date_ai_processed`):**
   - **Solo cuando el 100% de las 10 adaptaciones y campos estén terminados**, setea `date_ai_processed: "YYYY-MM-DD"`.

5. **Compilar y Desplegar:**
   - Ejecuta `./venv/bin/python build_blog.py`.
   - Ejecuta `git add . && git commit -m "feat(blog): procesar y traducir artículo PG-XXX" && git push origin main`.
   - Confirma al usuario con el resumen del trabajo realizado.
