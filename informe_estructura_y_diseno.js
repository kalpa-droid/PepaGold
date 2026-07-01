/**
 * =========================================================================
 * PEPA GOLD - INFORME COMPLETO DE ESTRUCTURA, TEXTOS Y DISEÑO VISUAL
 * =========================================================================
 * Este archivo contiene el mapeo estructurado del 100% de la landing page.
 * Puede ser importado como módulo JS o ejecutado directamente con Node.js
 * para imprimir el reporte en consola.
 * 
 * Ruta de guardado: /home/mappo/Kalpagrafica/PepaGold/informe_estructura_y_diseno.js
 */

const informeLandingPage = {
  metadata: {
    producto: "Laska Mini Set",
    marca: "Greenway Global",
    version: "3.4 (Overhaul de Conversión para Jóvenes Argentinas)",
    fechaInforme: "01 de Julio, 2026",
    idiomaPrincipal: "Español (Argentina)"
  },
  
  sistemaDiseno: {
    estiloVisual: {
      concepto: "Warm Minimalist (Minimalismo Cálido)",
      sensacion: "Premium, orgánica, clínica y editorial. Diseñada para generar confianza y sintonizar con un público joven.",
      texturas: "Capa de ruido fractal (film grain) al 3% de opacidad para eliminar la sensación plana digital."
    },
    paletaColores: {
      acentos: {
        primario: "#D48C90 (Rosa Empolvado - Usado en botones activos, iconos, etiquetas y titulares a resaltar)",
        hover: "#C97A7E (Rosa Oscuro - Feedback de interacción de cursor en botones y links)",
        acentoCálido: "#E29578 (Terracota Cálido - Usado para destacar pequeños subtítulos y badges)"
      },
      neutros: {
        carbonProfundo: "#2A2523 (Color de texto principal. Reemplaza el negro puro para reducir la fatiga visual)",
        carbonAtenuado: "#5A524E (Color secundario para párrafos y descripciones largas)",
        transparenteMuted: "rgba(42, 37, 35, 0.6) (Gris translúcido para badges flotantes y subtítulos sutiles)"
      },
      superficies: {
        blancoPuro: "#FFFFFF (Fondo de secciones que requieren luz y máximo contraste)",
        arenaCalido: "#FAF6F5 (Fondo off-white para separar secciones y destacar tarjetas de información)",
        rosaUltraSuave: "#FDF7F7 (Fondo rosa empolvado ultra suave para tarjetas y badges destacados)",
        gradienteHero: "linear-gradient(135deg, #F9F6F0, #F5EBE9, #ECE3DF, #FDFDFB) (Fondo del Hero principal)"
      },
      sombrasBordes: {
        bordeDelicado: "rgba(212, 140, 144, 0.2) (Borde rosa transparente para tarjetas y videos)",
        sombraChica: "0 4px 12px rgba(42, 37, 35, 0.03) (Tarjetas inactivas)",
        sombraMedia: "0 8px 25px rgba(42, 37, 35, 0.05) (Slider antes/después y borde de videos)",
        sombraLarga: "0 15px 40px rgba(212, 140, 144, 0.12) (Resplandor rosado al hacer hover)"
      }
    },
    tipografia: {
      fuenteTitulares: "Georgia, 'Times New Roman', serif (Elegancia editorial, autoridad científica)",
      fuenteCuerpoBotones: "'Poppins', sans-serif (Legibilidad moderna, balance orgánico)",
      escalaFluida: {
        h1: "clamp(2.3rem, 3.8vw, 4rem)",
        h2: "clamp(2rem, 3.5vw, 3rem)",
        h3: "clamp(1.4rem, 2.2vw, 1.8rem)",
        h4: "clamp(1.1rem, 1.8vw, 1.3rem)",
        cuerpo: "1rem (16px) estándar, 0.9rem para detalles y 0.75rem para pies de página"
      }
    }
  },

  estructuraSecciones: [
    {
      orden: 1,
      seccion: "Marquesina Superior (Top Banner)",
      visual: "Franja de color rosa con texto blanco deslizante (marquee).",
      contenido: {
        textosLiterales: [
          "🔥 Oferta por Tiempo Limitado — Comprar ahora (Enlace directo a Greenway Global)",
          "💸 Ahorrá +$15.000 al año en desmaquillantes",
          "🌱 Ecológico · Dura hasta 2 años · Sin químicos",
          "¿Dudas? Resuélvelas acá (Enlace interno #faq-section)"
        ]
      }
    },
    {
      orden: 2,
      seccion: "Hero Banner (Portada Principal)",
      visual: "Fondo gradiente cálido. Distribución a dos columnas en PC: izquierda texto de venta con CTA amarillo de alta conversión, derecha slider dinámico interactivo 'Antes y Después' de la piel con tirador de arrastre.",
      contenido: {
        titularH1: "Desmaquillate. Solo con agua. Nada más.",
        subhead: "El set que reemplaza todo lo demás.",
        descripcion: "Tres piezas de microfibra que eliminan el maquillaje, la grasa y la suciedad del día usando solo agua tibia. Reemplazan los discos de algodón, el agua micelar y el desmaquillante. Duran hasta 2 años. Una compra, cero residuos.",
        CTA: "COMPRAR AHORA →",
        badgeGarantia: "Primeras compradoras verificadas: 4.9/5",
        precioIntegrado: "$28.500 ARS"
      }
    },
    {
      orden: 3,
      seccion: "Strip de Prueba Social Inmediata (NUEVO)",
      visual: "Strip horizontal en desktop / carrusel horizontal con snap en mobile. Color arena cálido (#FAF6F5). Contiene fotos de clientas, estrellas de calificación, testimonios de una sola línea y firmas con edad y ciudad argentina.",
      contenido: {
        testimonios: [
          { autor: "Valentina (23, Buenos Aires)", text: "Lo compré por curiosidad. No volví a comprar discos de algodón." },
          { autor: "Camila (27, Córdoba)", text: "Mi piel mejoró en dos semanas. No es exageración." },
          { autor: "Lucía (21, Rosario)", text: "La mejor plata que gasté en skincare este año, sin duda." }
        ],
        footer: "23.415 reseñas verificadas · Promedio 4.9/5"
      }
    },
    {
      orden: 4,
      seccion: "Agitación del Dolor (Pain Agitation)",
      visual: "Formato de 3 tarjetas alineadas en zigzag vertical con videos interactivos, contadores dinámicos y bordes redondeados.",
      contenido: {
        tarjetas: [
          {
            titulo: "¿Harta de gastar de más cada mes?",
            descripcion: "Discos de algodón, agua micelar, toallitas, desmaquillante… Solo en descartables, una mujer promedio tira más de $4.000 por mes. Literalmente a la basura.",
            metrica: "Gasto Innecesario"
          },
          {
            titulo: "¿Tu piel queda roja e irritada al desmaquillarte?",
            descripcion: "Los desmaquillantes químicos limpian el maquillaje y, de paso, destruyen la capa que protege tu piel. Resultado: piel seca, irritada y más brotes que antes de usarlos.",
            metrica: "Piel Seca e Irritada"
          },
          {
            titulo: "¿Tu rutina nocturna tiene mil pasos?",
            descripcion: "Son las 12 de la noche y seguís en el baño. Con el Laska Mini Set, un paso. Y te vas a dormir.",
            metrica: "Tiempo Perdido"
          }
        ]
      }
    },
    {
      orden: 5,
      seccion: "Beneficios Rápidos (Slider Antes/Después)",
      visual: "Grid de 2 columnas de texto de beneficios con el slider central Antes/Después de la piel con tirador circular.",
      contenido: {
        tag: "Laska Mini Set",
        titulo: "Limpieza profunda y consciente",
        detalles: ["Limpieza sin químicos", "Microfibra UpPoly", "Suave con tu piel", "Ecológico y duradero"]
      }
    },
    {
      orden: 6,
      seccion: "Video Showcase (3 Productos CARE)",
      visual: "Video horizontal 16:9 de unboxing (LASKA MINI SET.mp4) con overlay inteligente de reproducción. Abajo, tarjetas simplificadas de 3 líneas con imágenes de producto oficiales pegadas al lado de la información.",
      contenido: {
        productos: [
          { nombre: "CARE 4: Cleanser Sponge", desc: "La esponja que atrapa el maquillaje sin jabón. Humedecela, pasala suave y lavala. Dura hasta 2 años." },
          { nombre: "CARE 15: Manopla-Esponja de Doble Cara", desc: "Una cara limpia, la otra exfolia. Para el maquillaje del día a día y para renovar la piel de a poco. Sin ácidos, sin irritación." },
          { nombre: "CARE 6: Soft Mitt", desc: "Textura ultra suave para cuello y escote, las zonas más delicadas. No estira, no irrita. Sin necesidad de ningún producto." }
        ]
      }
    },
    {
      orden: 7,
      seccion: "Ritual de Uso (3 Pasos) (NUEVO)",
      visual: "Grid de 3 tarjetas en fondo blanco con fotos de estilo lifestyle de clientas reales en su rutina y números de pasos flotantes en color rosa primario.",
      contenido: {
        titulo: "Tu nueva rutina. Sin pasos de más.",
        subhead: "Funciona igual para el maquillaje del día a día y para el look más cargado.",
        pasos: [
          { paso: "1. Humedecé", desc: "Pasá el paño bajo el agua tibia. Nada más que eso." },
          { paso: "2. Deslizá", desc: "Masajeá con suavidad. Las microfibras atrapan el maquillaje sin frotar fuerte." },
          { paso: "3. Lavá y reutilizá", desc: "Enjuagalo con jabón neutro, colgalo a secar. Mañana está listo de nuevo." }
        ]
      }
    },
    {
      orden: 8,
      seccion: "Opiniones de nuestras clientas (Reviews)",
      visual: "Slider infinito de tarjetas animadas de reviews en formato vertical. Al posar el mouse, se despliega el texto de review larga. Micro-CTA al final del bloque con estrellas de calificación.",
      contenido: {
        tituloH2: "Opiniones de nuestras clientas",
        CTA: "COMPRAR AHORA →",
        reviewsGlobales: "4.9 / 5 de más de 20.000 valoraciones alrededor del mundo"
      }
    },
    {
      orden: 9,
      seccion: "Prueba Experimental UGC (Contenido de Clientes)",
      visual: "Sección con videos cortos en proporción 9:16 tipo TikTok de clientas reales usando las fibras.",
      contenido: {
        tag: "Así lo usan ellas",
        tituloH2: "Unboxing & Uso Cotidiano",
        descripcion: "Sin filtros, sin edición. Así reaccionaron cuando lo probaron por primera vez."
      }
    },
    {
      orden: 10,
      seccion: "CTA Intermedio",
      visual: "Banda con fondo arena, gran botón de compra e información de garantías.",
      contenido: {
        botonText: "COMPRAR AHORA →",
        subtext: "Más de 15.000 argentinas ya lo tienen en su baño. / Envío disponible · Pago seguro · Devolución garantizada"
      }
    },
    {
      orden: 11,
      seccion: "Timeline 30 Días (NUEVO)",
      visual: "Cronograma interactivo horizontal en PC / vertical en móvil con línea de progreso. Conecta el paso del tiempo con cambios reales en la piel de la usuaria.",
      contenido: {
        tituloH2: "¿Qué le pasa a tu piel después de 30 días?",
        pasos: [
          { hito: "Semana 1", desc: "Tu piel deja de estar tirante. Sin el jabón químico diario, la capa natural de lípidos empieza a recuperarse." },
          { hito: "Semana 2", desc: "Los brotes y rojeces se reducen. Menos irritación química directa se traduce en menos inflamación y poros libres." },
          { hito: "Semana 4", desc: "Empezás a ver el glow que querías. La renovación celular es más uniforme y tu piel se ve visiblemente luminosa." },
          { hito: "Semana 8", desc: "Ya no te acordás de cuándo compraste la última bolsa de algodones o desmaquillante. Tu piel está sana y tu baño libre de residuos." }
        ]
      }
    },
    {
      orden: 12,
      seccion: "Lo que dice la ciencia (E-E-A-T)",
      visual: "Grid de 4 tarjetas con especialistas en dermatología y links a laboratorios universitarios.",
      contenido: {
        tituloH2: "Lo que dice la ciencia",
        descripcionHeader: "Limpiar sin jabón no es nuevo. Es lo que los dermatólogos llevan años recomendando para no dañar la capa natural de tu piel. Estos son los especialistas que más saben sobre el tema.",
        expertos: [
          { nombre: "Dr. Richard Gallo (UCSD Lab)", investigacion: "Su investigación muestra que los jabones alteran las bacterias buenas de tu piel. El Laska trabaja con tu microbioma, no contra él." },
          { nombre: "Prof. Kenji Kabashima (Universidad de Kyoto)", investigacion: "Galardonado por sus estudios sobre la hidratación del estrato córneo y los mecanismos fisiopatológicos de la piel seca sensible." },
          { nombre: "Dra. María Eugenia Santillán (Argentina - MP 2455 / MN 73735)", investigacion: "Dermatóloga argentina. Especializada en pieles reactivas. Avala el principio de limpieza sin surfactantes para pieles con acné y rosácea." },
          { nombre: "Dra. T. A. Belousova (Sechenov University)", investigacion: "Referente en la Sechenov University, especializada en protocolos no invasivos para la integridad estructural de la barrera dérmica." }
        ]
      }
    },
    {
      orden: 13,
      seccion: "Una decisión que importa (Eco/Valores) (NUEVO)",
      visual: "Grid de dos columnas: izquierda copy ecológico y concientizador del consumo de descartables en Argentina; derecha bloque de certificaciones (OEKO-TEX, Dermatest, PETA, FSC) explicadas en lenguaje simple.",
      contenido: {
        titulo: "Una decisión que importa",
        highlight: "Cuidarte no tiene por qué costarle al planeta.",
        parrafos: [
          "Cada año, una argentina promedio usa y descarta más de 900 discos de algodón. Con el Laska Mini Set, eso se convierte en cero.",
          "3 piezas. Hasta 2 años de uso. Sin residuos, sin químicos en el agua."
        ]
      }
    },
    {
      orden: 14,
      seccion: "Bloque de Compra (Producto + Precio)",
      visual: "Layout de ecommerce premium. Columna izquierda galería de fotos con miniaturas interactivas; columna derecha título, precio ($28.500 ARS), facilidades y acordeones de características.",
      contenido: {
        titulo: "Laska Mini Set (3 en 1)",
        precios: "Antes $35.000 ARS / Ahora $28.500 ARS",
        CTA: "Comprar Ahora"
      }
    },
    {
      orden: 15,
      seccion: "Preguntas Frecuentes (FAQ)",
      visual: "Acordeones desplegables interactivos con preguntas y respuestas optimizadas en voseo argentino.",
      contenido: {
        tituloH2: "Antes de comprar, resolvé tus dudas"
      }
    },
    {
      orden: 16,
      seccion: "Transparencia Corporativa",
      visual: "Tarjetas con datos fiscales, dirección de sede central, CUIT y contacto de soporte.",
      contenido: {
        titulo: "Sobre PepaGold y Greenway Global"
      }
    },
    {
      orden: 17,
      seccion: "Footer & Transparencia Legal E-E-A-T",
      visual: "Footer de tres columnas con enlaces de políticas legales, botón de arrepentimiento de Ley Argentina 24.240 y descargo científico final.",
      contenido: {
        transparenciaEEATLiteral: "* Transparencia E-E-A-T: Las referencias a investigadores y sus instituciones son informativas y enlazan a sus perfiles públicos y laboratorios verificados. Ningún experto avala comercialmente este producto. Los enlaces usan rel=\"nofollow noopener\" para cumplir con las directrices de Google sobre enlaces de terceros."
      }
    }
  ],

  caracteristicasTecnicasInteractividad: {
    smartVideoSystem: {
      comportamiento: "Script autoejecutable que monitorea mediante un IntersectionObserver los videos de Showcase y Beneficios con volumen regulable."
    },
    sliderAntesDespues: {
      comportamiento: "Controlador de tipo range input que modifica una variable CSS (--pos) en tiempo real para deslizar la máscara."
    }
  }
};

// Si se ejecuta en Node.js, imprime un resumen del informe
if (typeof require !== 'undefined' && require.main === module) {
  console.log("=====================================================================");
  console.log(`INFORME DE ESTRUCTURA Y DISEÑO - ${informeLandingPage.metadata.producto.toUpperCase()}`);
  console.log("=====================================================================");
  console.log(`Estilo: ${informeLandingPage.sistemaDiseno.estiloVisual.concepto}`);
  console.log(`Tipografía: ${informeLandingPage.sistemaDiseno.tipografia.fuenteTitulares} / ${informeLandingPage.sistemaDiseno.tipografia.fuenteCuerpoBotones}`);
  console.log("\nSecciones del Sitio (NUEVA ESTRUCTURA DE CONVERSIÓN JÓVENES):");
  informeLandingPage.estructuraSecciones.forEach(sec => {
    console.log(`  [Paso ${sec.orden}] - ${sec.seccion}`);
  });
  console.log("\nEl archivo JS ha sido guardado exitosamente en el proyecto.");
}

// Exportamos el objeto por si se desea importar en la aplicación
if (typeof module !== 'undefined') {
  module.exports = informeLandingPage;
}
