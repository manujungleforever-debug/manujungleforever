import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# The current section tag is:
# <section class="relative pt-32 pb-12 flex flex-col items-center justify-center text-center bg-transparent" style="width: 100%; padding-top: 140px; padding-bottom: 40px;">
old_section = r'<section class="relative pt-32 pb-12 flex flex-col items-center justify-center text-center bg-transparent"[^>]*>'
new_section = '''<section class="in-hero relative flex flex-col items-center justify-center text-center" style="width: 100%; padding-top: 140px; padding-bottom: 40px; background-image: url('../assets/img/hero.png'); background-position: center; background-size: cover;">'''

html = re.sub(old_section, new_section, html)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
