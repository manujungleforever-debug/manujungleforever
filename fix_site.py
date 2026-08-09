import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

bk_modal_re = re.compile(r'(<div id="bk-modal" class="bk-modal".*?</div>\s*</div>\s*</div>)', re.DOTALL)
open_modal_btn_re = re.compile(r'<button([^>]*?)onclick="openModal\(\)"([^>]*?)>(.*?)</button>')
open_modal_a_re = re.compile(r'<a([^>]*?)onclick="openModal\(\)"([^>]*?)>(.*?)</a>')

old_logo_re = re.compile(r'<div class="nl"><a href="index\.php"><img src="wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1\.png"[^>]*></a></div>')
home_php_re = re.compile(r'<a href="index\.php"([^>]*)>Home</a>')

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
            # Let's just find <div id="bk-modal" and remove everything until the script tag or footer
            if '<div id="bk-modal"' in content:
                # Find start
                start_idx = content.find('<div id="bk-modal"')
                # Find the script tag that follows it usually
                end_idx = content.find('<script>', start_idx)
                if end_idx == -1:
                    end_idx = content.find('</body>', start_idx)
                
                if start_idx != -1 and end_idx != -1:
                    content = content[:start_idx] + content[end_idx:]
            
            # 2. Change openModal buttons to links to contact page
            contact_url = prefix + "contact/index.html"
            
            # replace button with a
            content = open_modal_btn_re.sub(r'<a href="' + contact_url + r'"\1\2>\3</a>', content)
            # replace a with a
            content = open_modal_a_re.sub(r'<a href="' + contact_url + r'"\1\2>\3</a>', content)
            
            # 3. Fix blog old logo
            new_logo = f'<div class="nl"><a href="{prefix}index.html"><img src="{prefix}assets/img/logo.png" alt="Manu Jungle Forever" loading="eager"></a></div>'
            content = old_logo_re.sub(new_logo, content)
            
            # 4. Fix index.php home links
            content = home_php_re.sub(r'<a href="' + prefix + r'index.html"\1>Home</a>', content)
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {path}")

print("Done fixing site-wide issues.")
