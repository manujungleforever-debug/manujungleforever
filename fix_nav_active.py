import os
import re

base_dir = "www.manujungleforever.com"

# Dictionary mapping folder names (or file names) to the link text or href that should be active
# E.g. if we are in 'about-2' folder, the 'About Us' link should have class="on"
nav_mapping = {
    'index.html': 'Home',
    'guided-tours': 'Guided Tours',
    'about-2': 'About Us',
    'departures': 'Departures',
    'news-and-gallery': 'Gallery',
    'blog': 'Blog',
    'contact': 'Contact'
}

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # First, strip class="on" from ALL links in the nav menu to start clean
            # The nav menu is within <nav class="nm" aria-label="Main navigation"> ... </nav>
            nav_match = re.search(r'<nav class="nm" aria-label="Main navigation">(.*?)</nav>', content, flags=re.DOTALL)
            if not nav_match:
                continue
            
            nav_html = nav_match.group(1)
            # Remove class="on"
            nav_html = re.sub(r'\bclass="on"\s*', '', nav_html)
            nav_html = re.sub(r'\s+class="on"', '', nav_html)
            nav_html = nav_html.replace('class="on"', '')
            
            # Determine which folder we are in
            rel_dir = os.path.relpath(root, base_dir)
            active_target = None
            
            if rel_dir == '.':
                if file == 'index.html':
                    active_target = 'Home'
            else:
                top_folder = rel_dir.split(os.sep)[0]
                if top_folder in nav_mapping:
                    active_target = nav_mapping[top_folder]
                else:
                    # If it's a specific tour, maybe highlight 'Guided Tours' or nothing
                    active_target = 'Guided Tours'
            
            # Now inject class="on" to the active_target
            if active_target:
                if active_target == 'Guided Tours':
                    # Guided tours is special because it has a caret icon: <a href="guided-tours/index.html">Guided Tours <i class="fas fa-caret-down"></i></a>
                    # We just find >Guided Tours and replace the a tag
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*guided-tours/index\.html"[^>]*)>', r'\1 class="on">', nav_html)
                elif active_target == 'Home':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*index\.html"[^>]*)>Home</a>', r'\1 class="on">Home</a>', nav_html)
                elif active_target == 'About Us':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*about-2/index\.html"[^>]*)>About Us</a>', r'\1 class="on">About Us</a>', nav_html)
                elif active_target == 'Departures':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*departures/index\.html"[^>]*)>Departures</a>', r'\1 class="on">Departures</a>', nav_html)
                elif active_target == 'Gallery':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*news-and-gallery/index\.html"[^>]*)>Gallery</a>', r'\1 class="on">Gallery</a>', nav_html)
                elif active_target == 'Blog':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*blog/index\.html"[^>]*)>Blog</a>', r'\1 class="on">Blog</a>', nav_html)
                elif active_target == 'Contact':
                    nav_html = re.sub(r'(<a[^>]*href="[^"]*contact/index\.html"[^>]*)>Contact</a>', r'\1 class="on">Contact</a>', nav_html)

            # Replace the old nav with the new nav
            content = content[:nav_match.start(1)] + nav_html + content[nav_match.end(1):]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

print("Active nav classes updated successfully.")
