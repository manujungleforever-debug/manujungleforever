import os, glob, re

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update .fa style
        old_fa = r".fa { font-family: 'Syne', sans-serif; font-size: 0.85rem; line-height: 1.6; color: rgba(255,255,255,0.7); text-transform: uppercase; margin-bottom: 25px; margin-top: 15px; display: block; }"
        new_fa = r".fa { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 800; letter-spacing: 0.05em; line-height: 1.6; color: #ffffff; text-transform: uppercase; margin-bottom: 25px; margin-top: 15px; display: block; }"
        content = content.replace(old_fa, new_fa)
        
        # Add .sc style right after .fa or .f-col
        if '.sc {' not in content and '<footer class="ft">' in content:
            style_injection = r"""
  .sc { width: 36px; height: 36px; border-radius: 50%; background: var(--a); display: inline-flex; align-items: center; justify-content: center; color: #fff !important; text-decoration: none; transition: transform 0.3s ease; margin-right: 8px; }
  .sc i { color: #fff !important; width: auto !important; margin-top: 0 !important; }
  .sc:hover { transform: translateY(-3px); }
</style>"""
            content = content.replace('</style>', style_injection, 1)

        # Update logo max-width
        content = re.sub(r'(class="fl"[^>]*?style="max-width:\s*)250px(;?")', r'\g<1>320px\2', content)

        # Update social icons flex gap just in case
        if 'class="so" style="margin-top: 25px;"' in content:
             content = content.replace('class="so" style="margin-top: 25px;"', 'class="so" style="margin-top: 25px; display: flex; gap: 10px; flex-wrap: wrap;"')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error {fpath}: {e}")
print("Done.")
