with open('www.hiddenjunglecusco.com/3-day-wildlife-quest-machu-wasi/index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()
end_idx = c.find('</div></footer>')
cx_idx = c.rfind('<div class="cx">', 0, end_idx)
print(c[cx_idx:end_idx+200])
