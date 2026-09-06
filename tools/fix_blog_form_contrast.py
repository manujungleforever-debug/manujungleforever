import glob
import re

files = glob.glob('www.manujungleforever.com/**/*.html', recursive=True)
count = 0

for f in files:
    if 'admin' in f or 'wp-content' in f:
        continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    nc = c
    # Subtitle under leave a comment
    nc = re.sub(
        r'color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.55\);?',
        'color: var(--earth-muted);',
        nc,
        flags=re.I
    )
    # Note under comment button
    nc = re.sub(
        r'color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*(?:0\.35|0\.4|0\.45|0\.5)\);?',
        'color: var(--earth-subtle);',
        nc,
        flags=re.I
    )
    
    if nc != c:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(nc)
        print(f'Fixed blog comment contrast in: {f}')
        count += 1

print(f'Done. Updated {count} files.')
