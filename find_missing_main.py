import os
import glob

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

missing_main = []
for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if '<main' not in content:
                missing_main.append(filepath)
    except Exception as e:
        pass

if missing_main:
    print("Files missing <main tag:")
    for f in missing_main:
        print(f)
else:
    print("All HTML files have a <main tag.")
