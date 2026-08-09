import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

search_footer = 'Nuevo Eden, Manu National Park, Peru</a>'
replace_footer = 'Fitzcarrald 17800, Nuevo Eden, Peru</a>'

search_contact1 = 'Manu Jungle Forever – La Casa Escondida 17800<br>Nuevo Eden, Peru'
replace_contact1 = 'Fitzcarrald 17800<br>Nuevo Eden, Peru'

search_contact2 = 'Manu Jungle Forever - La Casa Escondida 17800'
replace_contact2 = 'Fitzcarrald 17800'

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace(search_footer, replace_footer)
        new_content = new_content.replace(search_contact1, replace_contact1)
        new_content = new_content.replace(search_contact2, replace_contact2)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Updated {fpath}")
    except Exception as e:
        pass
