import os, glob, re

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

desktop_nav_template = """
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
  """

mobile_nav_template = """
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
  """

for fpath in files:
    try:
        # Calculate relative path
        rel_path = os.path.relpath(fpath, base)
        depth = rel_path.count(os.sep)
        
        rel = "../" * depth
        
        if fpath.endswith('header.php') or fpath.endswith('footer.php'):
            # In partials, use ../ because they are included from subdirs usually
            # Actually, partials might use a PHP variable. Let's skip partials and index.php if they use PHP vars.
            # Wait, header.php uses ../ hardcoded.
            rel = "../"
            if fpath.endswith('footer.php'):
                continue
        
        if fpath.endswith('index.php'):
            rel = ""
            
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace desktop nav
        content = re.sub(r'(<nav class="nm" aria-label="Main navigation">).*?(</nav>)', r'\1' + desktop_nav_template.format(rel=rel) + r'\2', content, flags=re.DOTALL)
        
        # Replace mobile nav
        content = re.sub(r'(<ul class="ml">).*?(</ul>\s*</li>\s*<li><a[^>]*>Contact</a></li>\s*</ul>|</ul>\s*</div>)', r'\1' + mobile_nav_template.format(rel=rel) + r'\2', content, flags=re.DOTALL)
        
        # A simpler regex for mobile nav that just stops at the closing </ul> of the ml:
        # Wait, the mobile nav has nested <ul>. So .*? might stop at the FIRST </ul>.
        # We need a better regex or string manipulation.
        
        # Let's do string manipulation for mobile nav to find the matching closing tag
        start_tag = '<ul class="ml">'
        if start_tag in content:
            start_idx = content.find(start_tag) + len(start_tag)
            
            # Find the closing </ul> by counting
            depth_ul = 1
            curr_idx = start_idx
            while depth_ul > 0 and curr_idx < len(content):
                next_open = content.find('<ul', curr_idx)
                next_close = content.find('</ul>', curr_idx)
                
                if next_close == -1:
                    break
                
                if next_open != -1 and next_open < next_close:
                    depth_ul += 1
                    curr_idx = next_open + 3
                else:
                    depth_ul -= 1
                    curr_idx = next_close + 5
                    if depth_ul == 0:
                        end_idx = next_close
                        content = content[:start_idx] + mobile_nav_template.format(rel=rel) + content[end_idx:]
                        break
                        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
