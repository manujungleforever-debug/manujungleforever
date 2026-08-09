import os

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
broken_str = '".replace(">Home", " class=\\"on\\">Home")'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if broken_str in content:
                content = content.replace(broken_str, '')
                # Clean up any duplicate spaces left behind
                content = content.replace('</a>  <a', '</a>\n    <a')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed broken replace string in: {path}")

print("Done fixing broken replace string.")
