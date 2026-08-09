import os

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# The broken string we want to fix
broken_1 = '<img src="../assets/img/logo.png" alt="Manu Jungle Forever" loading="lazy">" class="fl" loading="lazy">'
fixed_1 = '<img src="../assets/img/logo.png" alt="Manu Jungle Forever" class="fl" loading="lazy">'

broken_2 = '<img src="../../assets/img/logo.png" alt="Manu Jungle Forever" loading="lazy">" class="fl" loading="lazy">'
fixed_2 = '<img src="../../assets/img/logo.png" alt="Manu Jungle Forever" class="fl" loading="lazy">'

broken_3 = 'loading="eager">" class="fl" loading="lazy">'
fixed_3 = 'class="fl" loading="eager">'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            content = content.replace(broken_1, fixed_1)
            content = content.replace(broken_2, fixed_2)
            content = content.replace('<img src="../assets/img/logo.png" alt="Manu Jungle Forever" loading="lazy">" width="190" height="54" loading="eager">', '<img src="../assets/img/logo.png" alt="Manu Jungle Forever" width="190" height="54" loading="eager">')
            
            # just in case
            content = content.replace('loading="lazy">" class="fl" loading="lazy">', 'class="fl" loading="lazy">')
            
            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed broken tag in: {path}")

print("Done fixing broken tags.")
