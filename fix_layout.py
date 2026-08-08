import os
import re

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")
css_path = os.path.join(base_dir, "assets", "css", "new.css")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove google_translate_element from the header
gt_element_regex = r'<div id="google_translate_element" style="display:none;"></div>\s*'
content = re.sub(gt_element_regex, '', content)

# 2. Add it to the bottom of the body, just before the script
gt_script_regex = r'<script type="text/javascript">\s*function googleTranslateElementInit'
replacement = '<div id="google_translate_element" style="display:none;"></div>\n<script type="text/javascript">\nfunction googleTranslateElementInit'
content = re.sub(gt_script_regex, replacement, content)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

# 3. Add CSS to ensure .ls-custom doesn't wrap and items stay inline
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

if ".nm { flex-wrap: nowrap; }" not in css_content:
    css_content += "\n.nm { flex-wrap: nowrap; white-space: nowrap; }\n"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

print("Moved google_translate_element to the bottom.")
