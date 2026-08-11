import re

# 1. Update CSS
css_file = 'g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com/assets/css/new.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css = f.read()

# Change from 4 columns to 5 columns in the grid
css = css.replace('1.6fr 1fr 1fr 1fr;gap:48px', '1.6fr 1fr 1fr 1.1fr 1.1fr;gap:36px')

# Also handle max-width:1100px media query
# Wait, let's see if there are other column definitions
# Just replace 1.6fr 1fr 1fr 1fr with 1.6fr 1fr 1fr 1fr 1fr to be safe if I can't find gap:48px exactly, wait I did find gap:48px before
css = re.sub(r'1\.6fr 1fr 1fr 1fr;gap:48px', '1.6fr 1fr 1fr 1.1fr 1.1fr;gap:36px', css)

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update index.php
php_file = 'g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com/index.php'
with open(php_file, 'r', encoding='utf-8') as f:
    php = f.read()

# Extract the libro box from Explore column
libro_pattern = r'\s*<div style="margin-top:30px;">.*?</a>\s*</div>'
libro_match = re.search(libro_pattern, php, flags=re.DOTALL)
if libro_match:
    libro_html = libro_match.group(0)
    # Remove from original place
    php = php.replace(libro_html, '')
    
    # Increase image size
    libro_html = libro_html.replace('max-width:40px;', 'max-width:90px; width:100%;')
    # Change padding slightly
    libro_html = libro_html.replace('padding:16px 12px;', 'padding:24px 16px;')
    # Remove top margin since it will be its own column
    libro_html = libro_html.replace('<div style="margin-top:30px;">', '<div>')
    
    # Create the new column
    new_column = f'    <div><p class="fh">Legal</p>{libro_html}</div>\n'
    
    # Insert new column between Explore and Wildlife Tours
    php = php.replace('    <div><p class="fh">Wildlife Tours</p>', new_column + '    <div><p class="fh">Wildlife Tours</p>')

with open(php_file, 'w', encoding='utf-8') as f:
    f.write(php)

print('Updated CSS and PHP')
