import os, re

ROOT = 'www.hiddenjunglecusco.com'

pages = [
    'index.html',
    '3-day-wildlife-quest-machu-wasi/index.html',
]

for page in pages:
    fpath = os.path.join(ROOT, page)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    m = re.search(r'<nav class="nm"[^>]*>.*?</nav>', c, re.DOTALL)
    if m:
        nav = m.group(0)
        # Find all links with class="on"
        on_links = re.findall(r'<a[^>]+class="[^"]*on[^"]*"[^>]*>', nav)
        print(f'Page: {page}')
        print(f'  Links with class="on" ({len(on_links)}):')
        for lnk in on_links:
            print(f'    {lnk[:120]}')
        print()
