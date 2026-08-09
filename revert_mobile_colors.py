import os

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

old_style = 'style="color:var(--g1);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"'
new_style = 'style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"'

updated = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_style in content:
                content = content.replace(old_style, new_style)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1

print(f"Reverted inline mobile colors in {updated} files.")
