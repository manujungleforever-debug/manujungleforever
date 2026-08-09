import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# Desktop menu regex to find the UL content of "Guided Tours"
dm_re = re.compile(r'(<div class="hd"><a href="[^"]*?guided-tours/index\.html">Guided Tours <i class="fas fa-caret-down"></i></a>\s*<ul class="dm">)(.*?)(</ul>\s*</div>)', re.DOTALL)
# Mobile menu regex
mdd_re = re.compile(r'(<li><button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>\s*<ul class="md" id="mdd">)(.*?)(</ul>\s*</li>)', re.DOTALL)


for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.php'):
            path = os.path.join(root, file)
            
            # calculate depth for paths
            rel_dir = os.path.relpath(root, base_dir)
            depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
            prefix = "../" * depth if depth > 0 else ""
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig_content = content
            
            new_dm_content = f"""
        <span class="dh"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="{prefix}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{prefix}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{prefix}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{prefix}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{prefix}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="{prefix}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="{prefix}8-day-wildlife-photography-tour/index.html">Wildlife Photography &ndash; 8 Days</a></li>
        
        <span class="dh"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="{prefix}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="{prefix}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{prefix}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="{prefix}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{prefix}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      """
      
            new_mdd_content = f"""
        <span class="dh" style="color:var(--g1);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="{prefix}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{prefix}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="{prefix}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{prefix}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="{prefix}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="{prefix}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="{prefix}8-day-wildlife-photography-tour/index.html">Wildlife Photography &ndash; 8 Days</a></li>
        
        <span class="dh" style="color:var(--g1);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="{prefix}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="{prefix}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{prefix}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh" style="color:var(--g1);font-size:0.8rem;text-transform:uppercase;padding:10px 20px;display:block;"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="{prefix}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{prefix}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      """

            # Replace desktop
            content = dm_re.sub(r'\1' + new_dm_content.replace('\\', '\\\\') + r'\3', content)
            
            # Replace mobile
            content = mdd_re.sub(r'\1' + new_mdd_content.replace('\\', '\\\\') + r'\3', content)
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {path}")

print("Done updating dropdown structures.")
