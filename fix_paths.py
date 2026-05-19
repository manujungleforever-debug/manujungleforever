import os

base_dir = 'g:/Git/HiddenJungleCusco/www.hiddenjunglecusco.com'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if '..../wp-content' in content:
                content = content.replace('..../wp-content', '../wp-content')
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed {path}")
