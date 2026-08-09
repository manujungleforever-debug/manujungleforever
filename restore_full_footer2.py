import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER"
hjc_index = os.path.join(base_dir, "www.hiddenjunglecusco.com", "index.html")

with open(hjc_index, 'r', encoding='utf-8') as f:
    hjc_content = f.read()

# Extract full footer
footer_match = re.search(r'(<footer class="ft">.*?</footer>)', hjc_content, re.DOTALL)
if not footer_match:
    print("Could not find full footer")
    exit(1)

full_footer = footer_match.group(1)

# Now, apply Manu Jungle Forever branding to the footer
full_footer = full_footer.replace("Hidden Jungle Cusco", "Manu Jungle Forever")
full_footer = full_footer.replace("wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png", "assets/img/logo.png")
full_footer = full_footer.replace("Hidden Jungle Cusco – La Casa Escondida 17800", "Manu Jungle Forever - Fitzcarrald 17800")
full_footer = full_footer.replace("+51 979 808 013", "+51 901 525 679")
full_footer = full_footer.replace("+51 923 289 231", "+51 901 525 679")
full_footer = full_footer.replace("tel:+51979808013", "tel:+51901525679")
full_footer = full_footer.replace("tel:+51923289231", "tel:+51901525679")
full_footer = full_footer.replace("discover@hiddenjunglecusco.com", "discover@manujungleforever.com")
full_footer = full_footer.replace("https://www.facebook.com/hiddenjunglecusco", "https://www.facebook.com/manujungleforever")
full_footer = full_footer.replace("https://www.instagram.com/hiddenjunglecusco/?hl=en", "https://www.instagram.com/manujungleforever/")
# Remove style block from footer (it's already in new.css)
full_footer = re.sub(r'<style>.*?</style>', '', full_footer, flags=re.DOTALL)

# Now inject this full_footer everywhere
mjf_dir = os.path.join(base_dir, "www.manujungleforever.com")
html_files = glob.glob(os.path.join(mjf_dir, "**", "*.html"), recursive=True)

def get_adapted_footer(depth):
    if depth == 0:
        return full_footer
    else:
        prefix = "../" * depth
        def replacer(m):
            attr = m.group(1)
            quote = m.group(2)
            val = m.group(3)
            if val.startswith(('http', 'mailto:', 'tel:', '#', '../')):
                return f"{attr}={quote}{val}{quote}"
            elif val.startswith('/'):
                return f"{attr}={quote}{val}{quote}"
            else:
                return f"{attr}={quote}{prefix}{val}{quote}"
        return re.sub(r'(href|src)=([\'"])(.*?)([\'"])', replacer, full_footer)

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, mjf_dir)
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

print(f"Force restored FULL EXACT footer in {count} HTML files.")
