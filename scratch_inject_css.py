import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

css_block = '''<style>
.sec, main, .in-hero {
  padding-top: 140px !important;
}
header, .site-header, .in-hero {
  background-color: #060b13 !important;
  background-image: none !important;
}
.in-hero::before, .in-hero::after {
  display: none !important;
}
</style>'''

# Replace existing <style> tag if present, else insert before </head>
if '<style>' in html:
    html = re.sub(r'<style>.*?</style>', css_block, html, flags=re.DOTALL)
else:
    html = html.replace('</head>', css_block + '\n</head>')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
