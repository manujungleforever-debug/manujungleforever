import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

# Read the correct footer from about-2/index2.html
with open(os.path.join(base_dir, "about-2", "index2.html"), 'r', encoding='utf-8') as f:
    about_html = f.read()

footer_match = re.search(r'(<footer class="ft">.*?</footer>)', about_html, re.DOTALL)
if not footer_match:
    print("Could not find footer in about-2/index2.html")
    exit(1)

# This footer already has ../ in its paths
raw_footer = footer_match.group(1)

# Convert it to a "root" footer by stripping ../
root_footer = raw_footer.replace('href="../', 'href="').replace('src="../', 'src="')

# Function to fix paths based on depth
def get_adapted_footer(depth):
    if depth == 0:
        return root_footer
    else:
        prefix = "../" * depth
        def replacer(m):
            attr = m.group(1)
            quote = m.group(2)
            val = m.group(3)
            if val.startswith(('http', 'mailto:', 'tel:', '#')):
                return f"{attr}={quote}{val}{quote}"
            elif val.startswith('/'):
                return f"{attr}={quote}{val}{quote}"
            else:
                return f"{attr}={quote}{prefix}{val}{quote}"
        return re.sub(r'(href|src)=([\'"])(.*?)([\'"])', replacer, root_footer)

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    current_footer = get_adapted_footer(depth)
    
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

print(f"Force restored FULL footer in {count} HTML files.")
