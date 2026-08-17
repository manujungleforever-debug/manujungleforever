import os
import codecs
import glob
import re

admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

# Standard logo height
new_logo_style = 'height: 120px; width: auto; max-width: none;'

files_changed = 0

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Update logo size in panel.html and index.html
    content = re.sub(r'style="height:\s*\d+px;\s*width:\s*auto;\s*max-width:\s*none;"', f'style="{new_logo_style}"', content)
    
    # 2. Update logo size if it doesn't have the inline style yet (just in case)
    content = re.sub(r'<img src="\.\./assets/img/logo\.png" alt="Logo">', f'<img src="../assets/img/logo.png" alt="Logo" style="{new_logo_style}">', content)
    
    # 3. Standardize header padding and background in panel.html to match the sleek dark theme better
    if os.path.basename(filepath) == 'panel.html':
        content = re.sub(r'padding:\s*15px\s*30px;', 'padding: 20px 30px;', content)
        
    # 4. Standardize padding in subpages (.hw)
    elif os.path.basename(filepath) not in ['panel.html', 'index.html']:
        content = re.sub(r'\.hw\s*\{\s*max-width:1400px;\s*margin:0\s+auto;\s*padding:10px\s+24px;', '.hw { max-width:1400px; margin:0 auto; padding: 20px 30px;', content)
        
    if content != original_content:
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Standardized header/logo in {os.path.basename(filepath)}")
        files_changed += 1

print(f"Total files updated: {files_changed}")
