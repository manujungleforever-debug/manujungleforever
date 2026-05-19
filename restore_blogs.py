import os
import zipfile
import re
from bs4 import BeautifulSoup

articles = [
    "why-visit-the-manu-national-park",
    "five-reasons-to-visit-manu-national-park",
    "how-tourism-helps-the-manu-national-park",
    "off-the-beaten-path-places-to-visit-from-cusco",
    "packing-list-for-your-trip-to-the-peruvian-amazon",
    "peru-travel-tips",
    "ten-days-in-peru",
    "the-sacred-valley-of-the-incas-a-comprehensive-guide",
    "everything-you-need-to-know-before-visiting-machu-picchu"
]

z = zipfile.ZipFile('hts-cache/new.zip', 'r')

for folder in articles:
    print(f"Fixing {folder}...")
    try:
        html = z.read(f"https://www.hiddenjunglecusco.com/{folder}/")
    except KeyError:
        print(f"Could not find {folder} in zip")
        continue

    soup = BeautifulSoup(html, 'html.parser')
    
    content_block = soup.select_one(".elementor-widget-theme-post-content")
    if content_block:
        rich_html = content_block.decode_contents()
    else:
        editors = soup.select(".elementor-widget-text-editor .elementor-widget-container")
        rich_html = "".join([e.decode_contents() for e in editors])
        
    if not rich_html.strip():
        print(f"Still no content for {folder}")
        continue
        
    path = f"www.hiddenjunglecusco.com/{folder}/index.html"
    if not os.path.exists(path):
        print(f"File {path} does not exist!")
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        current_content = f.read()
        
    # Find the empty <article class="article-content"> and replace it
    # We'll use regex to replace everything between <article class="article-content"> and </article>
    
    new_content = re.sub(
        r'(<article class="article-content">).*?(</article>)', 
        r'\1\n' + rich_html.replace('\\', '\\\\') + r'\n\2', 
        current_content, 
        flags=re.DOTALL
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully restored rich text for {folder}")

