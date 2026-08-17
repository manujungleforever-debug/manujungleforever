import os
import codecs
import glob
import re

admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

# Regex to match the logo block in subpages
logo_pattern = re.compile(
    r'<a href="panel\.html" class="logo-brand">\s*<div class="logo-wrap"><div class="logo-glow"></div><img src="\.\./assets/img/logo\.png" alt="Logo"></div>\s*<span class="brand-name">Manu Jungle</span>\s*</a>',
    re.MULTILINE
)

new_logo = '''<a href="/" class="logo-brand" title="Ir al Home">
      <div class="logo-wrap"><div class="logo-glow"></div><img src="../assets/img/logo.png" alt="Logo" style="height: 80px; width: auto; max-width: none;"></div>
    </a>'''

files_changed = 0

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    if os.path.basename(filepath) in ['panel.html', 'index.html']:
        continue
        
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()
    
    if logo_pattern.search(content):
        content = logo_pattern.sub(new_logo, content)
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Updated logo in {os.path.basename(filepath)}")
        files_changed += 1

print(f"Total subpages updated with new logo: {files_changed}")
