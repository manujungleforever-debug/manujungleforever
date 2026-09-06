import os
import re

root_dir = 'www.manujungleforever.com'
home_path = os.path.abspath(os.path.join(root_dir, 'index.html'))
target_style = "color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;"

modified = []
total_count = 0

for root, _, files in os.walk(root_dir):
    if 'admin' in root.split(os.sep):
        continue
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            if os.path.abspath(path) == home_path:
                continue
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            c = content.count(target_style)
            if c > 0:
                total_count += c
                new_content = content.replace(target_style, '')
                # Clean up empty style attributes or messy spaces inside style
                new_content = re.sub(r'style=[\'"]\s*[\'"]', '', new_content)
                new_content = re.sub(r'\s+style=[\'"]\s*;?\s*[\'"]', '', new_content)
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new_content)
                modified.append(path)

print(f"Cleaned {total_count} occurrences across {len(modified)} files.")
