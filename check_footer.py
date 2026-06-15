import os

with open('www.hiddenjunglecusco.com/3-day-wildlife-quest-machu-wasi/index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

target = '<div class="cx">\n  <div class="fg">'
idx = c.find(target)
print('Target index:', idx)
if idx >= 0:
    before = c[:idx]
    last_style = before.rfind('<style>')
    print('Last <style> tag at:', last_style)
    print(c[last_style:last_style+300])
