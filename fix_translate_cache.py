import os
import glob

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# 1. Update the CSS to have stronger Google Translate rules
css_path = os.path.join(base_dir, "assets", "css", "new.css")
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("\n/* Stronger Google Translate Fix */\n")
    f.write(".goog-text-highlight { background-color: transparent !important; box-shadow: none !important; border: none !important; }\n")
    f.write("#goog-gt-tt, .goog-te-balloon-frame, .goog-tooltip, .goog-tooltip:hover { display: none !important; }\n")
    f.write("body { top: 0 !important; }\n")

print("CSS updated.")

# 2. Add ?v=3 to all HTML files to bust cache
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)
count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # replace ../assets/css/new.css or ../assets/css/new.css?v=... with ?v=3
    import re
    new_content = re.sub(r'href="(\.\./)+assets/css/new\.css(\?v=\d+)?"', r'href="\1assets/css/new.css?v=3"', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated cache buster in {count} HTML files.")
