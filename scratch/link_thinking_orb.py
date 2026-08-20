import glob, os

admin_dirs = ['www.manujungleforever.com/admin', 'admin']

for ad in admin_dirs:
    files = glob.glob(os.path.join(ad, '*.html'))
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        modified = False
        if 'thinking-orb.css' not in content:
            if '</head>' in content:
                content = content.replace('</head>', '  <link rel="stylesheet" href="css/thinking-orb.css">\n</head>')
                modified = True
        
        if 'thinking-orb.js' not in content:
            if '</body>' in content:
                content = content.replace('</body>', '  <script src="js/thinking-orb.js"></script>\n</body>')
                modified = True
        
        if modified:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print(f'Linked thinking-orb in {f}')

print('Thinking Orb scripts linked across all admin pages.')
