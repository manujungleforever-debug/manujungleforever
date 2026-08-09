import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

with open(os.path.join(base_dir, "index.html"), 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract full footer from index.html
footer_match = re.search(r'(<footer class="ft">.*?</footer>)', index_html, re.DOTALL)
if not footer_match:
    print("Footer not found in index.html!")
    exit(1)

root_footer = footer_match.group(1)

# Now iterate over all HTML files
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to adapt the footer links based on the depth
    # If the file is in root (e.g. index.html), use root_footer.
    # If the file is in a subdirectory (e.g. contact/index.html), add ../ to hrefs and srcs.
    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    if depth == 0:
        adapted_footer = root_footer
    else:
        prefix = "../" * depth
        
        # Replace href="something" with href="../something"
        # EXCEPT for external links (http), mailto:, tel:, #, and already relative paths.
        def replacer(m):
            attr = m.group(1) # href or src
            quote = m.group(2) # " or '
            val = m.group(3)
            
            if val.startswith(('http', 'mailto:', 'tel:', '#', '../')):
                return f"{attr}={quote}{val}{quote}"
            elif val.startswith('/'):
                # Assuming / is root, we can replace it or just leave it
                return f"{attr}={quote}{val}{quote}"
            else:
                return f"{attr}={quote}{prefix}{val}{quote}"
                
        adapted_footer = re.sub(r'(href|src)=([\'"])(.*?)([\'"])', replacer, root_footer)

    # Now replace whatever is currently between <footer class="ft"> and </footer>
    # Wait, some pages might just have </footer> if <footer class="ft"> got deleted?
    # Let's check if the page has `<footer class="ft">`
    if '<footer class="ft">' in content:
        new_content = re.sub(r'<footer class="ft">.*?</footer>', adapted_footer, content, flags=re.DOTALL)
    elif '</footer>' in content:
        # If it only has </footer>, it's very broken. Let's find </footer> and replace it and any garbage before it?
        # Actually let's just replace from </main> to </footer> if <footer class="ft"> is missing.
        new_content = re.sub(r'</main>.*?</footer>', f'</main>\n  {adapted_footer}', content, flags=re.DOTALL)
    else:
        # If no footer at all, append before <a class="wa"
        # or before </body>
        new_content = content.replace('</body>', f'{adapted_footer}\n</body>')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Restored footer in {filepath}")

print("Footer restoration complete.")
