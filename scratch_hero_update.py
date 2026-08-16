import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Replace the style block and header CSS
style_update = '''
<style>
  body, main, section { background-color: #060b18 !important; background-image: none !important; }
  *::before, *::after { background-image: none !important; }
  
  /* UNIFICACIÓN DEL HEADER / NAVBAR */
  header, #N, .site-header, .hdr { 
    background: transparent !important; 
    background-color: #060b18 !important; 
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  }
  header::before, header::after, #N::before, #N::after { 
    display: none !important; 
    background: none !important; 
  }
  
  /* REESTRUCTURACIÓN DEL HERO */
  .in-hero-custom { 
    padding-top: 180px !important; 
    padding-bottom: 60px !important;
    background: transparent !important; 
    text-align: center;
    position: relative;
    z-index: 10;
  }
  
  /* Inputs dark styling */
  input, select, textarea {
    background: #111827 !important; 
    color: #ffffff !important; 
    border: 1px solid #374151 !important;
  }
</style>
'''
html = re.sub(r'<style>.*?</style>', style_update, html, flags=re.DOTALL)

# Replace the hero block with the new structured one
new_hero = '''
<!-- NUEVO HERO ESTRUCTURADO COMO /CONTACT/ -->
<section class="in-hero-custom">
  <div class="cx">
    <span class="ey" style="color:var(--a);">Manu Jungle Forever</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem); color:#fff; margin-top:8px; margin-bottom:16px;">Complaints Book</h1>
    <p class="hs" style="margin:0 auto 30px auto; color:rgba(255,255,255,0.7); max-width:600px;">In accordance with the Consumer Protection Code, Law N° 29571.</p>
    <img src="../assets/img/libro_reclamaciones.png" alt="Complaints Book" style="max-height: 200px; width: 100%; object-fit: contain; margin: 0 auto;">
  </div>
</section>
'''

# We need to remove the old title container and the policy-card from the HTML
# Old title container: <div class="title-container">...</div>
html = re.sub(r'<div class="title-container">.*?</div>', '', html, flags=re.DOTALL)

# Old policy card: <div class="policy-card" ...>...</div>
html = re.sub(r'<div class="policy-card".*?</div>', '', html, flags=re.DOTALL)

# Inject the new hero at the top of <main>
html = html.replace('<main id="main" style="background-color: #060b18 !important; background-image: none !important;">', 
                    '<main id="main" style="background-color: #060b18 !important; background-image: none !important;">\n' + new_hero)

# Ensure section titles are emerald green (var(--a))
html = html.replace('<h4>1. Consumer Details</h4>', '<h2 class="h2" style="margin-bottom:24px; font-size:1.4rem; color:var(--a);">1. Consumer Details</h2>')
html = html.replace('<h4>2. Contracted Good / Service</h4>', '<h2 class="h2" style="margin-bottom:24px; font-size:1.4rem; color:var(--a);">2. Contracted Good / Service</h2>')
html = html.replace('<h4>3. Complaint Details</h4>', '<h2 class="h2" style="margin-bottom:24px; font-size:1.4rem; color:var(--a);">3. Complaint Details</h2>')

# Business Information title should be green too
html = html.replace('<h2 class="h2" style="margin-bottom:8px; font-size:1.8rem;">Business Information</h3>', '<h2 class="h2" style="margin-bottom:16px; font-size:1.4rem; color:var(--a);">Business Information</h2>')

# Remove duplicate <h2> Business info if any
html = html.replace('<h2 class="h2" style="margin-bottom:8px; font-size:1.8rem;">Business Information</h2>', '<h2 class="h2" style="margin-bottom:16px; font-size:1.4rem; color:var(--a);">Business Information</h2>')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
