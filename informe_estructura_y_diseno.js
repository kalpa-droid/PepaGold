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
    version: "3.3 (Optimización de Conversión para Jóvenes)",
    fechaInforme: "30 de Junio, 2026",
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
        titularH1: "Desmaquillate solo con agua",
        subhead: "Fresh and radiant skin every day / Piel fresca y radiante cada día",
        descripcion: "3 accesorios reutilizables que limpian tu rostro, cuello y escote sin químicos, sin irritar y sin gastar de más. Mojás, deslizás y listo. Piel limpia, suave y radiante por solo $28.500 ARS.",
        CTA: "COMPRAR AHORA →",
        badgeGarantia: "4.9 / 5 (+20.000 reviews globales)"
      }
    },
    {
      orden: 3,
      seccion: "Agitación del Dolor (Pain Agitation)",
      visual: "Fondo arena cálida (#FAF6F5). Formato de 3 tarjetas alineadas en zigzag vertical con videos interactivos y bordes redondeados.",
      contenido: {
        pretitulo: "✨ El Problema",
        tituloH2: "El costo oculto de limpiar tu rostro",
        tarjetas: [
          {
            titulo: "¿Harta de gastar de más cada mes?",
            descripcion: "Discos de algodón, toallitas desechables, desmaquillantes líquidos… cada mes sumás gastos que se van a la basura.",
            metrica: "Gasto Innecesario"
          },
          {
            titulo: "¿Tu piel queda roja e irritada al desmaquillarte?",
            descripcion: "Los químicos agresivos de los desmaquillantes irritan tu barrera cutánea, dejándote la piel seca y sensible.",
            metrica: "Piel Seca e Irritada"
          },
          {
            titulo: "¿Tu rutina nocturna tiene mil pasos?",
            descripcion: "Toallita, agua micelar, algodón, enjuague, crema… Demasiados pasos que consumen tu tiempo y energía.",
            metrica: "Tiempo Perdido"
          }
        ]
      }
    },
    {
      orden: 4,
      seccion: "Beneficios Rápidos (Slider Antes/Después)",
      visual: "Grid de 2 columnas de texto de beneficios con el slider central Antes/Después de la piel.",
      contenido: {
        tag: "Laska Mini Set",
        titulo: "Limpieza profunda y consciente",
        detalles: ["Limpieza sin químicos", "Microfibra UpPoly", "Suave con tu piel", "Ecológico y duradero"]
      }
    },
    {
      orden: 5,
      seccion: "Video Showcase (3 Productos CARE)",
      visual: "Video horizontal 16:9 de unboxing. Abajo, las 3 tarjetas de producto simplificadas con imágenes de producto oficiales pegadas al lado de la información.",
      contenido: {
        pretitulo: "Laska Mini Set",
        tituloH2: "3 productos CARE en una sola caja",
        descripcionGeneral: "Máxima practicidad. Todo lo que tu piel necesita cabe en tu bolso para llevarlo a cualquier lugar. Limpia, exfolia y desmaquilla usando solo agua.",
        productosDetallados: [
          {
            nombre: "CARE 4: Cleanser Sponge",
            imagen: "4.webp",
            desc: "Esponja Desmaquillante — Mojala, pasala por tu cara y listo. Atrapa todo el maquillaje (sí, hasta el waterproof) sin líquidos ni químicos."
          },
          {
            nombre: "CARE 15: Manopla-Esponja de Doble Cara",
            imagen: "3.webp",
            desc: "Guante 2 en 1 — Un lado limpia con suavidad, el otro exfolia y activa la circulación. Para cara, cuello y cuerpo. Tu mini spa de todos los días."
          },
          {
            nombre: "CARE 6: Soft Mitt",
            imagen: "2.webp",
            desc: "Manopla Ultra Suave — Diseñada para las zonas más delicadas (cara, cuello, escote). Limpia sin frotar, sin irritar y sin productos extra."
          }
        ]
      }
    },
    {
      orden: 6,
      seccion: "Opiniones de nuestras clientas (Reviews)",
      visual: "Slider infinito de tarjetas animadas de reviews en formato vertical. Al posar el mouse, se despliega el texto de review larga. Micro-CTA al final del bloque con estrellas de calificación.",
      contenido: {
        tituloH2: "Opiniones de nuestras clientas",
        reviewsPrincipales: [
          { autor: "Sofía M.", text: "Me saca hasta el rímel waterproof, juro." },
          { autor: "lau.viajera", text: "Lo llevo a todos lados, literal." },
          { autor: "ele.skincare", text: "Me hago spa en la ducha todos los días." }
        ],
        CTA: "COMPRAR AHORA →",
        reviewsGlobales: "4.9 / 5 de más de 20.000 valoraciones alrededor del mundo"
      }
    },
    {
      orden: 7,
      seccion: "Prueba Experimental UGC (Contenido de Clientes)",
      visual: "Sección con videos cortos en proporción 9:16 tipo TikTok de clientas reales usando las fibras.",
      contenido: {
        tag: "Prueba Experimental · Experiencia Real",
        tituloH2: "Unboxing & Uso Cotidiano",
        descripcion: "Así se ve la remoción de maquillaje sin químicos en la vida real. Contenido sin filtros de clientas verificadas experimentando la tecnología UpPoly por primera vez."
      }
    },
    {
      orden: 8,
      seccion: "CTA Intermedio",
      visual: "Banda con fondo arena, gran botón de compra e información de garantías.",
      contenido: {
        botonText: "COMPRAR AHORA →",
        subtext: "Envío disponible · Pago seguro · Devolución garantizada"
      }
    },
    {
      orden: 9,
      seccion: "Beneficios a Largo Plazo (Videos CARE)",
      visual: "Tres grandes bloques con videos horizontales (16:9) autoejecutables con Smart Video System.",
      contenido: {
        tituloH2: "Beneficios a Largo Plazo",
        bloques: [
          {
            producto: "CARE 4",
            tituloH3: "Tu Escudo Protector Anti-Químicos",
            intro: "¿Piel tirante o colorada al desmaquillarte? Es tu cara gritando que los limpiadores químicos le hacen mal.",
            listaBeneficios: [
              "Chau irritación: Solo agua tibia. Decile adiós a la sequedad y tirantez.",
              "Tus defensas intactas: Sin jabones agresivos que barren con el microbioma natural.",
              "Piel sana siempre: Con el uso continuo, tu barrera cutánea se recupera."
            ]
          },
          {
            producto: "CARE 15",
            tituloH3: "Renovación Celular y Efecto 'Glow' Constante",
            intro: "¿Piel opaca y sin vida? Los exfoliantes químicos pueden ser muy agresivos. CARE 15 es la alternativa física y suave para renovar tu piel.",
            listaBeneficios: [
              "Efecto glow al instante: Su lado exfoliante barre células muertas.",
              "Masaje tonificante: Estimula la circulación, ayudando a que tu rostro se vea más firme.",
              "Tu mini spa en casa: Una rutina relajante de dos minutos en la ducha."
            ]
          },
          {
            producto: "CARE 6",
            tituloH3: "Firmeza y Prevención para Zonas Delicadas",
            intro: "El cuello y el escote también necesitan amor. Son las zonas más finas de la piel y las primeras en mostrar líneas de expresión por deshidratación.",
            listaBeneficios: [
              "Cuidado ultra delicado: Textura extrasuave diseñada para limpiar sin estirar.",
              "Adiós impurezas: Retira sudor, contaminación y protector solar sin jabón.",
              "Textura uniforme: Lográ un cuello y escote suaves y parejos."
            ]
          }
        ]
      }
    },
    {
      orden: 10,
      seccion: "El Respaldo de la Ciencia Global (E-E-A-T)",
      visual: "Grid de 4 tarjetas con especialistas en dermatología y links a laboratorios universitarios.",
      contenido: {
        tituloH2: "El Respaldo de la Ciencia Global",
        descripcionHeader: "La tecnología UpPoly elimina la necesidad de usar productos químicos agresivos. Limpia en profundidad sin tapar poros, sin irritar y sin resecar. Un método probado por dermatólogos e investigadores de las mejores universidades del mundo.",
        expertos: ["Dr. Richard Gallo (UCSD)", "Prof. Kenji Kabashima (Kyoto)", "Dra. María Eugenia Santillán (Argentina)", "Dra. T. A. Belousova (Rusia)"]
      }
    },
    {
      orden: 11,
      seccion: "Avales & Certificaciones",
      visual: "Logos de OEKO-TEX, PETA (Cruelty Free), Dermatest y FSC organizados en acordeones interactivos.",
      contenido: {
        titulo: "Certificaciones y Respaldo Global"
      }
    },
    {
      orden: 12,
      seccion: "Bloque de Compra (Producto + Precio)",
      visual: "Layout de ecommerce premium. Columna izquierda galería de fotos ampliables; columna derecha título, precio rebajado ($28.500 ARS), facilidades, botón grande y acordeones de características.",
      contenido: {
        titulo: "Laska Mini Set (3 en 1)",
        precios: "Antes $35.000 ARS / Ahora $28.500 ARS",
        CTA: "Comprar Ahora"
      }
    },
    {
      orden: 13,
      seccion: "Preguntas Frecuentes (FAQ)",
      visual: "Acordeones desplegables con preguntas de cuidado de la piel y durabilidad.",
      contenido: {
        tituloH2: "Antes de comprar, resolvé tus dudas"
      }
    },
    {
      orden: 14,
      seccion: "Transparencia Corporativa",
      visual: "Tarjetas con datos fiscales, dirección, email y WhatsApp de soporte.",
      contenido: {
        titulo: "Sobre PepaGold y Greenway Global"
      }
    },
    {
      orden: 15,
      seccion: "Footer & Transparencia Legal E-E-A-T",
      visual: "Footer oscuro. Al final absoluto, el descargo legal E-E-A-T.",
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
      comportamiento: "Controlador deslizante de tipo range input que modifica una variable CSS (--pos) en tiempo real."
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
