import os, glob, re

base = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

filepath = os.path.join(base, "3-day-wildlife-quest-machu-wasi", "index.html")
c = open(filepath, encoding='utf-8').read()

# Find footer using different search
idx = c.lower().find('footer')
print('footer at index:', idx)
print('Context:', c[idx-10:idx+200])
