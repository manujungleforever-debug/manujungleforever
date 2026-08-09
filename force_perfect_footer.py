import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
blog_index = os.path.join(base_dir, "blog", "index.html")

with open(blog_index, 'r', encoding='utf-8') as f:
    blog_content = f.read()

# Extract perfect footer
footer_match = re.search(r'(<footer class="ft">.*?</footer>)', blog_content, re.DOTALL)
if not footer_match:
    print("Could not find perfect footer in blog/index.html")
    exit(1)

perfect_footer_raw = footer_match.group(1)

# The raw footer has paths relative to depth=1 (e.g. `../assets/img/logo.png`)
# We need to normalize it to depth=0 (e.g. `assets/img/logo.png`) first
perfect_footer_base = perfect_footer_raw.replace('../assets', 'assets')
perfect_footer_base = perfect_footer_base.replace('../index.html', 'index.html')

html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

def get_adapted_footer(depth):
    if depth == 0:
        return perfect_footer_base
    else:
        prefix = "../" * depth
        # We need to add the prefix only to relative internal links
        # `assets/img...` -> `../assets/img...`
        # `index.html` -> `../index.html`
        adapted = perfect_footer_base.replace('src="assets', f'src="{prefix}assets')
        adapted = adapted.replace('href="index.html', f'href="{prefix}index.html')
        return adapted

count = 0
for filepath in html_files:
    # Skip blog/index.html to leave it exactly as it is (ground truth)
    if os.path.samefile(filepath, blog_index):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    current_footer = get_adapted_footer(depth)
    
    if '<footer class="ft">' in content:
        new_content = re.sub(r'<footer class="ft">.*?</footer>', current_footer, content, flags=re.DOTALL)
    elif '</footer>' in content:
        new_content = re.sub(r'</main>.*?</footer>', f'</main>\n{current_footer}', content, flags=re.DOTALL)
    else:
        new_content = content.replace('</body>', f'{current_footer}\n</body>')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected perfect footer into: {filepath}")
        count += 1

print(f"Force restored perfect footer in {count} HTML files.")
