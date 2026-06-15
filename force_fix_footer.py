import os, re

ROOT = 'www.hiddenjunglecusco.com'

from fix_layout_and_nav import get_new_footer

updated = 0
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if not fname.endswith('.html') or fname == 'original_raw.html': continue
        
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
            
        rel = '../' * (len(os.path.relpath(fpath, ROOT).split(os.sep)) - 1)
        if rel == '': rel = './'
        if rel == './' and dirpath == ROOT: rel = ''
        
        new_footer = get_new_footer(rel)
        
        # Method 1: standard match
        new_c = re.sub(r'<footer class="ft">.*?</footer>', new_footer, c, flags=re.DOTALL)
        
        # Method 2: if <footer class="ft"> is missing, find the block containing the logo and ending with </footer>
        if new_c == c:
            # Look for an optional footer tag, then something containing the logo, up to </footer>
            pattern = r'(?:<footer[^>]*>)?\s*(?:<style>.*?</style>)?\s*<div class="cx">\s*<div class="fg">.*?HiddenJungleCusco_Logo_TextSeal_3Color\.png.*?</footer>'
            new_c2 = re.sub(pattern, new_footer, c, flags=re.DOTALL)
            if new_c2 != c:
                new_c = new_c2

        if new_c != c:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_c)
            updated += 1

print(f"Force-updated footer in {updated} files.")
