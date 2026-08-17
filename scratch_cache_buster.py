import os
import glob

admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace auth.js with auth.js?v=2
    if 'src="js/auth.js"' in content:
        content = content.replace('src="js/auth.js"', 'src="js/auth.js?v=2"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added cache buster to {os.path.basename(filepath)}")
