import os

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
        
        # 1. Find the logo in the footer
        logo_idx = c.find('HiddenJungleCusco_Logo_TextSeal_3Color')
        if logo_idx == -1:
            logo_idx = c.find('class="fbi"') # Alternative marker in the footer
        
        if logo_idx != -1:
            # 2. Find start of footer
            start_idx = c.rfind('<footer class="ft">', 0, logo_idx)
            if start_idx == -1:
                start_idx = c.rfind('<footer', 0, logo_idx)
            if start_idx == -1:
                # If no footer tag at all, find the wrapper div
                start_idx = c.rfind('<div class="cx">', 0, logo_idx)
                
            # 3. Find end of footer
            end_idx = c.find('</footer>', logo_idx)
            if end_idx != -1:
                end_idx += len('</footer>')
                
                # We have start and end!
                if start_idx != -1:
                    old_footer = c[start_idx:end_idx]
                    
                    # Also remove any <style> blocks immediately before the footer if they exist and contain footer styles
                    # But it's safer to just replace from start_idx to end_idx
                    new_c = c[:start_idx] + new_footer + c[end_idx:]
                    if new_c != c:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(new_c)
                        updated += 1

print(f"Smarter footer replace updated {updated} files.")
