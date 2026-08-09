import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)
count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # replace ?v=3 with ?v=4
    new_content = re.sub(r'href="(\.\./)+assets/css/new\.css\?v=3"', r'href="\1assets/css/new.css?v=4"', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated cache buster to v=4 in {count} HTML files.")
