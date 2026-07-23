# Protocolo y Flujo de Trabajo del Editor IA de PepaGold

Este documento establece la normativa estricta e innegociable para la edición, optimización SEO, accesibilidad de contraste, distribución de imágenes y traducción multilingüe de los artículos del blog PepaGold.

---

## 🎯 Guía de Redacción Estricta (Público Objetivo 18-28 años)

Todo artículo publicado en PepaGold debe seguir estrictamente estas 8 reglas fijas para convertir información científica/técnica en notas que atrapen a lectoras de 18 a 28 años:

### 1. Voz y Tono
- **Segunda persona:** Hablar directamente en "vos" / "tú" / "tu piel". Nunca en tercera persona impersonal.
- **Tono:** Una amiga cercana que sabe mucho de dermatología, no una profesora dictando cátedra.
- **Autenticidad sobre autoridad:** Primero validar lo que la lectora siente (sus molestias, tirantez, ardor), después explicar por qué pasa.
- **Respeto e Inteligencia:** Tratamiento de alguien inteligente que busca respuestas reales. Cero condescendencia ni infantilización.

### 1.1. Fórmula Estricta de Títulos (SEO + Gancho Emocional para Chicas 18-28)
Todo título debe combinar la búsqueda real que hacen las chicas en Google/TikTok con la solución médica clara.
- **Fórmula:** `[Pregunta o Síntoma Real en Google/TikTok] + [Palabra Clave Científica y Solución]`
- **Ejemplo:** `¿Te arde la cara al ponerte crema? La Ciencia de la Barrera Cutánea y Cómo Repararla`
- **PROHIBIDO:** Títulos aburridos de manual universitario (*"Análisis del Estrato Córneo e Hidratantes"*).

### 2. La Apertura (Primeras 2-3 líneas del artículo)
- **PROHIBIDO ARRANCAR CON:**
  - Definiciones técnicas frías (*"El estrato córneo es..."*).
  - Cifras o estadísticas sueltas.
  - Frases históricas o globales (*"La ciencia ha experimentado..."*).
- **OBLIGATORIO ARRANCAR CON:**
  - **Pregunta directa sobre el síntoma:** *“¿Te ardió la cara la última vez que te pusiste crema?”*
  - **Escena reconocible en 1 línea:** *“Salís de la ducha y la piel te tira como si te hubieras puesto pegamento.”*
  - **Afirmación que rompe un mito común:** *“No, lavarte la cara más seguido no te va a sacar el acné. Puede empeorarlo.”*

### 3. Estructura de Frases y Párrafos (Lectura Móvil)
- **Máximo 20 palabras por oración.** Si la oración se pasa, cortarla en dos.
- **Máximo 3 líneas por párrafo en pantalla de celular (40-50 palabras).**
- **Una idea por párrafo.** Ritmo visual rápido y fluido.

### 4. Explicación de Términos Técnicos
- Nunca definir un término técnico antes de que la lectora sienta curiosidad o entienda el síntoma.
- **Fórmula:** Primero el síntoma que se nota → después la revelación del nombre técnico → después la explicación breve.
  *Ejemplo:* "Tu piel empieza a perder agua más rápido de lo que la repone. Eso tiene nombre: TEWL (pérdida de agua transepidérmica)."

### 5. Estructura Fija de la Nota
1. Eyebrow (Categoría)
2. Título Búsqueda Real (lenguaje de búsqueda de Google, no de laboratorio)
3. Apertura-Gancho (Síntoma / Escena / Mito)
4. Epígrafe (Cita inspiradora corta)
5. Resumen "En 30 segundos" (3-4 viñetas)
6. Imagen de Portada Widescreen 16:9
7. Cuerpo en 3 a 5 Secciones (H2), cada una con su **imagen intercalada**
8. Checklist accionable (`:::checklist`)
9. Mini-Quiz (`:::quiz`)
10. Enlace a "Lo que dice la ciencia"
11. CTA de Producto traducido
12. Preguntas Frecuentes (FAQ Schema en lenguaje de búsqueda real)

### 6. Regla Estricta Anti-Duplicación y Conciencia de Artículos Previos
- **PROHIBIDO:** Redactar un nuevo artículo reciclando la misma estructura, las mismas preguntas del quiz, la misma lista de verificación (checklist) o los mismos prompts de imagen de un artículo anterior. 
- **OBLIGATORIO:** Antes de redactar o generar contenido nuevo, el Editor IA DEBE revisar los informes técnicos crudos guardados en la carpeta `/reports/` (ej. `PG-001.txt`, `PG-002.txt`) y los artículos publicados, para asegurar que el nuevo artículo:
  - Tenga un enfoque científico, título y ángulo **totalmente nuevo y distinto**.
  - Incluya secciones H2, un Checklist y un Quiz con datos **exclusivos y específicos** de ese nuevo informe técnico.
  - Genere **prompts de imagen 100% únicos** que ilustren la ciencia exacta de ese nuevo artículo (nunca reciclar prompts genéricos).

### 7. Jerarquía Tipográfica y Regla Estricta de Encabezados (H1 vs H2)
- **PROHIBIDO:** Incluir `# Título` (encabezado H1) dentro del cuerpo del artículo en el archivo Markdown. La plantilla del blog ya genera automáticamente el título como el único `<h1>` principal del documento.
- **OBLIGATORIO:** El cuerpo del artículo debe comenzar directamente con la introducción y usar únicamente `## Nombre de Sección` (H2) para los apartados. Colocar un H1 dentro del cuerpo rompe la jerarquía tipográfica, genera un título gigante duplicado y desajusta el diseño visual y el SEO.

---

## 📸 Regla Estricta de Imágenes e Indicaciones Prompts

1. **Imagen de Portada (Prompt #1 - 16:9 Widescreen 1200x630px):**
   - Fotografía panorámica horizontal. Se ubica en la cabecera del artículo (debajo del título y metadatos) y en la tarjeta del índice.
2. **Imágenes del Cuerpo (Prompts #2 a #5 - 1:1 o 4:3):**
   - **PROHIBIDO agrupar imágenes al principio o al final.**
   - Debe haber **1 imagen específica por cada sección H2**, insertada **dentro del texto Markdown** de esa sección.
   - Si el artículo tiene 4 secciones H2, el modal de prompts de la IA debe generar **5 prompts detallados de 8K** (1 Portada + 4 Secciones H2).
   - Sintaxis Markdown dentro de la sección H2:
     ```markdown
     ## Título de la sección H2

     Primer párrafo corto...

     ![Descripción de la imagen científica](/@file_path.webp)

     Segundo párrafo continuando la explicación...
     ```

---

## 🌐 Preservación de Metadatos y Adaptación Cultural (10 Idiomas)

1. **Preservación del ID de Concepto (`concept`):**
   - El atributo `concept: barrera-cutanea-y-microbioma` y `article_id: PG-001` deben mantenerse idénticos en los 10 archivos de idioma.
2. **Adaptación Cultural y Climática (`local_phenomenon`):**
   - Reemplazar el fenómeno según la región (*Viento Zonda* en AR, *PM2.5* en MX/ZH, *Calima* en ES, *Aire seco HVAC* en US, *Frío de invierno* en DE/RU).
3. **Regla de Fallback Genérico Universal:**
   - Si una región no posee un fenómeno local directo, usar una traducción genérica equivalente (*"vientos secos"*, *"dry winds"*, *"干燥风"*).
4. **Cero Duplicados:**
   - En cada carpeta regional (`blog/posts/{locale}/`), debe existir **únicamente 1 archivo `.md` por `article_id`**.

---

## 🖼️ Regla Estricta de Sincronización de Imágenes (Anti-Corrupción)

**Contexto:** Insertar la referencia a una imagen recién subida sin comprobar que el archivo existe de verdad en disco es la causa raíz de artículos con imágenes rotas o cruzadas entre idiomas.

**Regla obligatoria:** El Agente IA **NUNCA** debe escribir manualmente una ruta de imagen en el frontmatter (`cover_image`, `media`) ni en el cuerpo Markdown de un artículo. Para insertar o sincronizar imágenes, el único método permitido es:

```bash
python3 insert_images.py PG-XXX
```

---

## 🚀 Protocolo Oficial en 2 Fases (Flujo de Trabajo Libre de Fricción)

Para garantizar la **integridad absoluta del sitio**, la edición y publicación de artículos se realiza **estrictamente en 2 Fases interactivas**:

### 📍 FASE 1: Redacción Base (`es-ar`) y Generación de Prompts
1. El usuario entrega un informe técnico o indica un tema (`/reports/PG-XXX.txt`).
2. El Agente IA redacta **únicamente** la versión original en español argentino (`blog/posts/es-ar/{slug}.md`).
3. El Agente IA genera los **5 Prompts de Imagen hiperdetallados en 8K** (1 Portada 16:9 + 4 Secciones H2 1:1).
4. **PAUSA OBLIGATORIA:** El Agente IA muestra los 5 Prompts por chat y le dice al usuario:  
   > *"Ya están listos los 5 prompts de imagen. Generá las fotos, guardalas como `prompt_1.webp` a `prompt_5.webp` en `assets/imagenes/blog/{slug}/` (o súbalas por el CMS) y avisame escribiendo 'Ya subí las imágenes'."*

### 📍 FASE 2: Verificación de Disco, Traducciones Multilingües y Deploy
5. El usuario notifica *"Ya subí las imágenes"*.
6. **Verificación de Disco:** El Agente IA ejecuta `python3 insert_images.py PG-XXX` para confirmar que los 5 archivos `.webp` existan físicamente y pesen > 8 KB.
7. **Traducción Multilingüe Blindada:** Una vez confirmadas las imágenes en `es-ar`, el Agente IA traduce el artículo a los otros 9 idiomas (`es-mx`, `es-es`, `en-us`, `fr-fr`, `de-de`, `it-it`, `pt-br`, `ru-ru`, `zh-hans`) adaptando el fenómeno local (`local_phenomenon`).
8. **Compilación y Auditoría:** Se ejecuta `python3 build_blog.py` y `python3 audit_all.py`.
9. **Deploy Automático:** Únicamente si la auditoría devuelve `🟢 0 errores`, el Agente IA ejecuta `git add .`, `git commit` y `git push origin main`.
