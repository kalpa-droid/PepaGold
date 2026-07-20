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
