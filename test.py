import os, re
with open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

nav_match = re.search(r'<nav class="nm"[^>]*>.*?</nav>', c, re.DOTALL)
nav_html = nav_match.group(0)
print('Before cleanup:')
print(nav_html[:200])

# Remove any existing 'on' class from links
nav_html = re.sub(r'class="on"', '', nav_html)
nav_html = re.sub(r'class="nb on"', 'class="nb"', nav_html)
# Remove empty class="" left over
nav_html = nav_html.replace('class=""', '')

print('\nAfter cleanup class="on":')
print(nav_html[:200])

nav_html = re.sub(r'\bon\b\s*', '', nav_html) # from my later change? No, my later change was inside add_on_class
print('\nAfter \bon\b cleanup:')
print(nav_html[:200])
