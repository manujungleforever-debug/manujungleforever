import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_sc = ".sc i { color: #fff !important; width: auto !important; margin-top: 0 !important; }"
new_sc = ".sc i { color: #fff !important; margin-top: 0 !important; }"

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if old_sc in content:
            content = content.replace(old_sc, new_sc)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error {fpath}: {e}")
print("Done.")
