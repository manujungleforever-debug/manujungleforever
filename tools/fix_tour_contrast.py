import glob
import re

tour_files = glob.glob('www.manujungleforever.com/**/*.html', recursive=True)
updated_count = 0

for f in tour_files:
    if 'admin' in f or 'wp-content' in f:
        continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    nc = c
    # 1. Strip text-white from h2 in tour body sections (Overview and Tour Itinerary)
    nc = re.sub(
        r'<h2 class=[\'"]h2 text-white[\'"](\s*style=[\'"][^\'"]*[\'"])?>Tour Itinerary</h2>',
        r'<h2 class="h2" style="font-size: 2.2rem; margin-bottom: 30px; color: var(--forest-dark);">Tour Itinerary</h2>',
        nc,
        flags=re.I
    )
    nc = re.sub(
        r'<h2 class=[\'"]h2 text-white[\'"](\s*style=[\'"][^\'"]*[\'"])?>Experience the Wild Heart of Manu</h2>',
        r'<h2 class="h2" style="font-size: 2.2rem; margin-bottom: 20px; color: var(--forest-dark);">Experience the Wild Heart of Manu</h2>',
        nc,
        flags=re.I
    )
    
    # 2. In overview paragraph (Short Description)
    nc = re.sub(
        r'(<p style=[\'"][^\'"]*font-size:\s*1\.1rem;[^\'"]*)color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.85\);?([^\'"]*[\'"])',
        r'\1color: var(--earth-text);\2',
        nc,
        flags=re.I
    )
    
    # 3. In itinerary list day cards:
    # Change background:var(--f); to background:var(--sand-card);
    # Change color:rgba(255,255,255,0.85) to color:var(--earth-text)
    # Change border:1px solid rgba(255,255,255,0.08) to border:1px solid var(--sand-border); box-shadow: var(--shadow-eco);
    nc = re.sub(
        r'(<div class=[\'"]itinerary-list[\'"][\s\S]*?</div>\s*</div>\s*</div>)',
        lambda m: re.sub(
            r'color:\s*rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.85\);?',
            'color: var(--earth-text);',
            re.sub(
                r'border:1px solid rgba\(255,255,255,0\.08\);',
                'border: 1px solid var(--sand-border); box-shadow: var(--shadow-eco);',
                m.group(1)
            )
        ),
        nc
    )
    
    # 4. In sidebar booking card:
    # Make background: var(--forest-card);
    nc = re.sub(
        r'(style=[\'"][^\'"]*position:\s*sticky;\s*top:\s*100px;[^\'"]*)background:\s*var\(--f\);?([^\'"]*[\'"])',
        r'\1background: var(--forest-card); color: #FFFFFF;\2',
        nc,
        flags=re.I
    )
    
    if nc != c:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(nc)
        print(f'Updated tour contrast in: {f}')
        updated_count += 1

print(f'Done. Updated {updated_count} files.')
