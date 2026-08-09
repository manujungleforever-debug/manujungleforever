import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# The menu items and their associated paths
menu_mapping = {
    'home': ['index.html', 'index.php'],
    'about-2': ['about-2'],
    'departures': ['departures'],
    'news-and-gallery': ['news-and-gallery'],
    'blog': ['blog'],
    'guided-tours': [
        'guided-tours', 
        '3-day', '4-day', '5-day', '6-day', '8-day', 'rainforest-road-trip',
        'wildlife-tours-from-cusco'
    ],
    'contact': ['contact', 'book-now']
}

def determine_active_menu(filepath):
    # relative to base_dir
    rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
    for item, keywords in menu_mapping.items():
        if any(kw in rel_path for kw in keywords):
            return item
    return 'home' # default to home if not matched

def set_active_menu(content, active_item):
    # First, remove class="on" from ALL main nav links
    # The links are in <nav class="nm"
    
    # regex to match any link in the nav and remove class="on"
    nav_match = re.search(r'<nav class="nm".*?</nav>', content, re.DOTALL)
    if not nav_match: return content
    
    nav_content = nav_match.group(0)
    
    # Remove class="on" from all links
    nav_content = re.sub(r' class="on"', '', nav_content)
    
    # Now add class="on" to the correct link
    if active_item == 'home':
        nav_content = re.sub(r'(<a href="[^"]*index\.html">Home</a>)', r'<a href="\g<1>".replace(">Home", " class=\"on\">Home")', nav_content)
        # using a safer replacement:
        nav_content = re.sub(r'<a href="([^"]*index\.html)">Home</a>', r'<a href="\1" class="on">Home</a>', nav_content)
    elif active_item == 'about-2':
        nav_content = re.sub(r'<a href="([^"]*about-2[^"]*)">About Us</a>', r'<a href="\1" class="on">About Us</a>', nav_content)
    elif active_item == 'departures':
        nav_content = re.sub(r'<a href="([^"]*departures[^"]*)">Departures</a>', r'<a href="\1" class="on">Departures</a>', nav_content)
    elif active_item == 'news-and-gallery':
        nav_content = re.sub(r'<a href="([^"]*news-and-gallery[^"]*)">Gallery</a>', r'<a href="\1" class="on">Gallery</a>', nav_content)
    elif active_item == 'blog':
        nav_content = re.sub(r'<a href="([^"]*blog[^"]*)">Blog</a>', r'<a href="\1" class="on">Blog</a>', nav_content)
    elif active_item == 'guided-tours':
        nav_content = re.sub(r'<a href="([^"]*guided-tours[^"]*)">Guided Tours', r'<a href="\1" class="on">Guided Tours', nav_content)
    
    # replace back into content
    content = content[:nav_match.start()] + nav_content + content[nav_match.end():]
    return content


for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            active = determine_active_menu(path)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            orig = content
            content = set_active_menu(content, active)
            
            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Set active to '{active}' in: {path}")

print("Done fixing active menu links.")
