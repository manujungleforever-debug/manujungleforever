import os
import re

base_dir = "www.manujungleforever.com"
css_file = os.path.join(base_dir, "assets", "css", "new.css")

# 1. Update index.php and index.html to remove the ugly inline style
for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove the inline styling that ruins the footer paragraph
        content = re.sub(
            r'<span style="font-family: \'Playfair Display\', serif; font-style: italic; font-size: 1\.15rem; letter-spacing: 0\.02em; color: var\(--a\); line-height: 1\.5; display: block; margin-top: 10px;">(.*?)</span>',
            r'<span style="display: block; margin-top: 15px; font-size: 0.95rem; line-height: 1.6; color: rgba(255,255,255,0.65); font-weight: 300;">\1</span>',
            content
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# 2. Update new.css colors to premium Emerald Green and fix footer styles
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Replace cyan with emerald green
    css = css.replace('--a:#22d3ee', '--a:#10B981')
    css = css.replace('--al:#67e8f9', '--al:#34D399')
    
    # Improve footer heading visibility
    css = css.replace('color:rgba(255,255,255,.28)', 'color:rgba(255,255,255,.5)')
    
    # Fix the weird list item marker in the footer links
    css = re.sub(r'\.fli a::before\{content:\'.*?\';', '.fli a::before{content:\'\\\\2192\';', css)
    
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)

# 3. Update rebuild_tours.py since we modified index.php
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'<span style="font-family: \'Playfair Display\'.*?</span>',
        r'<span style="display: block; margin-top: 15px; font-size: 0.95rem; line-height: 1.6; color: rgba(255,255,255,0.65); font-weight: 300;">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</span>',
        content
    )
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)

