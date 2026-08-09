import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# Regexes for the logo and links
# The old logo in the footer is:
# src="wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png"
# and in the header:
# src="wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1.png"
old_logo_re = re.compile(r'<img[^>]*src="wp-content/uploads/[^"]*(?:Logo-1|TextSeal_3Color)\.png"[^>]*>')
# Also replace the surrounding <a> if it goes to index.php
index_php_re = re.compile(r'href="index\.php"')

def remove_bk_modal(content):
    idx = content.find('id="bk-modal"')
    if idx == -1: return content
    
    # find the preceding <div
    start_idx = content.rfind('<div', 0, idx)
    if start_idx == -1: return content
    
    # Count divs to find matching end
    div_count = 0
    curr_idx = start_idx
    while curr_idx < len(content):
        next_open = content.find('<div', curr_idx)
        next_close = content.find('</div', curr_idx)
        
        if next_open == -1 and next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            curr_idx = next_open + 4
        elif next_close != -1:
            div_count -= 1
            curr_idx = next_close + 6
            if div_count == 0:
                # We found the end!
                return content[:start_idx] + content[curr_idx:]
    
    return content

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            
            # calculate depth for paths
            rel_dir = os.path.relpath(root, base_dir)
            depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
            prefix = "../" * depth if depth > 0 else ""
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig_content = content
            
            # 1. Remove bk-modal
            # It might appear multiple times if the user copy-pasted badly
            while 'id="bk-modal"' in content:
                content = remove_bk_modal(content)
            
            # 2. Fix logos
            new_logo = f'<img src="{prefix}assets/img/logo.png" alt="Manu Jungle Forever" loading="lazy">'
            content = old_logo_re.sub(new_logo, content)
            
            # 3. Fix index.php links
            content = index_php_re.sub(f'href="{prefix}index.html"', content)
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {path}")

print("Done fixing site-wide issues.")
