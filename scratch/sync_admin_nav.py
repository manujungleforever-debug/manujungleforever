import glob, os

admin_dirs = ['www.manujungleforever.com/admin', 'admin']

for ad in admin_dirs:
    files = glob.glob(os.path.join(ad, 'gestionar-*.html'))
    for f in files:
        if 'gestionar-usuarios.html' in f:
            continue
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        if 'gestionar-usuarios.html' not in content and '<nav class="mnav">' in content:
            if '<a href="gestionar-medios.html"' in content:
                target = '<a href="gestionar-medios.html"'
                idx = content.find(target)
                end_idx = content.find('</a>', idx) + 4
                content = content[:end_idx] + '\n      <a href="gestionar-usuarios.html" id="nav-usuarios"><i class="ph ph-users-three"></i> Usuarios</a>' + content[end_idx:]
                
                with open(f, 'w', encoding='utf-8') as fp:
                    fp.write(content)
                print(f'Updated {f}')

print('All admin files synchronized with Usuarios nav link.')
