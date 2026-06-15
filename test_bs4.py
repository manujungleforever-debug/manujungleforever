import os, sys
from bs4 import BeautifulSoup
from fix_layout_and_nav import get_new_footer

ROOT = 'www.hiddenjunglecusco.com'
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
        
        soup = BeautifulSoup(c, 'html.parser')
        
        # Method 1: Find <footer class="ft">
        footer = soup.find('footer', class_='ft')
        
        # Method 2: Find <div class="cx"> containing the logo
        if not footer:
            divs = soup.find_all('div', class_='cx')
            for d in divs:
                if 'HiddenJungleCusco_Logo_TextSeal_3Color' in str(d):
                    footer = d
                    break
        
        if footer:
            new_footer_html = get_new_footer(rel)
            new_footer_soup = BeautifulSoup(new_footer_html, 'html.parser')
            
            # Replace the old footer node with the new one
            footer.replace_with(new_footer_soup)
            
            new_c = str(soup)
            # BS4 sometimes messes up doctype or adds html/body tags where not wanted, but html.parser usually preserves it ok.
            # Actually, BS4 rewrites the whole HTML. If we just want to replace the text, we can use string replacement
            # but getting the exact string of the tag can be tricky if it's malformed.
            # Let's just use string replacement on the exact string matched by BS4
            old_footer_str = str(footer)
            
            # we need to be careful. What if str(footer) is slightly different in `c` due to formatting?
            # BS4 re-formats tags. So str(footer) might not be in `c`.
            
            # Let's write a smarter regex based on what we know:
            pass

