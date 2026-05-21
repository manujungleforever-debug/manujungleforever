import os, re, sys
from bs4 import BeautifulSoup
import urllib.request
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'www.hiddenjunglecusco.com'
ZIP_PATH = 'hts-cache/new.zip'

NEW_FOOTER_CSS = """
/* ── Legal Footer Section ── */
.fg-legal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-top: 56px;
  padding-top: 48px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
@media(max-width: 768px) {
  .fg-legal { grid-template-columns: 1fr; }
}
.leg-col h3 { font-family: 'Outfit', sans-serif; font-size: 1.4rem; color: #fff; margin-bottom: 24px; font-weight: 600; }
.leg-links { list-style: none; padding: 0; margin: 0; }
.leg-links li { margin-bottom: 16px; }
.leg-links a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 1.05rem; display: flex; align-items: center; gap: 12px; transition: color 0.2s; }
.leg-links a:hover { color: var(--a); }
.leg-links a i { color: #4488ff; font-size: 0.9rem; }

.libro-box {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: border-color 0.3s;
  height: 100%;
  box-sizing: border-box;
}
.libro-box:hover { border-color: rgba(255,255,255,0.2); }
.libro-box p { font-size: 0.85rem; color: rgba(255,255,255,0.6); line-height: 1.6; margin: 0; }
"""

def get_legal_html(rel):
    return f"""
  <div class="fg-legal">
    <div class="leg-col">
      <h3>Soporte y Legal</h3>
      <ul class="leg-links">
        <li><a href="{rel}contact/index.html"><i class="fas fa-angle-double-right"></i> Contáctenos</a></li>
        <li><a href="{rel}faq/index.html"><i class="fas fa-angle-double-right"></i> Preguntas frecuentes</a></li>
        <li><a href="{rel}terms-and-conditions/index.html"><i class="fas fa-angle-double-right"></i> Términos y Condiciones</a></li>
        <li><a href="{rel}privacy-policy/index.html"><i class="fas fa-angle-double-right"></i> Política de privacidad</a></li>
        <li><a href="{rel}cookies-policy/index.html"><i class="fas fa-angle-double-right"></i> Política de Cookies</a></li>
      </ul>
    </div>
    <div class="leg-col">
      <a href="{rel}libro-de-reclamaciones/index.html" style="text-decoration:none; display:block;">
        <div class="libro-box">
          <div style="background:#fff; border-radius:12px; padding:20px 24px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:24px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
            <div style="color:#007bff; font-weight:800; font-size:1.15rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center;">Libro de<br>Reclamaciones</div>
            <i class="fas fa-book-open" style="color:#555; font-size:2.2rem; margin-top:12px;"></i>
          </div>
          <p>Conforme al Código de Protección y Defensa del Consumidor contamos con un Libro de Reclamaciones Virtual. Solicítalo para registrar una queja o reclamo.</p>
        </div>
      </a>
    </div>
  </div>
"""

# ==========================================
# 1. FIX WILDLIFE TOURS FROM CUSCO
# ==========================================
w_path = os.path.join(ROOT, 'wildlife-tours-from-cusco', 'index.html')
with open(w_path, 'r', encoding='utf-8', errors='replace') as f:
    w_content = f.read()

# Replace "Day-by-Day Itinerary" heading with "Frequently Asked Questions"
w_content = w_content.replace('>Day-by-Day Itinerary</h2>', '>Frequently Asked Questions</h2>')
w_content = w_content.replace('>The Journey Plan</span>', '>Information</span>')

# Remove day badges from accordion buttons
w_content = re.sub(r'<span class="day-badge">Day \d+</span>\s*', '', w_content)

# We will extract the accordion content for the standalone FAQ page
soup = BeautifulSoup(w_content, 'html.parser')
accordion_items = soup.select('.itinerary-card')

faq_accordion_html = ""
for item in accordion_items:
    btn = item.select_one('.itinerary-toggle')
    if not btn: continue
    title = btn.select_one('.day-title').get_text(strip=True)
    content_div = item.select_one('.itinerary-content')
    content_html = content_div.decode_contents().strip()
    
    faq_accordion_html += f"""
    <div class="itinerary-card">
      <button class="itinerary-toggle" onclick="toggleAccordion(this)">
        <span class="day-title">{title}</span>
        <i class="fas fa-chevron-down"></i>
      </button>
      <div class="itinerary-content">
        {content_html}
      </div>
    </div>
    """

with open(w_path, 'w', encoding='utf-8') as f:
    f.write(w_content)
print("✅ wildlife-tours-from-cusco FAQ fixed.")

# ==========================================
# 2. CREATE NEW PAGES
# ==========================================
def create_page(folder, title, content_html, is_faq=False):
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    fpath = os.path.join(ROOT, folder, 'index.html')
    
    # Base layout from contact page script
    from build_contact import HEADER
    
    rel = '../'
    
    # Custom hero section
    bg_img = f"{rel}wp-content/uploads/2022/10/Hero-wildlife-cuest-6-dyas-reserved-zone.jpg"
    
    if is_faq:
        # Wrap accordion in list
        body = f"""
<main id="main">
<section class="in-hero" style="background-image: url('{bg_img}');">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">Frequently Asked Questions</h1>
  </div>
</section>
<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div style="max-width:800px; margin:0 auto;">
      <div class="itinerary-list">
        {content_html}
      </div>
    </div>
  </div>
</section>
</main>
"""
    else:
        body = f"""
<main id="main">
<section class="in-hero" style="background-image: url('{bg_img}'); padding:140px 0 80px;">
  <div class="cx">
    <h1 class="h1" style="font-size:clamp(2rem,4vw,3.5rem)">{title}</h1>
  </div>
</section>
<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div style="max-width:800px; margin:0 auto; color:rgba(255,255,255,0.75); line-height:1.8; font-size:1.05rem;">
      {content_html}
    </div>
  </div>
</section>
</main>
"""

    # Fix canonical in header
    h = HEADER.replace('https://www.hiddenjunglecusco.com/contact/', f'https://www.hiddenjunglecusco.com/{folder}/')
    h = h.replace('<title>Contact –', f'<title>{title} –')
    # Remove active class from nav
    h = h.replace('class="nb on"', 'class="nb"')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(h)
        f.write(body)
        # We will let the footer injection script handle the footer!
        f.write("</body></html>")

print("Creating standalone pages...")
create_page('faq', 'Frequently Asked Questions', faq_accordion_html, is_faq=True)
create_page('privacy-policy', 'Política de Privacidad', "<h2 class='h2'>Privacy Policy</h2><p>Our privacy policy outlines how we protect and use your data when booking trips with Hidden Jungle Cusco.</p>")
create_page('terms-and-conditions', 'Términos y Condiciones', "<h2 class='h2'>Terms & Conditions</h2><p>Standard terms and conditions for booking, cancellations, and jungle tours.</p>")
create_page('cookies-policy', 'Política de Cookies', "<h2 class='h2'>Cookie Policy</h2><p>Information about how we use cookies on this website.</p>")
create_page('libro-de-reclamaciones', 'Libro de Reclamaciones', """
<h2 class="h2">Libro de Reclamaciones</h2>
<p>Conforme al Código de Protección y Defensa del Consumidor, contamos con un Libro de Reclamaciones a su disposición.</p>
<div style="background:rgba(255,255,255,0.02); padding:30px; border-radius:12px; margin-top:30px; border:1px solid rgba(255,255,255,0.1);">
  <p><strong>Razón Social:</strong> Hidden Jungle Cusco E.I.R.L.</p>
  <p><strong>RUC:</strong> 20000000000 (Ejemplo)</p>
  <p><strong>Dirección:</strong> Nuevo Eden, Manu, Peru</p>
  <div style="margin-top:30px;">
    <a href="mailto:discover@hiddenjunglecusco.com" class="btn ba">Solicitar Formulario Virtual de Reclamo</a>
  </div>
</div>
""")

# ==========================================
# 3. UPDATE ALL FOOTERS
# ==========================================
print("\nUpdating global footers...")
updated = 0
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if not fname.endswith('.html') or fname == 'original_raw.html': continue
        
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
            
        rel = '../' * (len(os.path.relpath(fpath, ROOT).split(os.sep)) - 1)
        if rel == '': rel = './'
        if rel == './' and dirpath == ROOT: rel = ''
        
        changed = False
        
        # Inject CSS
        if '/* ── Legal Footer Section ── */' not in c:
            head_end = c.find('</head>')
            style_end = c.rfind('</style>', 0, head_end) if head_end > 0 else -1
            if style_end > 0:
                c = c[:style_end] + NEW_FOOTER_CSS + '\n' + c[style_end:]
                changed = True
        
        # We need to insert the Legal section INSIDE the <footer class="ft"><div class="cx"> right after <div class="fg">...</div>
        if '<div class="fg-legal">' not in c:
            # Find the closing tag of <div class="fg">
            # Using regex to find the end of the fg div block, or simply finding '<div class="fb">' which follows it
            fb_idx = c.find('<div class="fb">')
            if fb_idx > 0:
                legal_html = get_legal_html(rel)
                c = c[:fb_idx] + legal_html + '\n  ' + c[fb_idx:]
                changed = True
                
        # If the page didn't have a footer (like the newly created ones), we need to append the full footer
        if '<footer class="ft">' not in c:
            # Extract full footer from contact page
            from build_contact import OUT_FILE as contact_file
            with open(contact_file, 'r', encoding='utf-8') as conf:
                con_c = conf.read()
                footer_match = re.search(r'<footer class="ft">.*?</script>', con_c, re.DOTALL)
                if footer_match:
                    full_foot = footer_match.group(0)
                    # Replace relative links
                    full_foot = full_foot.replace('../', rel)
                    # Insert before </body>
                    body_close = c.rfind('</body>')
                    if body_close > 0:
                        c = c[:body_close] + '\n' + full_foot + '\n' + c[body_close:]
                        changed = True

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)
            updated += 1

print(f"✅ Updated {updated} files with the new legal footer.")
