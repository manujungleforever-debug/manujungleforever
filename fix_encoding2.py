import os

replacements = {
    'Â·': '·',
    'â˜…': '★',
    'â€“': '–',
    'â€”': '—',
    'Ã¢â‚¬â€œ': '-',
    'Ã¢â‚¬â€': '-'
}

for root, dirs, files in os.walk('www.manujungleforever.com'):
    for file in files:
        if file.endswith(('.html', '.php')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                for old, new in replacements.items():
                    if old in content:
                        content = content.replace(old, new)
                        modified = True
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
            except Exception as e:
                pass
