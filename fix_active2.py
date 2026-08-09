import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

def determine_active_menu(filepath):
    rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
    dirname = os.path.dirname(rel_path)
    
    if dirname == "":
        return "home"
    if dirname == "about-2":
        return "about-2"
    if dirname == "departures":
        return "departures"
    if dirname == "news-and-gallery":
        return "news-and-gallery"
    if dirname == "blog":
        return "blog"
    if dirname in ["contact", "book-now"]:
        return "contact"
    
    # All tour pages
    tour_keywords = [
        'guided-tours', '3-day', '4-day', '5-day', '6-day', '8-day', 
        'rainforest-road-trip', 'wildlife-tours-from-cusco', 'amazon-expedition'
    ]
    if any(kw in dirname for kw in tour_keywords):
        return "guided-tours"
        
    return "home"

def set_active_menu(content, active_item):
    nav_match = re.search(r'<nav class="nm".*?</nav>', content, re.DOTALL)
    if not nav_match: return content
    nav_content = nav_match.group(0)
    
    # Remove all class="on" globally inside <nav>
    nav_content = nav_content.replace(' class="on"', '')
    nav_content = nav_content.replace('class="on"', '')
    
    # Add class="on" to the correct item
    if active_item == 'home':
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
        nav_content = re.sub(r'<a href="([^"]*guided-tours/index\.html)">Guided Tours', r'<a href="\1" class="on">Guided Tours', nav_content)
    elif active_item == 'contact':
        nav_content = re.sub(r'<a href="([^"]*contact[^"]*)"[^>]*>Book Now</a>', r'<a href="\1" class="nb on">Book Now</a>', nav_content)
    
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
