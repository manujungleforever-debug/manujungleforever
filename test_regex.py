import re

fpath = 'www.hiddenjunglecusco.com/3-day-wildlife-quest-machu-wasi/index.html'
with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

pattern = r'<div class="cx">\s*<div class="fg">\s*<div>\s*<a[^>]*><img[^>]*HiddenJungleCusco_Logo_TextSeal_3Color.*?</footer>'
match = re.search(pattern, c, flags=re.DOTALL)
if match:
    print('Found length:', len(match.group(0)))
    
    # Let's replace it and see what it looks like
    from fix_layout_and_nav import get_new_footer
    new_footer = get_new_footer('../')
    new_c = c[:match.start()] + new_footer + c[match.end():]
    
    with open(fpath, 'w', encoding='utf-8') as f2:
        f2.write(new_c)
    print('Wrote updated content to file')
else:
    print('No match!')
