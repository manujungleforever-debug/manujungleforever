import glob, os, re

admin_dirs = ['admin', 'www.manujungleforever.com/admin']

for d in admin_dirs:
    for fpath in glob.glob(os.path.join(d, 'gestionar-*.html')) + glob.glob(os.path.join(d, 'index.html')) + glob.glob(os.path.join(d, 'panel.html')):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()

        # 1. Standardize main in CSS
        c = re.sub(
            r'main\s*\{[^}]*\}',
            'main { flex-grow:1; max-width:1200px !important; width:100% !important; margin:0 auto !important; padding:28px 20px 100px !important; position:relative; z-index:1; box-sizing:border-box; }',
            c
        )

        # 2. Standardize .eform in CSS
        c = re.sub(
            r'\.eform\s*\{\s*max-width:\s*\d+px;[^}]*\}',
            '.eform { max-width:1200px; width:100%; margin:0 auto 60px auto; display:flex; flex-direction:column; gap:18px; box-sizing:border-box; }',
            c
        )
        c = re.sub(
            r'\.eform\s*\{\s*width:\s*100%;\s*display:\s*flex;[^}]*\}',
            '.eform { max-width:1200px; width:100%; margin:0 auto 60px auto; display:flex; flex-direction:column; gap:18px; box-sizing:border-box; }',
            c
        )

        # 3. Ensure .list-grid, .blog-grid are 100%
        c = re.sub(
            r'\.list-grid,\s*\.blog-grid\s*\{[^}]*\}',
            '.list-grid, .blog-grid { display:grid; gap:14px; width:100%; max-width:1200px; margin:0 auto; box-sizing:border-box; }',
            c
        )

        # 4. Clean any inline max-width:900px or 1280px in .eform
        c = re.sub(
            r'<div class="eform" style="[^"]*">',
            '<div class="eform">',
            c
        )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Centered layout in {fpath}")

print("All admin views centered.")
