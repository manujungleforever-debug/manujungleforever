import os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'www.hiddenjunglecusco.com'

pages_old    = []
pages_no_new = []
pages_no_wa  = []

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if fname != 'index.html':
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
        if '<body' not in c or '</html>' not in c:
            continue
        rel = os.path.relpath(fpath, ROOT)
        if 'hjc_preloaded' in c:
            pages_old.append(rel)
        if 'hjc_loaded' not in c:
            pages_no_new.append(rel)
        if 'wa-wrap' not in c:
            pages_no_wa.append(rel)

print(f'OLD key still present: {len(pages_old)}')
for p in pages_old:
    print(f'  - {p}')

print(f'Missing NEW key (hjc_loaded): {len(pages_no_new)}')
for p in pages_no_new:
    print(f'  - {p}')

print(f'Missing wa-wrap: {len(pages_no_wa)}')
for p in pages_no_wa:
    print(f'  - {p}')

if not pages_old and not pages_no_new and not pages_no_wa:
    print('\nALL GOOD - Every page has the correct preloader + WA button')
else:
    print('\nISSUES FOUND - see above')
