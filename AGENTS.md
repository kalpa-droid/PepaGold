# Instrucciones Automáticas del Proyecto PepaGold

> 🤖 **Nota para Antigravity / Asistente IA:** Este archivo contiene las instrucciones globales del proyecto. En cualquier conversación nueva dentro de este workspace, ya conoces todo este contexto automáticamente.

---

## 📌 Contexto del Repositorio
- **Directorio local:** `/home/mappo/Kalpagrafica/PepaGold`
- **Repositorio GitHub:** `git@github.com:kalpa-droid/PepaGold.git` (Rama `main`)
- **Dominio web:** `https://pepagold.blog`
- **Admin CMS:** `https://pepagold.blog/admin/`

---

## 🎯 Reglas de Redacción Fija (Público 18-28 años)

Al redactar o procesar cualquier artículo en PepaGold:
1. **Apertura-Gancho (Primeras 2-3 líneas):** Prohibido arrancar con definiciones técnicas, cifras o frases históricas (*"La ciencia ha experimentado..."*). Arrancar SIEMPRE con un síntoma directo (*"¿Te ardió la cara la última vez que..."*), una escena reconocible (*"Salís de la ducha y la piel te tira..."*) o un mito roto.
2. **Ritmo Ágil:** Máximo 20 palabras por oración. Párrafos de máximo 3 líneas en pantalla de celular (40-50 palabras).
3. **Regla Estricta de 5 Imágenes Máximo por Artículo y Etiquetado Único:**
   - **Límite Fijo:** Cada artículo acepta un máximo estricto de **5 imágenes en total** (1 Portada 16:9 + 4 Secciones H2). Prohibido subir o mantener duplicados.
   - **Etiquetado Único Sin Duplicados:** Cada imagen debe estar asignada a una posición única e ininterrumpible (`portada`, `seccion-1`, `seccion-2`, `seccion-3`, `seccion-4`). Si se cambia la etiqueta de una foto a una posición ocupada, el CMS intercambia la posición automáticamente para impedir duplicados de etiqueta.
   - **Eliminación Garantizada:** La eliminación de imágenes en el CMS consulta la firma `sha` en tiempo real para borrar físicamente los archivos de GitHub sin errores.
4. **Preservación del Sistema de Conceptos:** Conservar `concept`, `article_id`, `local_phenomenon`, `region_label` y la Regla de Fallback Genérico Universal en las 10 regiones.

---

## ⚡ COMANDO RÁPIDO: "Procesá el artículo PG-XXX"

Cuando el usuario escriba únicamente:
> `"Procesá el artículo PG-001"` (o cualquier otro ID)

Debes ejecutar **automáticamente y en un solo paso de 0 a 100%** lo siguiente:

1. **Buscar el Borrador:**
   - Busca en `blog/posts/es-ar/` el archivo `.md` con `article_id: PG-XXX`.

2. **Reescritura y SEO (Guía 18-28 Años):**
   - Redacta con apertura por síntoma y párrafos ultracortos.
   - Organiza en 3 a 5 secciones H2, insertando **1 imagen por sección H2**.
   - Inyecta bloques interactivos (`:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`, `:::funfact`).

3. **Generar Prompts e Indicaciones:**
   - Redacta 5 prompts ultra-detallados en `meta.image_prompts` (1 Portada 16:9 + 4 Secciones H2).

4. **Traducciones Multilingües, Inserción de Imágenes e Inspección Preventiva:**
   - Genera los 10 archivos `.md` (`es-ar`, `es-mx`, `es-es`, `en-us`, `fr-fr`, `de-de`, `it-it`, `pt-br`, `ru-ru`, `zh-hans`) manteniendo `concept` e hiper-localización.
   - **Garantía de Imágenes:** Verifica que todas las versiones regionales contengan la imagen de portada y **exactamente 1 imagen intercalada por cada sección H2**, alineadas con la versión `es-ar`.
   - **AUDITORÍA INTERMEDIA OBLIGATORIA (Fase 1):** Ejecuta `./venv/bin/python validate_translations.py --article PG-XXX` inmediatamente después de traducir. Si el script detecta mezcla de idiomas, desalineación de metadatos o imágenes desiguales/faltantes, corrígelo antes de proceder.

5. **Compilación, Auditoría Final y Deploy:**
   - Setea `date_ai_processed: "YYYY-MM-DD"`.
   - Ejecuta `./venv/bin/python build_blog.py`.
   - **AUDITORÍA COMPLETA OBLIGATORIA (Fase 2):** Ejecuta `./venv/bin/python audit_all.py` para validar artículos (idioma, imágenes, estructura) y la estructura del sitio.
   - Si la auditoría da 🟢 0 errores, ejecuta `git add . && git commit -m "feat(blog): procesar artículo PG-XXX con guía 18-28 años en 10 idiomas" && git push origin main`. Si la auditoría falla, corrige el problema y re-audita antes de hacer push.
