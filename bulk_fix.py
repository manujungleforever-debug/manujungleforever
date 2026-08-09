import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

# Replacements
replacements = [
    (r'51979808013', r'51901525679'),
    (r'51923289231', r'51901525679'),
    (r'\+51 979 808 013', r'+51 901 525 679'),
    (r'\+51 923 289 231 \(Anna\'s WhatsApp\)', r'+51 901 525 679 (WhatsApp)'),
    (r'\+51 923 289 231', r'+51 901 525 679'),
    (r'La Casa Escondida 17800', r'Fitzcarrald 17800'),
    (r'https://maps\.google\.com/maps\?q=-12\.551044080333435,-71\.16934096724118&hl=en&z=15&output=embed', r'https://maps.google.com/maps?q=-12.540486,-71.166315&hl=en&z=17&t=k&output=embed'),
    # Note: added z=17 to zoom in a bit more on the satellite map
    (r'Message Anna on WhatsApp', r'Message us on WhatsApp')
]

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = re.sub(old, new, new_content)
    
    # Remove bk-modal ONLY in contact/index.html to prevent duplicate forms
    if filepath.endswith(os.path.join('contact', 'index.html')):
        modal_pattern = re.compile(r'<div class="modal" id="bk-modal".*?</div>\s*</div>\s*</div>', re.DOTALL)
        new_content = modal_pattern.sub('', new_content)
        # Also remove the scripts that open it in contact to avoid errors
        script_pattern = re.compile(r'function openModal\(\).*?function closeModal\(\).*?\}', re.DOTALL)
        new_content = script_pattern.sub('function openModal(){} function closeModal(){}', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# Update new.css for map-container
css_path = os.path.join(base_dir, 'assets', 'css', 'new.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

map_css = """
.map-container {
  height: 350px;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  margin-top: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.05);
}
"""
if ".map-container {" not in css:
    css += "\n" + map_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Injected .map-container into new.css")

print("All bulk fixes completed.")
