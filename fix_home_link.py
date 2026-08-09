import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            
            # Fix corrupted Home links
            # Looking for things like: <a href="<a href="../index.html">Home</a>
            content = re.sub(r'<a href="<a href="([^"]*index\.html)">Home</a>', r'<a href="\1">Home</a>', content)
            content = re.sub(r'<a href="<a href="([^"]*index\.html)" class="on">Home</a>', r'<a href="\1" class="on">Home</a>', content)
            
            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed Home link in: {path}")

print("Done fixing Home links.")
