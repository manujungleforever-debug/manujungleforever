import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

desktop_nav_template = """<nav class="nm" aria-label="Main navigation">
    <a href="{rel}index.html" >Home</a>
    <a href="{rel}about-2/index.html">About Us</a>
    <a href="{rel}departures/index.html">Departures</a>
    <a href="{rel}news-and-gallery/index.html">Gallery</a>
    <a href="{rel}blog/index.html">Blog</a>
    <div class="hd"><a href="{rel}guided-tours/index.html">Guided Tours <i class="fas fa-caret-down"></i></a>
      <ul class="dm">
        <span class="dh"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="{rel}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{rel}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{rel}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="{rel}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="{rel}8-day-wildlife-photography-tour/index.html">Wildlife Photography &ndash; 8 Days</a></li>
        
        <span class="dh"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="{rel}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="{rel}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{rel}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="{rel}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{rel}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
    <a href="{rel}contact/index.html" class="nb">Book Now</a>

    <div class="ls-custom" tabindex="0">
      <div class="ls-current"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</div>
      <ul class="ls-options">
        <li onclick="doTranslate('en')"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</li>
        <li onclick="doTranslate('es')"><span class="flg">&#x1F1EA;&#x1F1F8;</span> ES</li>
      </ul>
    </div>
  </nav>"""

mobile_nav_template = """<ul class="ml">
    <li><a href="{rel}index.html">Home</a></li>
    <li><a href="{rel}about-2/index.html">About Us</a></li>
    <li><a href="{rel}departures/index.html">Departures</a></li>
    <li><a href="{rel}news-and-gallery/index.html">Gallery</a></li>
    <li><a href="{rel}blog/index.html">Blog</a></li>
    <li><button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>
      <ul class="md" id="mdd">
        <span class="dh" style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="{rel}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{rel}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{rel}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="{rel}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="{rel}8-day-wildlife-photography-tour/index.html">Wildlife Photography &ndash; 8 Days</a></li>
        
        <span class="dh" style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="{rel}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="{rel}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{rel}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="color:var(--a);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="{rel}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{rel}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </li>
    <li><a href="{rel}contact/index.html">Contact</a></li>
  </ul>"""


def find_matching_tag(content, start_idx, tag_name):
    open_tag = f"<{tag_name}"
    close_tag = f"</{tag_name}>"
    depth = 1
    curr_idx = start_idx
    while depth > 0 and curr_idx < len(content):
        next_open = content.find(open_tag, curr_idx)
        next_close = content.find(close_tag, curr_idx)
        if next_close == -1: return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            curr_idx = next_open + len(open_tag)
        else:
            depth -= 1
            curr_idx = next_close + len(close_tag)
    if depth == 0: return curr_idx
    return -1


for fpath in files:
    if fpath.endswith('admin\\index.html') or 'admin/index.html' in fpath.replace('\\','/'):
        continue # Skip admin page which has a totally different nav menu
        
    try:
        rel_path = os.path.relpath(fpath, base)
        depth = rel_path.count(os.sep)
        
        rel = "../" * depth
        if fpath.endswith('header.php'):
            rel = "../"
        elif fpath.endswith('index.php') and depth == 0:
            rel = ""
        elif fpath.endswith('footer.php'):
            continue
            
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace desktop nav
        start_tag_desktop = '<nav class="nm" aria-label="Main navigation">'
        idx = content.find(start_tag_desktop)
        if idx != -1:
            end_idx = find_matching_tag(content, idx + len(start_tag_desktop), "nav")
            if end_idx != -1:
                content = content[:idx] + desktop_nav_template.format(rel=rel) + content[end_idx:]
                
        # Replace mobile nav
        start_tag_mobile = '<ul class="ml">'
        idx = content.find(start_tag_mobile)
        if idx != -1:
            end_idx = find_matching_tag(content, idx + len(start_tag_mobile), "ul")
            if end_idx != -1:
                content = content[:idx] + mobile_nav_template.format(rel=rel) + content[end_idx:]
                
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
