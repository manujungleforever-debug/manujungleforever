import os

search_dir = 'www.hiddenjunglecusco.com'

reps = [
    ('family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600', 'family=Montserrat:wght@700;800&family=Inter:wght@300;400;500;600'),
    ("'Syne'", "'Montserrat'"),
    ('"Syne"', "'Montserrat'"),
    ("'Outfit'", "'Inter'"),
    ('"Outfit"', "'Inter'")
]

for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.css'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                new_content = content
                for old, new in reps:
                    new_content = new_content.replace(old, new)
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print('Updated ' + path)
            except Exception as e:
                pass
