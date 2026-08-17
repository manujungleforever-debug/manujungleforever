import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Update the injected style block
new_style = '''<style>
.in-hero, .sec-hero {
  background-image: radial-gradient(circle at center, rgba(5, 25, 20, 0.85) 0%, rgba(6, 11, 19, 0) 100%) !important;
}
</style>'''
html = re.sub(r'<style>.*?</style>', new_style, html, flags=re.DOTALL)

# 2. Add class="in-hero" to the title div so the CSS applies exclusively to it
html = html.replace('<div style="text-align:center; padding: 140px 0 60px 0;">', '<div class="in-hero" style="text-align:center; padding: 140px 0 60px 0;">')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
