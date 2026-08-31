import os

filepath = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\contact\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "<script>" in line and lines[lines.index(line) + 1].strip() == "// Dynamic Contact & Global Data Hydration":
        skip = True
    
    if not skip:
        new_lines.append(line)
        
    if skip and "</script>" in line and "})();" in lines[lines.index(line) - 1]:
        skip = False

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    
print("Removed duplicate inline hydration script from contact/index.html")
