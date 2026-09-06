import glob
import re

html_files = glob.glob('www.manujungleforever.com/**/*.html', recursive=True)
modified = 0

for f in html_files:
    if 'admin' in f:
        continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    new_content = content
    
    # 1. In .tour-rich-text, remove or replace white/semi-white color with var(--earth-text)
    new_content = re.sub(
        r'(<div[^>]*class=[\'"][^\'"]*tour-rich-text[^\'"]*[\'"][^>]*style=[\'"][^\'"]*)color:\s*(?:rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*[\d\.]+\)|#fff(?:fff)?);?([^\'"]*[\'"])',
        r'\1color: var(--earth-text);\2',
        new_content,
        flags=re.I
    )
    
    # 2. In intro-block h2 text-white
    new_content = re.sub(
        r'(<div class=[\'"]intro-block[^\'"]*[\'"][\s\S]*?<h2 class=[\'"][^\'"]*)\btext-white\b([^\'"]*[\'"])',
        r'\1\2',
        new_content,
        flags=re.I
    )
    
    # 3. In blog detail metadata/comment form labels that had inline white
    # e.g., <div style="display:flex; align-items:center; gap:8px; margin-bottom:32px; font-size:1rem; color:rgba(255,255,255,.8)">
    new_content = re.sub(
        r'(<div[^>]*style=[\'"][^\'"]*margin-bottom:\s*32px;[^\'"]*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*[\d\.]+\);?([^\'"]*[\'"])',
        r'\1color: var(--earth-muted);\2',
        new_content,
        flags=re.I
    )
    
    # In blog comment form labels: <label for="cf-..." style="display:block; ... color:rgba(255,255,255,0.7); ...">
    new_content = re.sub(
        r'(<label[^>]*for=[\'"]cf-[^\'"]*[\'"][^>]*style=[\'"][^\'"]*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*[\d\.]+\);?([^\'"]*[\'"])',
        r'\1color: var(--forest-mid);\2',
        new_content,
        flags=re.I
    )
    
    # In blog comment form note: <p style="... color:rgba(255,255,255,0.35); ...">Your email address will not be published.
    new_content = re.sub(
        r'(<p[^>]*style=[\'"][^\'"]*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.35\);?([^\'"]*[\'"][^>]*>Your email address)',
        r'\1color: var(--earth-subtle);\2',
        new_content,
        flags=re.I
    )
    
    # In wildlife-tours-from-cusco:
    new_content = re.sub(
        r'(<p style=[\'"]font-size:\s*1\.05rem;\s*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.7\);?',
        r'\1color: var(--earth-text);',
        new_content,
        flags=re.I
    )
    new_content = re.sub(
        r'(<li[^>]*style=[\'"][^\'"]*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.8\);?',
        r'\1color: var(--earth-text);',
        new_content,
        flags=re.I
    )
    new_content = re.sub(
        r'(<p style=[\'"]color:\s*)rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.6\);?(\s*font-size:\s*0\.95rem;[\'"]>\(Placeholder text)',
        r'\1var(--earth-muted);\2',
        new_content,
        flags=re.I
    )

    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        print(f'Updated contrast in: {f}')
        modified += 1

print(f'Done. Updated {modified} files.')
