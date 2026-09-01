import glob

for f in glob.glob('g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com/admin/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original = content
    
    # Fix the title attribute injection
    content = content.replace('title="${l}">${l}</button>', 'title="${l.replace(/<[^>]+>/g, \'\').trim()}">${l}</button>')
    
    # Fix the ? R2 string
    content = content.replace('?☁️ R2</button>', '<i class="ph ph-cloud"></i> R2</button>')
    content = content.replace('?&#9729;&#65039; R2</button>', '<i class="ph ph-cloud"></i> R2</button>')
    
    if content != original:
        print(f'Fixed {f}')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
