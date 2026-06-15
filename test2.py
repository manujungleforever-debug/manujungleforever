import os, re
with open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

nav_match = re.search(r'<nav class="nm"[^>]*>.*?</nav>', c, re.DOTALL)
if nav_match:
    nav_html = nav_match.group(0)
    orig_nav_html = nav_html
    
    # Global cleanup
    nav_html = re.sub(r'\bon\b\s*', '', nav_html)
    nav_html = re.sub(r'class="\s*"', '', nav_html)
    nav_html = re.sub(r'\s+', ' ', nav_html)
    
    target_href = 'index.html'
    pattern = rf'<a\s[^>]*href="[^"]*?{re.escape(target_href)}"[^>]*>'
    
    def add_on_class(match):
        tag = match.group(0)
        if 'class="' in tag:
            return re.sub(r'class="([^"]*)"', r'class="\1 on"', tag)
        else:
            return tag.replace('<a ', '<a class="on" ')
    
    nav_html = re.sub(pattern, add_on_class, nav_html)
    
    if nav_html != orig_nav_html:
        c = c.replace(orig_nav_html, nav_html)
        print('Changed! Length diff:', len(nav_html) - len(orig_nav_html))
    else:
        print('NO CHANGE!')
    
    print('First 500 chars of new nav:')
    print(nav_html[:500])
