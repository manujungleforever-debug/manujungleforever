import re

with open('about_us_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, undo the simple replacement I did via powershell
html = html.replace('<div class="zz-img r rl">', '<div class="zz-img">')
html = html.replace('<div class="zz-txt r rr">', '<div class="zz-txt">')

def replacer(match):
    full_row = match.group(0)
    if 'reverse' in full_row:
        # Reverse row: txt on left, img on right
        full_row = full_row.replace('<div class="zz-img">', '<div class="zz-img r rr">')
        full_row = full_row.replace('<div class="zz-txt">', '<div class="zz-txt r rl">')
    else:
        # Normal row: img on left, txt on right
        full_row = full_row.replace('<div class="zz-img">', '<div class="zz-img r rl">')
        full_row = full_row.replace('<div class="zz-txt">', '<div class="zz-txt r rr">')
    return full_row

# Pattern to capture a full zigzag row
html = re.sub(r'<div class="zigzag-row.*?</div>\s*</div>', replacer, html, flags=re.DOTALL)

with open('about_us_template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated animations")
