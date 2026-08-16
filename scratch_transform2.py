import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Replace .in-hero
html = re.sub(
    r'<section class="in-hero".*?</section>',
    r'<div style="text-align:center; padding: 60px 0;"><span class="ey">Manu Jungle Forever</span><h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">Complaints Book</h1></div>',
    html,
    flags=re.DOTALL
)

# Remove reclamo-wrapper
html = html.replace('<div class="reclamo-wrapper">', '')

# Remove an extra closing div since we removed reclamo-wrapper
html = html.replace('</div>\n</section>\n</main>', '</section>\n</main>')

# Replace business info box
html = html.replace('<div class="reclamo-box">', '<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:24px; padding:40px; margin-bottom: 24px;">')
html = html.replace('<h3 class="reclamo-subtitle">', '<h2 class="h2" style="margin-bottom:8px; font-size:1.8rem;">')
html = html.replace('<p class="reclamo-desc">', '<p style="font-size:.87rem;color:rgba(255,255,255,.55);margin-bottom:8px;">')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
print('Done')
