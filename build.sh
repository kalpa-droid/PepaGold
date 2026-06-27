#!/bin/bash
# Script para ensamblar index.html desde el original PepaGold.html
# Reorganiza las secciones según la estructura de conversión CRO

ORIG="/home/mappo/Kalpagrafica/PepaGold/PepaGold.html"
OUT="/home/mappo/Kalpagrafica/PepaGold/index.html"

cat > "$OUT" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laska Mini Set | Limpieza facial sin químicos — Greenway</title>
    <meta name="description" content="Set reutilizable de microfibra UpPoly para limpiar rostro, cuello y escote solo con agua. Sin químicos. Dura hasta 2 años.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      html { scroll-behavior: smooth; }
      body { font-family: 'Poppins', sans-serif; color: #2A2523; background: #fff; -webkit-font-smoothing: antialiased; }
      img { max-width: 100%; height: auto; }
    </style>
</head>
<body>
HTMLEOF

# SECTION 1: Top Banner (lines 431-625)
sed -n '431,625p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 2: Hero Banner (lines 1-429)
sed -n '1,429p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 3: NEW - Pain Agitation
cat >> "$OUT" << 'PAINEOF'
<!-- =============================================
     SECCIÓN 3: AGITACIÓN DEL DOLOR (NUEVO)
============================================= -->
<section class="pain-agitation-section">
  <div class="pain-container">
    <div class="pain-card">
      <div class="pain-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" stroke="#FF6699" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="12" r="4" stroke="#FF6699" stroke-width="1.5"/></svg>
      </div>
      <h3>¿Cansada de gastar una fortuna?</h3>
      <p>Discos de algodón, toallitas desechables, desmaquillantes líquidos… cada mes sumás gastos que se van a la basura.</p>
    </div>
    <div class="pain-card">
      <div class="pain-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" stroke="#FF6699" stroke-width="1.5"/><path d="M8 15s1.5-2 4-2 4 2 4 2M9 9h.01M15 9h.01" stroke="#FF6699" stroke-width="1.5" stroke-linecap="round"/></svg>
      </div>
      <h3>¿Rojeces y tirantez constantes?</h3>
      <p>Los químicos agresivos de los desmaquillantes irritan tu barrera cutánea, dejándote la piel seca y sensible.</p>
    </div>
    <div class="pain-card">
      <div class="pain-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="#FF6699" stroke-width="1.5"/><path d="M12 6v6l4 2" stroke="#FF6699" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h3>¿Tu rutina de noche es eterna?</h3>
      <p>Toallita, agua micelar, algodón, enjuague, crema… Demasiados pasos que consumen tu tiempo y energía.</p>
    </div>
  </div>
</section>

<style>
.pain-agitation-section { background: #ffffff; padding: 90px 20px 70px; text-align: center; }
.pain-container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.pain-card { padding: 40px 30px; border-radius: 20px; background: #FDF9F9; border: 1px solid rgba(255, 102, 153, 0.1); transition: all 0.4s ease; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }
.pain-card:hover { transform: translateY(-6px); box-shadow: 0 15px 40px rgba(255, 102, 153, 0.12); border-color: rgba(255, 102, 153, 0.25); }
.pain-icon { width: 60px; height: 60px; margin: 0 auto 25px; display: flex; align-items: center; justify-content: center; background: rgba(255, 102, 153, 0.08); border-radius: 50%; padding: 14px; animation: painPulse 3s ease-in-out infinite; }
.pain-icon svg { width: 100%; height: 100%; }
@keyframes painPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }
.pain-card h3 { font-family: Georgia, "Times New Roman", serif; font-size: clamp(1.3rem, 2vw, 1.6rem); font-weight: 400; color: #2A2523; margin-bottom: 12px; line-height: 1.3; }
.pain-card p { font-family: 'Poppins', sans-serif; font-size: 0.95rem; line-height: 1.7; color: #666; font-weight: 300; }
@media (max-width: 900px) { .pain-agitation-section { padding: 60px 20px 50px; } .pain-container { grid-template-columns: 1fr; gap: 25px; max-width: 500px; } }
</style>
PAINEOF

echo "" >> "$OUT"

# SECTION 4: Benefits V2 (lines 627-1034)
sed -n '627,1034p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 5: Comparison (lines 1864-2030)
sed -n '1864,2030p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 6: Video Showcase (lines 2032-2291)
sed -n '2032,2291p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 7a: Science Section - extract just the section, CSS, and JS (cleaned)
# CSS (skip :root, body, duplicate grain/benefits styles)
cat >> "$OUT" << 'SCIHEADEOF'
<!-- =============================================
     SECCIÓN 7a: CIENCIA A NIVEL MICROSCÓPICO
============================================= -->
<style>
SCIHEADEOF

# Extract science-specific CSS
sed -n '3370,3668p' "$ORIG" >> "$OUT"

cat >> "$OUT" << 'SCIHTML1'
</style>
SCIHTML1

# Section HTML (cleaned - no DOCTYPE/html/head/body)
sed -n '3672,3807p' "$ORIG" >> "$OUT"

# Script
sed -n '3809,3866p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 7b: Hotspots - extract just the section, CSS, and JS (cleaned)
cat >> "$OUT" << 'HOTHEAD'
<!-- =============================================
     SECCIÓN 7b: BENEFICIOS A LARGO PLAZO (HOTSPOTS)
============================================= -->
<style>
HOTHEAD

# Extract hotspot-specific CSS (skip :root, body, duplicates)
sed -n '2968,3165p' "$ORIG" >> "$OUT"

cat >> "$OUT" << 'HOTHTML1'
</style>
HOTHTML1

# Section HTML (cleaned)
sed -n '3169,3230p' "$ORIG" >> "$OUT"

# Script
sed -n '3232,3331p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION: Intermediate CTA (NEW)
cat >> "$OUT" << 'CTAEOF'
<!-- =============================================
     CTA INTERMEDIO (NUEVO)
============================================= -->
<section class="intermediate-cta-section">
  <a href="#compra-section" class="intermediate-cta-btn">COMPRAR AHORA →</a>
  <p class="intermediate-cta-sub">Envío disponible · Pago seguro · Devolución garantizada</p>
</section>

<style>
.intermediate-cta-section { background: #FDF9F9; padding: 60px 20px; text-align: center; }
.intermediate-cta-btn { display: inline-block; background: #2A2523; color: #fff; font-family: 'Poppins', sans-serif; font-weight: 600; text-decoration: none; padding: 1.3rem 3.5rem; border-radius: 60px; font-size: 1.2rem; letter-spacing: 1px; transition: all 0.4s ease; box-shadow: 0 10px 25px rgba(42,37,35,0.15); }
.intermediate-cta-btn:hover { background: #FF6699; transform: translateY(-4px); box-shadow: 0 15px 35px rgba(255, 102, 153, 0.25); }
.intermediate-cta-sub { font-family: 'Poppins', sans-serif; font-size: 0.9rem; color: #888; margin-top: 15px; font-weight: 400; }
</style>
CTAEOF

echo "" >> "$OUT"

# SECTION 8: Reviews V2 (lines 1287-1724)
sed -n '1287,1724p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 9: Product Purchase (lines 2294-2882) - add id="compra-section"
# First line needs modification
echo '<div class="custom-product-section" id="compra-section">' >> "$OUT"
sed -n '2295,2406p' "$ORIG" >> "$OUT"

# Enhanced shipping accordion content
cat >> "$OUT" << 'SHIPEOF'
          <div class="accordion-content">
            <p data-i18n="acc3_desc"><strong>📦 Envíos:</strong> Realizamos envíos a todo el país. Tu pedido será preparado en 24-48 horas hábiles y el tiempo de entrega estimado es de 3 a 7 días hábiles según tu ubicación.<br><br><strong>🔄 Devoluciones:</strong> Queremos que estés 100% satisfecha. Tenés hasta 30 días desde la recepción para solicitar una devolución si el producto presenta fallas de fábrica. Como se trata de un producto de higiene personal, el mismo debe estar sin uso para poder ser devuelto.<br><br><strong>💬 ¿Dudas?</strong> Escribinos y te ayudamos con tu compra.</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
SHIPEOF

# CSS and JS for product section
sed -n '2417,2882p' "$ORIG" >> "$OUT"

echo "" >> "$OUT"

# SECTION 10: FAQ (NEW)
cat >> "$OUT" << 'FAQEOF'
<!-- =============================================
     SECCIÓN 10: PREGUNTAS FRECUENTES (NUEVO)
============================================= -->
<section class="faq-section">
  <div class="grain-overlay-faq"></div>
  <div class="faq-container">
    <h4 class="faq-pretitle">💬 PREGUNTAS FRECUENTES</h4>
    <h2 class="faq-title">¿Tenés dudas? Te las resolvemos</h2>
    <div class="faq-accordion">
      <div class="faq-item">
        <button class="faq-btn"><span>¿Cómo se lava la fibra después de usarla?</span><span class="faq-icon">+</span></button>
        <div class="faq-content">
          <p>Después de cada uso, lavá tu producto CARE con jabón neutro (blanco) y agua tibia. Frotá suavemente con las manos, enjuagá bien y dejá secar al aire libre. No uses suavizante ni blanqueador, ya que pueden dañar las microfibras. Con este cuidado simple, mantendrás su efectividad durante toda su vida útil.</p>
        </div>
      </div>
      <div class="faq-item">
        <button class="faq-btn"><span>¿Sirve para pieles con acné o rosácea?</span><span class="faq-icon">+</span></button>
        <div class="faq-content">
          <p>¡Sí! Es justamente ideal para pieles sensibles, con acné o rosácea. Al limpiar solo con agua y sin necesidad de químicos, no irritás ni alterás tu barrera cutánea. La microfibra UpPoly trabaja de forma mecánica ultra-suave, sin agregar sustancias que puedan provocar brotes o enrojecimiento.</p>
        </div>
      </div>
      <div class="faq-item">
        <button class="faq-btn"><span>¿Realmente dura 2 años?</span><span class="faq-icon">+</span></button>
        <div class="faq-content">
          <p>Sí. Con el cuidado adecuado (lavado con jabón neutro y secado al aire), las fibras UpPoly mantienen sus propiedades de limpieza durante más de 500 lavados, lo que equivale a aproximadamente 2 años de uso diario. Esto lo convierte en una inversión que te ahorra miles de pesos en productos desechables.</p>
        </div>
      </div>
      <div class="faq-item">
        <button class="faq-btn"><span>¿Puedo usarlo con maquillaje waterproof?</span><span class="faq-icon">+</span></button>
        <div class="faq-content">
          <p>Sí. La tecnología de microfibra UpPoly captura eficazmente incluso el maquillaje de larga duración y waterproof, como máscaras de pestañas resistentes al agua. Solo necesitás humedecer la fibra con agua tibia y deslizar suavemente sobre el rostro. Sin frotar, sin irritar.</p>
        </div>
      </div>
      <div class="faq-item">
        <button class="faq-btn"><span>¿Es apto para todo tipo de piel?</span><span class="faq-icon">+</span></button>
        <div class="faq-content">
          <p>Absolutamente. El set Laska Mini es apto para pieles secas, grasas, mixtas, sensibles y maduras. Al no utilizar químicos, se adapta a cualquier tipo de piel sin causar reacciones adversas. Incluso es seguro para adolescentes que están comenzando su rutina de cuidado facial.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
.faq-section { position: relative; background: #FDF9F9; padding: 90px 20px; color: #2A2523; overflow: hidden; }
.grain-overlay-faq { position: absolute; inset: 0; z-index: 1; opacity: 0.03; pointer-events: none; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E"); }
.faq-container { position: relative; z-index: 2; max-width: 800px; margin: 0 auto; }
.faq-pretitle { font-family: 'Poppins', sans-serif; color: #FF6699; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; text-align: center; margin-bottom: 15px; }
.faq-title { font-family: Georgia, "Times New Roman", serif; font-size: clamp(2rem, 3.5vw, 3rem); font-weight: 400; text-align: center; margin-bottom: 50px; line-height: 1.2; }
.faq-accordion { border-top: 1px solid #eee; }
.faq-item { border-bottom: 1px solid #eee; }
.faq-btn { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 22px 0; background: none; border: none; font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 500; color: #2A2523; cursor: pointer; transition: color 0.3s ease; text-align: left; gap: 15px; }
.faq-btn:hover { color: #FF6699; }
.faq-icon { font-size: 1.5rem; font-weight: 400; transition: transform 0.3s ease; flex-shrink: 0; color: #FF6699; }
.faq-content { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
.faq-content p { font-family: 'Poppins', sans-serif; font-size: 1rem; color: #555; line-height: 1.8; font-weight: 300; padding-bottom: 25px; margin: 0; }
.faq-item.active .faq-content { max-height: 400px; }
.faq-item.active .faq-icon { transform: rotate(45deg); }
@media (max-width: 768px) { .faq-section { padding: 60px 20px; } .faq-btn { font-size: 1rem; } .faq-title { font-size: 2rem; margin-bottom: 35px; } }
</style>

<script>
(function() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const btn = item.querySelector('.faq-btn');
    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('active');
      faqItems.forEach(other => other.classList.remove('active'));
      if (!isOpen) item.classList.add('active');
    });
  });
})();
</script>
FAQEOF

echo "" >> "$OUT"

# SECTION 11: Footer (NEW)
cat >> "$OUT" << 'FOOTEOF'
<!-- =============================================
     SECCIÓN 11: FOOTER (NUEVO)
============================================= -->
<footer class="site-footer">
  <div class="footer-container">
    <div class="footer-brand">
      <span class="footer-logo notranslate" translate="no">GREENWAY GLOBAL</span>
      <p class="footer-tagline">Tecnología en microfibra para el cuidado de tu piel.</p>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Greenway Global. Todos los derechos reservados.</p>
    </div>
  </div>
</footer>

<style>
.site-footer { background: #2A2523; color: rgba(255,255,255,0.7); padding: 60px 20px 40px; font-family: 'Poppins', sans-serif; }
.footer-container { max-width: 1200px; margin: 0 auto; text-align: center; }
.footer-logo { font-size: 1.4rem; font-weight: 700; letter-spacing: 3px; color: #fff; display: block; margin-bottom: 10px; }
.footer-tagline { font-size: 0.95rem; font-weight: 300; color: rgba(255,255,255,0.5); margin-bottom: 40px; }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 25px; }
.footer-bottom p { font-size: 0.85rem; color: rgba(255,255,255,0.4); margin: 0; }
</style>

</body>
</html>
FOOTEOF

echo "✅ index.html generado exitosamente en $OUT"
echo "Líneas totales: $(wc -l < "$OUT")"
