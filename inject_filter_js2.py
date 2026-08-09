import os
import re

manu_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\guided-tours\index.html"

# Extract just the category filter block from temp
with open('temp_filter_js.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

match = re.search(r'(// ── Category Filter.*?\(\)\{.*?\}\)\(\);)', js_content, re.DOTALL)
if match:
    filter_js = match.group(1)
else:
    print("Could not extract filter JS.")
    exit(1)

with open(manu_path, 'r', encoding='utf-8') as f:
    html = f.read()

# The script block at the bottom has: // Modal
if '// Modal' in html and 'const buttons = document.querySelectorAll' not in html:
    html = html.replace('// Modal', filter_js + '\n\n// Modal')
    with open(manu_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully injected Category Filter JS.")
elif 'const buttons = document.querySelectorAll' in html:
    print("Filter JS already exists.")
else:
    print("Could not find // Modal anchor.")
