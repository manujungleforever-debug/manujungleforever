import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# The block to remove:
hero_regex = r'<!-- HERO -->\s*<section class="in-hero"[^>]*>.*?<\/section>'
html = re.sub(hero_regex, '', html, flags=re.DOTALL)

# The duplicate title to replace:
old_title_regex = r'<div style="text-align:center; padding: 60px 0;"><span class="ey">Manu Jungle Forever</span><h1 class="h1" style="font-size:clamp\(2\.5rem,6vw,4\.5rem\)">Complaints Book</h1></div>'

new_title = '''<!-- HEADER CLEAN (SIN IMAGEN DE SELVA) -->
<div style="text-align:center; padding: 140px 0 60px 0;">
    <span class="ey emerald-title" style="font-size:14px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#10b981;">— MANU JUNGLE FOREVER</span>
    <h1 class="h1 white-title" style="font-size:clamp(2.5rem,6vw,4.5rem); margin-top:8px; margin-bottom:16px; color:#fff;">Complaints Book</h1>
    <p class="hs" style="margin:0 auto 30px auto; color:rgba(255,255,255,0.7); max-width:600px;">In accordance with the Consumer Protection Code, Law N° 29571.</p>
    <img src="../assets/img/libro_reclamaciones.png" alt="Complaints Book" style="max-height: 200px; width: 100%; object-fit: contain; margin: 0 auto;">
</div>'''

html = re.sub(old_title_regex, new_title, html, flags=re.DOTALL)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
