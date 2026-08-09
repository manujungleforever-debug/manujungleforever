import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            
            rel_dir = os.path.relpath(root, base_dir)
            depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
            prefix = "../" * depth if depth > 0 else ""
            
            favicon_path = f"{prefix}assets/img/favicon.png"
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = re.sub(
                r'<link rel="icon" href="[^"]*" sizes="32x32">',
                f'<link rel="icon" href="{favicon_path}" sizes="32x32">',
                content
            )
            new_content = re.sub(
                r'<link rel="apple-touch-icon" href="[^"]*">',
                f'<link rel="apple-touch-icon" href="{favicon_path}">',
                new_content
            )
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("Done - favicon.png applied to all pages.")
