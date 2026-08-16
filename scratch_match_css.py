import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Replace the stylesheet link
html = re.sub(r'<link rel="stylesheet" href="\.\./assets/css/new\.css\?v=\d+">', '<link rel="stylesheet" href="../assets/css/new.css">', html)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
