import glob

html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if '/admin/' not in f.replace('\\', '/')]

count = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'global-sync.js' not in c:
        rel = fpath.replace('\\', '/').replace('www.manujungleforever.com/', '')
        depth = len(rel.split('/')) - 1
        prefix = '../' * depth
        tag = f'<script src="{prefix}assets/js/global-sync.js" defer></script>'
        c = c.replace('</body>', tag + '\n</body>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        count += 1

print(f'Injected global-sync.js into {count} HTML files.')
