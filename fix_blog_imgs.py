import os

search_dir = 'www.hiddenjunglecusco.com'

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

updated_files = []

for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                
                # Fix image paths everywhere
                if '..../wp-content' in new_content:
                    new_content = new_content.replace('..../wp-content', '../wp-content')
                
                # Fix active menu in blog folders
                is_blog_post = False
                for b in blog_folders:
                    if f"\\{b}\\" in path or f"/{b}/" in path.replace('\\', '/'):
                        is_blog_post = True
                        break
                
                if is_blog_post:
                    # Remove active class from Guided Tours
                    new_content = new_content.replace('<a class="on" href="../guided-tours/index.html">', '<a href="../guided-tours/index.html">')
                    new_content = new_content.replace('<a class="on" href="../../guided-tours/index.html">', '<a href="../../guided-tours/index.html">')
                    
                    # Add active class to Blog (only in the top nav, usually followed by Book Now)
                    # For English:
                    new_content = new_content.replace('<a href="../blog/index.html">Blog</a> <a href="../contact/index.html" class="nb">', '<a class="on" href="../blog/index.html">Blog</a> <a href="../contact/index.html" class="nb">')
                    new_content = new_content.replace('<a href="../blog/index.html" >Blog</a> <a href="../contact/index.html" class="nb">', '<a class="on" href="../blog/index.html">Blog</a> <a href="../contact/index.html" class="nb">')
                    
                    # For Spanish (adjust if needed):
                    new_content = new_content.replace('<a href="../../es/blog/index.html">Blog</a> <a href="../../es/contact/index.html" class="nb">', '<a class="on" href="../../es/blog/index.html">Blog</a> <a href="../../es/contact/index.html" class="nb">')
                    new_content = new_content.replace('<a href="../../es/blog/index.html" >Blog</a> <a href="../../es/contact/index.html" class="nb">', '<a class="on" href="../../es/blog/index.html">Blog</a> <a href="../../es/contact/index.html" class="nb">')
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    updated_files.append(path)
            except Exception as e:
                pass

print(f"Updated {len(updated_files)} files.")
