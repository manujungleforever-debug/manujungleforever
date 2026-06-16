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

def fix_articles():
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        bg_url = "../wp-content/uploads/2022/12/five-reasons-to-visit-manu-national-park.webp"
        
        # Replace the background image
        content = re.sub(r'(<section class="in-hero"[^>]*background-image:\s*url\()[^)]+(\))', rf"\g<1>'{bg_url}'\g<2>", content)
        
        # Also let's make sure background-size is cover, since that creates a "banner that covers the whole width"
        # The CSS `.in-hero` already has `background-size: cover;` natively.
        
        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"Fixed {path}")

    print(f"Fixed {updated} English files.")

fix_articles()
