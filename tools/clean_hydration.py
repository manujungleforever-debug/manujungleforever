import os

# 1. Clean index.html
index_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\index.html"
with open(index_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "<script>" in line and i + 1 < len(lines) and "// Dynamic Home & Global Data Hydration" in lines[i+1]:
        skip = True
    
    if not skip:
        new_lines.append(line)
        
    if skip and "</script>" in line and i - 1 >= 0 and "})();" in lines[i-1]:
        skip = False

with open(index_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"Removed inline script from index.html (before: {len(lines)}, after: {len(new_lines)})")

# 2. Clean global-sync.js
sync_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\js\global-sync.js"
with open(sync_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "// 1. Floating WhatsApp button" in line:
        skip = True
        
    if skip and "// 5. Individual Tour Page dynamic hydration" in line:
        skip = False
        
    if not skip:
        new_lines.append(line)

with open(sync_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Removed static DOM manipulation from global-sync.js (before: {len(lines)}, after: {len(new_lines)})")
