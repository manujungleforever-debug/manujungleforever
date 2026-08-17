import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

css_block = '''<style>
.in-hero, .sec-hero, section:first-of-type {
  background: radial-gradient(circle at center, rgba(5, 25, 20, 0.85) 0%, rgba(6, 11, 19, 1) 100%) !important;
}
</style>'''

html = html.replace('</head>', css_block + '\n</head>')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
