import glob
import re

html_files = glob.glob('www.manujungleforever.com/**/*.html', recursive=True)
count_div = 0
count_script_src = 0
count_script_load = 0

div_pat = re.compile(r'<div\s+id=[\'"]tsparticles-footer[\'"][^>]*>\s*</div>\s*', re.I)
script_src_pat = re.compile(r'<script\s+src=[\'"][^\'"]*particles\.min\.js[\'"]\s*></script>\s*', re.I)
script_load_pat = re.compile(r'<script>\s*tsParticles\.load\(\s*[\'"]tsparticles-footer[\'"][\s\S]*?\);\s*</script>\s*', re.I)

for f in html_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    new_content = content
    if div_pat.search(new_content):
        new_content = div_pat.sub('', new_content)
        count_div += 1
    if script_src_pat.search(new_content):
        new_content = script_src_pat.sub('', new_content)
        count_script_src += 1
    if script_load_pat.search(new_content):
        new_content = script_load_pat.sub('', new_content)
        count_script_load += 1
        
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        print(f'Cleaned particles in: {f}')

print(f'Total: {count_div} divs removed, {count_script_src} script tags removed, {count_script_load} load calls removed.')
