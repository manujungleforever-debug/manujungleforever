import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Update style block with explicit colors
style_update = '''
<style>
  body, main, section { background-color: #060b13 !important; background-image: none !important; }
  *::before, *::after { background-image: none !important; }
  
  /* HEADER */
  header, #N, .site-header, .hdr { 
    background: transparent !important; 
    background-color: #060b13 !important; 
    border-bottom: 1px solid #1e293b !important;
  }
  header::before, header::after, #N::before, #N::after { 
    display: none !important; 
    background: none !important; 
  }
  
  /* HERO */
  .in-hero-custom { 
    padding-top: 140px !important; 
    padding-bottom: 60px !important;
    background: transparent !important; 
    text-align: center;
    position: relative;
    z-index: 10;
  }
  
  /* CARDS */
  .form-card {
    background-color: #0b1019 !important; 
    border: 1px solid #1e293b !important; 
    border-radius: 24px; 
    padding: 40px; 
    margin-bottom: 24px;
  }

  /* INPUTS */
  input, select, textarea {
    background: #0b1019 !important; 
    color: #ffffff !important; 
    border: 1px solid #1e293b !important;
  }
  input::placeholder, textarea::placeholder {
    color: #94a3b8 !important;
  }

  /* TITLES */
  .emerald-title {
    color: #10b981 !important;
  }
  .white-title {
    color: #ffffff !important;
  }
</style>
'''
html = re.sub(r'<style>.*?</style>', style_update, html, flags=re.DOTALL)

# Update hero
hero_new = '''
<!-- HERO -->
<section class="in-hero-custom">
  <div class="cx">
    <span class="ey emerald-title" style="font-size:14px; font-weight:700; letter-spacing:2px; text-transform:uppercase;">— MANU JUNGLE FOREVER</span>
    <h1 class="h1 white-title" style="font-size:clamp(2.5rem,6vw,4.5rem); margin-top:8px; margin-bottom:16px;">Complaints Book</h1>
    <p class="hs" style="margin:0 auto 30px auto; color:rgba(255,255,255,0.7); max-width:600px;">In accordance with the Consumer Protection Code, Law N° 29571.</p>
    <img src="../assets/img/libro_reclamaciones.png" alt="Complaints Book" style="max-height: 200px; width: 100%; object-fit: contain; margin: 0 auto;">
  </div>
</section>
'''
html = re.sub(r'<!-- NUEVO HERO ESTRUCTURADO COMO /CONTACT/ -->.*?</section>', hero_new, html, flags=re.DOTALL)

# Update <main> and <section class="sec"> inline styles to #060b13
html = re.sub(r'<main id="main" style="background-color: #060b18 !important; background-image: none !important;">', '<main id="main" style="background-color: #060b13 !important; background-image: none !important;">', html)
html = re.sub(r'<section class="sec" style="background-color: #060b18 !important; background-image: none !important;">', '<section class="sec" style="background-color: #060b13 !important; background-image: none !important;">', html)

# Replace all old card background inline styles
html = html.replace('background-color: #0b111e !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius:24px; padding:40px; margin-bottom: 24px;', 'background-color: #0b1019 !important; border: 1px solid #1e293b !important; border-radius:24px; padding:40px; margin-bottom: 24px;')

# Replace old section titles var(--a) with literal emerald #10b981
html = html.replace('color:var(--a);', 'color:#10b981;')
html = html.replace('var(--a)', '#10b981')

# Replace old border-color transitions var(--a)
html = html.replace('borderColor=\'var(--a)\'', 'borderColor=\'#10b981\'')
html = html.replace('borderColor=\'rgba(255,255,255,0.08)\'', 'borderColor=\'#1e293b\'')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
