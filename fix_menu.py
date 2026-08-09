import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# Regex for desktop Guided Tours block
# It captures the whole <div class="hd">...</div> block
# Since the links inside change depending on prefix (../), we must capture it via regex
desktop_tours_re = re.compile(r'(\s*<div class="hd"><a href="[^"]*?guided-tours/index\.html">Guided Tours.*?</ul>\s*</div>)', re.DOTALL)

# Regex for desktop Blog link
desktop_blog_re = re.compile(r'(\s*<a href="[^"]*?blog/index\.html">Blog</a>)')

# Regex for desktop Translator block
desktop_translator_re = re.compile(r'(\s*<div class="ls-custom".*?</ul>\s*</div>)', re.DOTALL)

# Regex for desktop Book Now link
desktop_booknow_re = re.compile(r'(\s*<a href="[^"]*?contact/index\.html" class="nb">Book Now</a>)')

# Mobile Guided Tours block
mobile_tours_re = re.compile(r'(\s*<li><button class="mb" id="mbt">Guided Tours.*?</ul>\s*</li>)', re.DOTALL)

# Mobile Blog link
mobile_blog_re = re.compile(r'(\s*<li><a href="[^"]*?blog/index\.html">Blog</a></li>)')

# Footer menu
footer_menu_re = re.compile(r'(<ul class="fli">.*?</ul>)', re.DOTALL)


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_content = content
    
    # 1. Move Desktop Guided Tours to after Blog
    m_tours = desktop_tours_re.search(content)
    m_blog = desktop_blog_re.search(content)
    if m_tours and m_blog:
        tours_block = m_tours.group(1)
        # Remove tours block from its original position
        content = content.replace(tours_block, '', 1)
        # Insert after blog
        m_blog = desktop_blog_re.search(content) # search again since indices changed
        if m_blog:
            content = content[:m_blog.end()] + tours_block + content[m_blog.end():]
            
    # 2. Move Desktop Translator to after Book Now
    m_trans = desktop_translator_re.search(content)
    m_book = desktop_booknow_re.search(content)
    if m_trans and m_book:
        trans_block = m_trans.group(1)
        # Remove trans block
        content = content.replace(trans_block, '', 1)
        # Insert after Book Now
        m_book = desktop_booknow_re.search(content)
        if m_book:
            content = content[:m_book.end()] + trans_block + content[m_book.end():]

    # 3. Move Mobile Guided Tours to after Blog
    m_mob_tours = mobile_tours_re.search(content)
    m_mob_blog = mobile_blog_re.search(content)
    if m_mob_tours and m_mob_blog:
        mob_tours_block = m_mob_tours.group(1)
        content = content.replace(mob_tours_block, '', 1)
        m_mob_blog = mobile_blog_re.search(content)
        if m_mob_blog:
            content = content[:m_mob_blog.end()] + mob_tours_block + content[m_mob_blog.end():]
            
    # 4. Fix Footer menu order
    m_footer = footer_menu_re.search(content)
    if m_footer:
        footer_block = m_footer.group(1)
        # Extract the list items
        # <li><a href="...">...</a></li>
        lis = re.findall(r'<li>.*?</li>', footer_block)
        
        # Identify tours and blog
        tours_li = None
        for li in lis:
            if 'guided-tours' in li:
                tours_li = li
                break
                
        if tours_li:
            lis.remove(tours_li)
            # Find blog index
            blog_idx = -1
            for i, li in enumerate(lis):
                if 'blog/index' in li:
                    blog_idx = i
                    break
            if blog_idx != -1:
                lis.insert(blog_idx + 1, tours_li)
                
            new_footer_block = '<ul class="fli">' + ''.join(lis) + '</ul>'
            content = content.replace(footer_block, new_footer_block)
            
    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

updated = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            if process_file(path):
                updated += 1
                
print(f"Updated menu in {updated} files.")
