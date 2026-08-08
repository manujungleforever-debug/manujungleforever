import os

src_dir = "www.hiddenjunglecusco.com"
dst_dir = "www.manujungleforever.com"

replacements = {
    'hiddenjunglecusco': 'manujungleforever',
    'Hidden Jungle Cusco': 'Manu Jungle Forever',
    'Hidden Jungle': 'Manu Jungle',
    'Guided jungle tours from Cusco to the Manu National Park & the Peruvian Amazon. Local. Wild. Authentic.': '<span style="font-family: \'Playfair Display\', serif; font-style: italic; font-size: 1.15rem; letter-spacing: 0.02em; color: var(--a); line-height: 1.5; display: block; margin-top: 10px;">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</span>',
    'Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.': '<span style="font-family: \'Playfair Display\', serif; font-style: italic; font-size: 1.15rem; letter-spacing: 0.02em; color: var(--a); line-height: 1.5; display: block; margin-top: 10px;">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</span>'
}

for root, dirs, files in os.walk(dst_dir):
    for file in files:
        if file.endswith(('.html', '.php', '.json', '.js', '.css')) and file != 'new.css':
            dst_path = os.path.join(root, file)
            # Find corresponding file in src_dir
            rel_path = os.path.relpath(dst_path, dst_dir)
            src_path = os.path.join(src_dir, rel_path)
            
            if os.path.exists(src_path):
                try:
                    with open(src_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for old, new in replacements.items():
                        content = content.replace(old, new)
                    
                    with open(dst_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    pass
