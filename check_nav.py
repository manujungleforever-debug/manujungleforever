with open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()
idx = c.find('<nav class="nm"')
if idx > 0:
    print(c[idx:idx+1500])
