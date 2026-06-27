# Guía de Estilo y Sistema de Diseño — PepaGold

A continuación, te presento el sistema de diseño completo y unificado que hemos implementado en la landing page del **Laska Mini Set**. Este sistema sigue una estética "Warm Minimalist" (Minimalismo Cálido), diseñada para transmitir una sensación premium, orgánica y amigable, maximizando la confianza del usuario.

---

## 🎨 Sistema de Color (Warm Minimalist)

La paleta de colores evita los tonos duros y saturados, favoreciendo contrastes suaves que invitan a la lectura y generan una atmósfera de cuidado de la piel.

### Colores Principales (Acentos)
- **Rosa Empolvado / Terracota sutil** (`#D48C90`): Es el color principal de tu marca (`var(--color-primary)`). Se usa en iconos, botones activos, líneas de división y textos a resaltar.
- **Rosa Oscuro Interactivo** (`#C97A7E`): Un tono ligeramente más oscuro (`var(--color-primary-hover)`) que se usa exclusivamente cuando el usuario pasa el mouse (hover) por elementos interactivos para dar un feedback visual de que se puede hacer clic.
- **Terracota Cálido** (`#E29578`): Color de acento (`var(--color-accent)`) usado en pequeños subtítulos (ej. "✨ Laska Mini Set") para generar contraste cálido sin competir con el rosa principal.

### Tonos de Texto y Neutros Oscuros
- **Carbón Profundo** (`#2A2523`): El color más oscuro (`var(--color-dark)` o `var(--color-text-dark)`). Reemplaza al negro puro (`#000000`) para reducir la fatiga visual. Se usa en títulos principales (H1, H2) y fondos oscuros como el Footer.
- **Carbón Atenuado** (`#5A524E`): Color secundario para textos largos y párrafos (`var(--color-dark-muted)`). Facilita la lectura extendida.
- **Transparencia Sutil** (`rgba(42, 37, 35, 0.6)`): Un gris translúcido para etiquetas flotantes, badges o textos complementarios (`var(--color-text-light)`).

### Fondos y Superficies
- **Blanco Puro** (`#FFFFFF`): Fondo principal (`var(--bg-primary)`) usado para bloques que requieren máxima limpieza y contraste.
- **Arena Cálido / Off-White** (`#FAF6F5`): Fondo secundario (`var(--bg-secondary)`) utilizado para crear franjas horizontales que separen secciones, y como fondo de tarjetas (cards) de información.
- **Fondo Rosa Ultra Suave** (`#FDF7F7`): Utilizado en el contenedor del slider interactivo para integrarlo delicadamente al resto de la página (`var(--bg-accent-light)`).
- **Gradiente Premium (Hero)**: Una transición suave y luminosa (`linear-gradient(135deg, #F9F6F0, #F5EBE9, #ECE3DF, #FDFDFB)`) usada en el fondo de la portada principal.

---

## 🖋️ Jerarquía Tipográfica

Se han seleccionado dos familias tipográficas contrastantes y una escala de tamaños fluida (que crece o se encoge automáticamente según el tamaño de la pantalla).

### Fuentes (Familias)
1. **Titulares Elegantes (Serif)**: `Georgia, "Times New Roman", serif`
   - Aplicada a grandes titulares de sección (H1, H2, H3).
   - Transmite sofisticación, autoridad científica y estética "editorial" de belleza de alta gama.
2. **Textos y Botones Limpios (Sans-Serif)**: `'Poppins', sans-serif`
   - Aplicada a descripciones, botones de compra, badges, menú FAQ y el Footer.
   - Es moderna, redonda, muy legible en pantallas pequeñas y equilibra la formalidad de la Serif.

### Pesos Tipográficos (Grosor)
- **Light (300)**: Para descripciones suaves y textos de acompañamiento.
- **Regular (400)**: Para titulares Serif que deben verse delicados.
- **Medium (500) & Semibold (600)**: Para botones, etiquetas y subtítulos cortos (ej. "LIMPIEZA SIN QUÍMICOS").
- **Bold (700)**: Reservado solo para enlaces importantes o precios destacados.

### Tamaños Fluidos (Responsive)
- **H1 (Título Principal)**: Escala desde `2.3rem` (móviles) hasta `4rem` (computadoras).
- **H2 (Títulos de Sección)**: Escala desde `2rem` hasta `3rem`.
- **H3 y H4 (Subtítulos de Tarjetas)**: Rango de `1.1rem` a `1.8rem`.
- **Cuerpo de Texto**: Mantenido en `1rem` (16px) estándar, y `0.9rem` para detalles pequeños.
- *Las alturas de línea oscilan entre `1.2` (titulares para que se vean compactos) y `1.6` a `1.8` (párrafos para darles aire).*

---

## 🔲 Efectos, Bordes y Profundidad (Glassmorphism & Sombras)

El sitio utiliza sutiles efectos 3D para jerarquizar información sin sobrecargar visualmente.

### Bordes
- **Bordes Delicados** (`rgba(212, 140, 144, 0.2)`): Un borde fino color rosa transparente (`var(--border-color)`) delinea las tarjetas de beneficios y el marco de video.
- En interacción (hover), este borde duplica su opacidad al `0.4` para resaltarlo.

### Sombras (Box Shadows)
1. **Sombra Pequeña (sm)**: `0 4px 12px rgba(42, 37, 35, 0.03)` – Leve despegue del fondo para tarjetas inactivas.
2. **Sombra Media (md)**: `0 8px 25px rgba(42, 37, 35, 0.05)` – Usada en elementos interactivos como el botón redondo de arrastre del "Antes y Después" y el borde de videos.
3. **Sombra Larga y Resplandeciente (lg)**: `0 15px 40px rgba(212, 140, 144, 0.12)` – Un "resplandor" cálido rosado que se enciende cuando el usuario pasa el mouse sobre las tarjetas o los botones flotantes.

### Texturas (Granulado Premium)
- Múltiples secciones de la web (Hero y Beneficios) tienen una capa flotante imperceptible (`.grain-overlay-benefits`) que proyecta un "ruido fractal" (film grain) al `3%` de opacidad. Esto elimina la sensación "plana" de los fondos digitales y le da una textura fotográfica/orgánica propia de las marcas de belleza de lujo.

---

## 💡 Botones y CTA (Llamados a la acción)
- **Botón Primario**: Mantiene el color base del e-commerce (Amarillo / `#FFC439` en el caso del producto final) para garantizar alta conversión.
- **Botones Secundarios y Acordeones**: Utilizan fondos oscuros (`var(--color-dark)`) o blancos limpios, reaccionando al pasar el cursor cambiando la letra o el fondo al Rosa Empolvado.

Este sistema permite que cualquier cambio futuro de colores se realice modificando un solo valor global en la sección `:root`, aplicándose automáticamente a toda la página y manteniendo siempre la coherencia y jerarquía visual.
