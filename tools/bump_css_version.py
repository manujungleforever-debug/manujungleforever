import os
import glob

ROOT = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

count = 0
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('new.css?v=30', 'new.css?v=31')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} files to v=31")
