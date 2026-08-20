import glob

files = [
    'admin/gestionar-salidas.html',
    'www.manujungleforever.com/admin/gestionar-salidas.html'
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update newId calculation to DEP-0001 (4 digits)
    old_code = "newId = String(nextNum).padStart(3, '0');"
    new_code = "newId = `DEP-${String(nextNum).padStart(4, '0')}`;"
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated departure ID format in {fpath}")
    else:
        print(f"Old code not found in {fpath}")
