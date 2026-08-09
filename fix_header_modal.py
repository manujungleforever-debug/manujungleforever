import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

new_desktop_dropdown = """<ul class="dm" style="min-width: 320px;">
        <span class="dh"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        
        <span class="dh" style="margin-top:15px;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="../rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="../2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="../5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="margin-top:15px;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""

new_mobile_dropdown = """<ul class="md" id="mdd">
        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em;"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        
        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; margin-top:10px;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="../rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="../2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="../5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="display:block; padding:10px 15px; color:#10B981; font-size:0.8rem; font-weight:700; letter-spacing:0.1em; margin-top:10px;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""

desktop_pattern = re.compile(r'<ul class="dm">.*?</ul>', re.DOTALL)
mobile_pattern = re.compile(r'<ul class="md" id="mdd">.*?</ul>', re.DOTALL)
modal_pattern = re.compile(r'<div class="modal" id="bk-modal" role="dialog" aria-modal="true" aria-label="Book a Tour">.*?</div>\s*</div>\s*</div>', re.DOTALL)
modal_pattern_fallback = re.compile(r'<div class="modal" id="bk-modal" role="dialog" aria-modal="true" aria-label="Book a Tour">.*?</div>\s*</div>', re.DOTALL) # in case it has fewer divs
script_pattern = re.compile(r'function openModal\(\)\{.*?\}', re.DOTALL)
script_pattern2 = re.compile(r'function closeModal\(\)\{.*?\}', re.DOTALL)
script_pattern3 = re.compile(r"document\.getElementById\('bk-modal'\)\.addEventListener\('click',function\(e\)\{if\(e\.target===this\)closeModal\(\);\w*\}\);", re.DOTALL)
script_pattern4 = re.compile(r"document\.addEventListener\('keydown',e=>\{if\(e\.key==='Escape'\)closeModal\(\);\w*\}\);", re.DOTALL)
form_ajax_pattern = re.compile(r"// Booking form AJAX.*?\}\);", re.DOTALL)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    
    # 1. Update Dropdowns
    if desktop_pattern.search(new_content):
        new_content = desktop_pattern.sub(new_desktop_dropdown, new_content)
    if mobile_pattern.search(new_content):
        new_content = mobile_pattern.sub(new_mobile_dropdown, new_content)
        
    # 2. Remove bk-modal HTML globally
    if '<div class="modal" id="bk-modal"' in new_content:
        # We need a robust way to strip the modal. It contains <form> and <div class="mb">
        # A simpler way is to just use a greedy regex from `<div class="modal" id="bk-modal"` up to the start of `<footer class="ft">`
        # Because the modal is always right above the footer!
        footer_split = new_content.split('<footer class="ft">')
        if len(footer_split) == 2:
            before_footer = footer_split[0]
            # remove modal from before_footer
            modal_start = before_footer.find('<div class="modal" id="bk-modal"')
            if modal_start != -1:
                before_footer = before_footer[:modal_start]
                new_content = before_footer + '<footer class="ft">' + footer_split[1]

    # 3. Remove modal JS globally
    new_content = script_pattern.sub('', new_content)
    new_content = script_pattern2.sub('', new_content)
    new_content = script_pattern3.sub('', new_content)
    new_content = script_pattern4.sub('', new_content)
    new_content = form_ajax_pattern.sub('', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

print("Global fixes for Dropdown and Modal complete.")
