import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

with open(os.path.join(base_dir, "index.html"), 'r', encoding='utf-8') as f:
    root_footer = re.search(r'(<footer class="ft">.*?</footer>)', f.read(), re.DOTALL).group(1)

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

count = 0
for filepath in html_files:
    # skip index.html as it is the source of truth
    if filepath == os.path.join(base_dir, "index.html"):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if it needs ../ (if it's in a subdirectory)
    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    current_footer = adapted_footer if depth > 0 else root_footer
    
    if '<footer class="ft">' in content:
        new_content = re.sub(r'<footer class="ft">.*?</footer>', current_footer, content, flags=re.DOTALL)
    elif '</footer>' in content:
        new_content = re.sub(r'</main>.*?</footer>', f'</main>\n  {current_footer}', content, flags=re.DOTALL)
    else:
        new_content = content.replace('</body>', f'{current_footer}\n</body>')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Force updated footer in {filepath}")

print(f"Force footer replacement complete. Updated {count} files.")
