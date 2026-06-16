import os
import re
import json

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
                date = date.strip()
                title = title.strip()
                img = img.strip()
                if img.startswith('../../'):
                    img = img[3:]
                elif img.startswith('../'):
                    pass
                else:
                    img = '../' + img
                metadata[folder_name] = {'date': date, 'title': title, 'img': img}
    return metadata

en_meta = extract_metadata_from_blog_index('')
es_meta = extract_metadata_from_blog_index('es')
if not es_meta:
    es_meta = en_meta

def process_articles(lang_prefix, meta_dict):
    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if not os.path.exists(path):
            continue
            
        data = meta_dict.get(bf)
        if not data:
            print(f"Warning: No metadata found for {bf} in {lang_prefix}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        bg_img = "../wp-content/uploads/2021/04/MachuWasi_Lake-1-scaled.jpg"
        if lang_prefix == "es":
            bg_img = "../../wp-content/uploads/2021/04/MachuWasi_Lake-1-scaled.jpg"
            
        # Update Hero background
        content = re.sub(r'(<section class="in-hero" style="background-image:\s*url\()[\'"]?[^\)]+[\'"]?(\);?">)', rf'\g<1>\'{bg_img}\'\g<2>', content)
        
        # Update Hero Title
        content = re.sub(r'(<h1 class="h1"[^>]*>).*?(</h1>)', rf'\g<1>{data["title"]}\g<2>', content, count=1, flags=re.DOTALL)
        
        # We need to remove the existing <div class="article-meta"> completely if it exists
        content = re.sub(r'<div class="article-meta">.*?</div>\s*<!-- Content -->', '<!-- Content -->', content, flags=re.DOTALL)
        
        author_name = "Anna Ashley" if "packing-list" in bf else "Hidden Jungle Cusco"
        
        meta_html = f"""
    <!-- Added User Meta -->
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:32px; font-size:1rem; color:rgba(255,255,255,.6); font-family:'Inter',sans-serif">
      <i class="fas fa-user-circle" style="font-size:1.8rem; color:rgba(255,255,255,.8)"></i>
      <span>Published by: <strong style="color:var(--w)">{author_name}</strong></span>
      <span style="margin:0 12px; color:rgba(255,255,255,.2)">|</span>
      <i class="far fa-calendar-alt"></i>
      <span>{data["date"]}</span>
    </div>
    <img src="{data["img"]}" alt="{data["title"]}" style="width:100%; border-radius:16px; margin-bottom:48px; box-shadow:0 12px 40px rgba(0,0,0,.4); object-fit:cover; max-height:600px">
"""
        
        # Check if we've already injected it
        if "Published by:" not in content:
            # We inject BEFORE <div class="article-body"> or <div class="tour-rich-text">
            if '<div class="article-body">' in content:
                content = re.sub(r'(<div class="article-body">)', lambda m: meta_html + '\n    ' + m.group(1), content, count=1)
            elif '<div class="tour-rich-text">' in content:
                content = re.sub(r'(<div class="tour-rich-text">)', lambda m: meta_html + '\n  ' + m.group(1), content, count=1)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

    print(f"Updated {updated} files in '{lang_prefix}'")

process_articles('', en_meta)
process_articles('es', es_meta)
