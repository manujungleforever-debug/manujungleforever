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

def clean_elementor_junk(lang_prefix):
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Strip duplicated H1 titles
        content = re.sub(r'<div class="tour-rich-text-custom">\s*<h1 class="elementor-heading-title[^>]*>.*?</h1>\s*</div>', '', content, flags=re.DOTALL)
        
        # Strip post navigation and posts container
        content = re.sub(r'<div class="tour-rich-text-custom">\s*<div class="elementor-post-navigation">.*?</article>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="elementor-post-navigation">.*?</article>\s*</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
            print(f"Cleaned {path}")

    print(f"Cleaned {updated} files in '{lang_prefix}'")

clean_elementor_junk('')
clean_elementor_junk('es')
