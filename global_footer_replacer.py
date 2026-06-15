import os, re
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
        
        new_footer = get_new_footer(rel)
        
        # We know the footer content ends with </div></footer>
        # We need to find the START of the footer.
        # The footer is preceded by the Whatsapp floating button or </style> or </body>
        # Let's search backwards from </div></footer>
        end_idx = c.find('</div></footer>')
        if end_idx != -1:
            end_idx += len('</div></footer>')
            
            # The footer always starts with <div class="cx"> inside a <footer class="ft">, or just <div class="cx">
            # So let's look for the last <div class="cx"> before </div></footer> that is part of the footer
            # We can find all occurrences of <div class="cx">
            cx_indices = [m.start() for m in re.finditer(r'<div class="cx">', c[:end_idx])]
            if cx_indices:
                # The last one is the footer's main container.
                cx_idx = cx_indices[-1]
                
                # Check if it has <footer class="ft"> before it
                footer_start = c.rfind('<footer class="ft">', 0, cx_idx)
                if footer_start != -1 and cx_idx - footer_start < 200:
                    start_idx = footer_start
                else:
                    # check if there's a <style> block before it that belongs to the footer
                    # the footer style block contains .cx, .fg, .fh etc.
                    style_start = c.rfind('<style>', 0, cx_idx)
                    if style_start != -1 and c.find('.fg {', style_start, cx_idx) != -1:
                        # this style block is the footer's style block!
                        # check if there's <footer class="ft"> before the style block
                        footer_start2 = c.rfind('<footer class="ft">', 0, style_start)
                        if footer_start2 != -1 and style_start - footer_start2 < 50:
                            start_idx = footer_start2
                        else:
                            start_idx = style_start
                    else:
                        start_idx = cx_idx
                
                new_c = c[:start_idx] + new_footer + c[end_idx:]
                if new_c != c:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_c)
                    updated += 1

print(f"Global replacer updated {updated} files.")
