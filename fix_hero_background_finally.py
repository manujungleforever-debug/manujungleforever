import os
import re

base_dir = 'www.hiddenjunglecusco.com'

blog_folders = [
    'discovering-the-mysteries-of-the-peruvian-amazon',
    'amazon-rainforest-tour-to-manu-national-park-from-cusco',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026',
    'climate-change-manu-national-park-peru',
    'how-tourism-helps-the-manu-national-park',
    'everything-you-need-to-know-before-visiting-machu-picchu',
    'peru-travel-tips',
    'packing-list-for-your-trip-to-the-peruvian-amazon',
    'five-reasons-to-visit-manu-national-park',
    'ten-days-in-peru'
]

def fix_articles(lang_prefix):
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        bg_url = "../wp-content/uploads/2021/04/MachuWasi_Lake-1-scaled.jpg"
        if lang_prefix == "es":
            bg_url = "../../wp-content/uploads/2021/04/MachuWasi_Lake-1-scaled.jpg"
            
        # Robust regex for background-image in .in-hero
        content = re.sub(r'(<section class="in-hero"[^>]*background-image:\s*url\()[^)]+(\))', rf"\g<1>'{bg_url}'\g<2>", content)

        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"Fixed {path}")

    print(f"Fixed {updated} files in '{lang_prefix}'")

fix_articles('')
fix_articles('es')
