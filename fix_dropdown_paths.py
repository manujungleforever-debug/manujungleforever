import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

raw_desktop_dropdown = """<ul class="dm" style="min-width: 320px;">
        <span class="dh"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        
        <span class="dh" style="margin-top:15px;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="margin-top:15px;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""

raw_mobile_dropdown = """<ul class="md" id="mdd">
        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em;"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        
        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; margin-top:10px;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; margin-top:10px;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""

def get_adapted_dropdown(raw_dropdown, depth):
    if depth == 0:
        return raw_dropdown
    else:
        prefix = "../" * depth
        def replacer(m):
            attr = m.group(1)
            quote = m.group(2)
            val = m.group(3)
            return f"{attr}={quote}{prefix}{val}{quote}"
        return re.sub(r'(href)=([\'"])(.*?)([\'"])', replacer, raw_dropdown)

desktop_pattern = re.compile(r'<ul class="dm".*?>.*?</ul>', re.DOTALL)
mobile_pattern = re.compile(r'<ul class="md" id="mdd">.*?</ul>', re.DOTALL)

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    adapted_desktop = get_adapted_dropdown(raw_desktop_dropdown, depth)
    adapted_mobile = get_adapted_dropdown(raw_mobile_dropdown, depth)
    
    new_content = desktop_pattern.sub(adapted_desktop, content)
    new_content = mobile_pattern.sub(adapted_mobile, new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Fixed Dropdown paths in {count} HTML files.")
