import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
with open(os.path.join(base_dir, "index.html"), 'r', encoding='utf-8') as f:
    root_footer = re.search(r'(<footer class="ft">.*?</footer>)', f.read(), re.DOTALL).group(1)

# fix paths for 1 level deep
def replacer(m):
    attr = m.group(1)
    quote = m.group(2)
    val = m.group(3)
    if val.startswith(('http', 'mailto:', 'tel:', '#', '../')):
        return f"{attr}={quote}{val}{quote}"
    elif val.startswith('/'):
        return f"{attr}={quote}{val}{quote}"
    else:
        return f"{attr}={quote}../{val}{quote}"

adapted_footer = re.sub(r'(href|src)=([\'"])(.*?)([\'"])', replacer, root_footer)

target = os.path.join(base_dir, "book-now", "index.html")
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(r'<footer class="ft">.*?</footer>', adapted_footer, content, flags=re.DOTALL)

with open(target, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Forcibly replaced footer in book-now")
