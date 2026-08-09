import os

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

replacements = [
    ('<link rel="icon" href="assets/img/hero.png" sizes="32x32">', '<link rel="icon" href="assets/img/favicon.png" sizes="32x32">'),
    ('<link rel="apple-touch-icon" href="assets/img/hero.png">', '<link rel="apple-touch-icon" href="assets/img/favicon.png">'),
    ('<link rel="icon" href="../assets/img/hero.png" sizes="32x32">', '<link rel="icon" href="../assets/img/favicon.png" sizes="32x32">'),
    ('<link rel="apple-touch-icon" href="../assets/img/hero.png">', '<link rel="apple-touch-icon" href="../assets/img/favicon.png">')
]

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            for old, new in replacements:
                content = content.replace(old, new)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated favicon in: {filepath}")

print("Done updating favicons.")
