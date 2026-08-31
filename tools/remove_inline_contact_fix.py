import os

filepath = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\contact\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "<script>" in line and i + 1 < len(lines) and "// Dynamic Contact & Global Data Hydration" in lines[i+1]:
        skip = True
    
    if not skip:
        new_lines.append(line)
        
    if skip and "</script>" in line and i - 1 >= 0 and "})();" in lines[i-1]:
        skip = False

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    
print(f"Original lines: {len(lines)}")
print(f"New lines: {len(new_lines)}")
