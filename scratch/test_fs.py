keys = [
    'usuarios/kemmesik-gmail-com/avatar_1787257830305.jpg',
    'usuarios/manujungleforever-gmail-com/avatar_1787257867111.jpg',
    'pasajeros/dep-010_manu-reserved-zone-6-days_2026-09-10/idel-everardo-maza-maza.jpg',
    'pasajeros/dep-010_manu-reserved-zone-6-days_2026-09-10/johan-miro.jpg',
    '1787077873119-fb-img-1748235222019.jpg',
    '1787078183119-fa-img-1748235222019.jpg'
]

def get_contents_at_path(keys, current_path=''):
    current_path = current_path.strip('/')
    folders = set()
    files = []
    
    for k in keys:
        if not current_path:
            # Root level
            if '/' in k:
                folders.add(k.split('/')[0])
            else:
                files.append(k)
        else:
            if k.startswith(current_path + '/'):
                rel = k[len(current_path) + 1:]
                if '/' in rel:
                    folders.add(rel.split('/')[0])
                else:
                    files.append(k)
                    
    print(f'Path: "{current_path}"')
    print('  Folders:', sorted(list(folders)))
    print('  Files:', files)

get_contents_at_path(keys, '')
get_contents_at_path(keys, 'pasajeros')
get_contents_at_path(keys, 'pasajeros/dep-010_manu-reserved-zone-6-days_2026-09-10')
get_contents_at_path(keys, 'usuarios')
