import glob
import os

count = 0
for root, _, files in os.walk('www.manujungleforever.com'):
    for file in files:
        if file.endswith('.html'):
            f = os.path.join(root, file)
            content = ""
            enc = 'utf-8'
            try:
                with open(f, 'r', encoding='utf-8') as file_obj:
                    content = file_obj.read()
            except UnicodeDecodeError:
                try:
                    with open(f, 'r', encoding='cp1252') as file_obj:
                        content = file_obj.read()
                    enc = 'cp1252'
                except Exception:
                    continue
            
            if 'libro_reclamaciones_new.png' in content:
                content = content.replace('libro_reclamaciones_new.png', 'libro_reclamaciones.png')
                with open(f, 'w', encoding=enc) as file_obj:
                    file_obj.write(content)
                count += 1
                print(f"Updated (as {enc}): {f}")

print(f"Successfully updated {count} files.")
