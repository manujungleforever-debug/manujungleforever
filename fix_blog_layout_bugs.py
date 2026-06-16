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

def extract_metadata_from_blog_index(lang_prefix):
    metadata = {}
    paths = [
        os.path.join(base_dir, lang_prefix, 'blog/index.html'),
        os.path.join(base_dir, lang_prefix, 'blog/page/2/index.html')
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            cards = re.findall(r'<a href="([^"]+)" class="blog-card[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*>.*?<p class="blog-date">.*?</i>(.*?)</p>\s*<h2>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
            for url, img, date, title in cards:
                folder_name = url.split('/')[-2] if '/' in url else url
                img = img.strip()
                if img.startswith('../../'):
                    img = img[3:]
                elif img.startswith('../'):
                    pass
                else:
                    img = '../' + img
                metadata[folder_name] = {'img': img}
    return metadata

en_meta = extract_metadata_from_blog_index('')
es_meta = extract_metadata_from_blog_index('es')
if not es_meta:
    es_meta = en_meta

def fix_articles(lang_prefix, meta_dict):
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        data = meta_dict.get(bf)
        if not data:
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Fix the broken background image and set it to the article's own featured image
        # The broken background image currently looks like: style="background-image: url(\'../wp-content/uploads/2021/04/MachuWasi_Lake-1-scaled.jpg\');"
        # We want to replace it with url('../wp-content/uploads/2022/10/FullSizeRender.jpg')
        bg_img = data["img"]
        if lang_prefix == "es" and bg_img.startswith('../'):
            bg_img = "." + bg_img # make it ../../
            
        # Regex to find ANY background image in .in-hero and replace it with the correct one
        content = re.sub(r'(<section class="in-hero" style="background-image:\s*url\()\\\\?[\'"]?[^\)]+[\'"]?(\);?">)', rf"\g<1>'{bg_img}'\g<2>", content)
        
        # 2. Remove the duplicated featured image block I injected under the author
        # It looks like: <img src="..." alt="..." style="width:100%; border-radius:16px; margin-bottom:48px; box-shadow:0 12px 40px rgba(0,0,0,.4); object-fit:cover; max-height:600px">
        content = re.sub(r'<img src="[^"]+" alt="[^"]+" style="width:100%; border-radius:16px; margin-bottom:48px; box-shadow:0 12px 40px rgba\(0,0,0,\.4\); object-fit:cover; max-height:600px">\s*', '', content, count=1)
        
        if content != original_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    print(f"Fixed {updated} files in '{lang_prefix}'")

fix_articles('', en_meta)
fix_articles('es', es_meta)
