import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'www.hiddenjunglecusco.com'

def get_base_parts():
    with open(os.path.join(ROOT, 'about-2/index.html'), 'r', encoding='utf-8') as f:
        html = f.read()
        
    head_match = re.search(r'(<!doctype html>.*?<head>.*?</style>)', html, re.DOTALL)
    head_top = head_match.group(1) if head_match else '<!doctype html><html lang="en"><head>'
    
    head_bottom_match = re.search(r'(<script>\(function\(w,d,s,l,i\).*?</head><body>)', html, re.DOTALL)
    head_bottom = head_bottom_match.group(1) if head_bottom_match else '</head><body>'
    
    header_match = re.search(r'(<!-- HJC Preloader -->.*?<main id="main">)', html, re.DOTALL)
    header_html = header_match.group(1) if header_match else '<main id="main">'
    
    footer_match = re.search(r'(</main>\s*<footer class="ft">.*</body></html>)', html, re.DOTALL)
    footer_html = footer_match.group(1) if footer_match else '</main></body></html>'
    
    return head_top, head_bottom, header_html, footer_html

head_top, head_bottom, header_html, footer_html = get_base_parts()

# Custom styles for policies and form
custom_styles = """
/* Policy & Form Styles */
.policy-card {
  background: var(--f);
  border: 1px solid rgba(255,255,255,.07);
  border-radius: 24px;
  padding: 48px;
  margin-top: -60px;
  position: relative;
  z-index: 10;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  color: rgba(255,255,255,0.75);
  line-height: 1.8;
  font-size: 1.05rem;
}
.policy-card h2 { color: #fff; margin-top: 30px; margin-bottom: 15px; font-family: 'Syne', sans-serif; }
.policy-card h3 { color: #fff; margin-top: 25px; margin-bottom: 10px; font-family: 'Syne', sans-serif; }
.policy-card ul { margin-left: 20px; margin-bottom: 20px; }
.policy-card p { margin-bottom: 15px; }

/* Libro de Reclamaciones Specific */
.reclamo-header {
  text-align: center;
  margin-bottom: 40px;
}
.reclamo-header i {
  font-size: 3rem;
  color: #00e5ff;
  text-shadow: 0 0 15px rgba(0,229,255,0.6);
  margin-bottom: 15px;
}
.reclamo-header h1 {
  font-family: 'Syne', sans-serif;
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 10px;
}
.reclamo-header h1 span { color: #00e5ff; }
.reclamo-header p {
  color: rgba(255,255,255,0.6);
  font-size: 0.9rem;
}
.reclamo-box {
  background: #11141a;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
}
.reclamo-box.glow {
  border: 1px solid rgba(0,229,255,0.2);
  box-shadow: inset 0 0 20px rgba(0,229,255,0.05);
}
.reclamo-box h3 {
  color: #fff;
  font-size: 1.2rem;
  margin-top: 0;
  margin-bottom: 10px;
}
.reclamo-box.glow h3 {
  color: #00e5ff;
}
.reclamo-box p {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.5);
  margin-bottom: 0;
}
.reclamo-form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
@media(max-width: 768px) {
  .reclamo-form-row { grid-template-columns: 1fr; }
}
.reclamo-input-group label {
  display: block;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.6);
  margin-bottom: 8px;
}
.reclamo-input-group input, .reclamo-input-group textarea, .reclamo-input-group select {
  width: 100%;
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  font-family: 'Outfit', sans-serif;
  transition: all 0.3s;
  box-sizing: border-box;
}
.reclamo-input-group input:focus, .reclamo-input-group textarea:focus, .reclamo-input-group select:focus {
  outline: none;
  border-color: #00e5ff;
  box-shadow: 0 0 0 2px rgba(0,229,255,0.2);
}
.reclamo-submit {
  background: #00e5ff;
  color: #000;
  border: none;
  padding: 14px 32px;
  font-weight: 700;
  font-family: 'Syne', sans-serif;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}
.reclamo-submit:hover {
  background: #fff;
  box-shadow: 0 0 15px rgba(0,229,255,0.5);
}
"""

def generate_page(folder, title, content_html, hero_title):
    path = os.path.join(ROOT, folder, 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Fix active state in header
    nav_html = header_html.replace('class="nb on"', 'class="nb"')
    
    hero_bg = "../wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg"
    
    main_content = f"""
<section class="in-hero" style="background-image: url('{hero_bg}'); padding:180px 0 140px;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">{hero_title}</h1>
  </div>
</section>
<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="policy-card">
      {content_html}
    </div>
  </div>
</section>
"""
    
    full_html = head_top.replace('</style>', f'\n{custom_styles}\n</style>') + head_bottom + nav_html + main_content + footer_html
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_html)


# 1. Privacy Policy
privacy_html = """
<h2>Privacy Policy</h2>
<p>Hidden Jungle Cusco is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website or book a tour with us.</p>
<h3>1. Information We Collect</h3>
<p>We collect personal information that you voluntarily provide to us when expressing an interest in obtaining information about our tours, or otherwise contacting us. This includes names, email addresses, phone numbers, and dietary requirements.</p>
<h3>2. How We Use Your Information</h3>
<p>We use the information we collect to facilitate the booking process, respond to your inquiries, ensure your safety during tours, and improve our services.</p>
<h3>3. Data Security</h3>
<p>We implement a variety of security measures to maintain the safety of your personal information. However, no method of transmission over the Internet is 100% secure.</p>
<h3>4. Contact Us</h3>
<p>If you have questions about this privacy policy, please contact us at discover@hiddenjunglecusco.com.</p>
"""
generate_page('privacy-policy', 'Privacy Policy', privacy_html, 'Privacy Policy')

# 2. Terms & Conditions
terms_html = """
<h2>Terms & Conditions</h2>
<p>Welcome to Hidden Jungle Cusco. By booking a tour with us, you agree to the following terms and conditions.</p>
<h3>1. Booking and Payments</h3>
<p>A deposit is required to secure your booking. Full payment must be completed prior to the start of the tour. We accept major credit cards and bank transfers.</p>
<h3>2. Cancellations and Refunds</h3>
<p>Cancellations made 30 days prior to the departure date will receive a full refund minus administrative fees. Cancellations made within 30 days of departure are non-refundable.</p>
<h3>3. Health and Safety</h3>
<p>Travelers must ensure they are in good health and physical condition for jungle exploration. Hidden Jungle Cusco is not liable for illnesses or injuries sustained during the tour.</p>
<h3>4. Itinerary Changes</h3>
<p>We reserve the right to alter itineraries due to weather conditions, safety concerns, or other unforeseen circumstances in the Amazon rainforest.</p>
"""
generate_page('terms-and-conditions', 'Terms & Conditions', terms_html, 'Terms & Conditions')

# 3. Cookies Policy
cookies_html = """
<h2>Cookie Policy</h2>
<p>This Cookie Policy explains how Hidden Jungle Cusco uses cookies and similar technologies to recognize you when you visit our website.</p>
<h3>1. What are cookies?</h3>
<p>Cookies are small data files that are placed on your computer or mobile device when you visit a website. They are widely used by website owners in order to make their websites work, or to work more efficiently.</p>
<h3>2. Why do we use cookies?</h3>
<p>We use first-party and third-party cookies for several reasons. Some cookies are required for technical reasons in order for our website to operate. Other cookies also enable us to track and target the interests of our users to enhance their experience.</p>
<h3>3. Analytics</h3>
<p>We use Google Analytics to help us understand how visitors engage with our website. This information is used to improve our site and tailor it to our users' needs.</p>
"""
generate_page('cookies-policy', 'Cookie Policy', cookies_html, 'Cookie Policy')

# 4. FAQ
# Extract FAQ content from existing faq file
faq_content_html = ""
with open(os.path.join(ROOT, 'faq/index.html'), 'r', encoding='utf-8') as f:
    faq_full = f.read()
    faq_match = re.search(r'<div class="itinerary-list">(.*?)</div>\s*</div>\s*</div>\s*</section>', faq_full, re.DOTALL)
    if faq_match:
        faq_content_html = f'<div class="itinerary-list">{faq_match.group(1)}</div>'
    else:
        faq_content_html = "<p>FAQs coming soon.</p>"

generate_page('faq', 'Frequently Asked Questions', faq_content_html, 'Frequently Asked Questions')

# 5. Libro de Reclamaciones
libro_html = """
<div class="reclamo-header">
  <i class="fas fa-book-open"></i>
  <h1>Libro de <span>Reclamaciones</span></h1>
  <p>Conforme a lo establecido en el Código de Protección y Defensa del Consumidor, Ley N° 29571.</p>
</div>

<div class="reclamo-box">
  <h3>Hoja de Reclamación Virtual</h3>
  <p>La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.</p>
</div>

<form>
  <div class="reclamo-box glow">
    <h3>1. Identificación del Consumidor</h3>
    <div class="reclamo-form-row">
      <div class="reclamo-input-group">
        <label>Nombres y Apellidos *</label>
        <input type="text" required>
      </div>
      <div class="reclamo-input-group">
        <label>DNI / CE / RUC *</label>
        <input type="text" required>
      </div>
    </div>
    <div class="reclamo-form-row" style="grid-template-columns: 1fr;">
      <div class="reclamo-input-group">
        <label>Domicilio *</label>
        <input type="text" required>
      </div>
    </div>
    <div class="reclamo-form-row">
      <div class="reclamo-input-group">
        <label>Teléfono *</label>
        <input type="text" required>
      </div>
      <div class="reclamo-input-group">
        <label>Correo Electrónico *</label>
        <input type="email" required>
      </div>
    </div>
  </div>

  <div class="reclamo-box glow">
    <h3>2. Detalle del Reclamo / Queja</h3>
    <div class="reclamo-form-row">
      <div class="reclamo-input-group">
        <label>Tipo *</label>
        <select required>
          <option value="">Seleccionar...</option>
          <option value="reclamo">Reclamo (Disconformidad relacionada a los productos o servicios)</option>
          <option value="queja">Queja (Disconformidad no relacionada a los productos o servicios)</option>
        </select>
      </div>
      <div class="reclamo-input-group">
        <label>Fecha de la incidencia *</label>
        <input type="date" required>
      </div>
    </div>
    <div class="reclamo-form-row" style="grid-template-columns: 1fr;">
      <div class="reclamo-input-group">
        <label>Detalle *</label>
        <textarea rows="4" required placeholder="Describa el hecho..."></textarea>
      </div>
    </div>
    <div class="reclamo-form-row" style="grid-template-columns: 1fr;">
      <div class="reclamo-input-group">
        <label>Pedido *</label>
        <textarea rows="3" required placeholder="Indique su petición..."></textarea>
      </div>
    </div>
  </div>

  <div style="text-align: right;">
    <button type="submit" class="reclamo-submit">Enviar Reclamo</button>
  </div>
</form>
"""
generate_page('libro-de-reclamaciones', 'Libro de Reclamaciones', libro_html, '') # No hero title for libro since it has custom header

print("Rebuilt policy and FAQ pages cleanly without the contact form appended.")
