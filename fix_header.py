import os
import re

base_dir = "www.manujungleforever.com"

# 1. Update index.php and index.html
for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix TripAdvisor icon
        content = content.replace('<i class="fab fa-tripadvisor"></i>', '<i class="fa-brands fa-tripadvisor"></i>')
        content = content.replace('<i class="fab fa-facebook-f"></i>', '<i class="fa-brands fa-facebook-f"></i>')
        content = content.replace('<i class="fab fa-instagram"></i>', '<i class="fa-brands fa-instagram"></i>')
        content = content.replace('<i class="fab fa-airbnb"></i>', '<i class="fa-brands fa-airbnb"></i>')
        content = content.replace('<i class="fab fa-whatsapp"></i>', '<i class="fa-brands fa-whatsapp"></i>')
        content = content.replace('<i class="fab fa-tiktok"></i>', '<i class="fa-brands fa-tiktok"></i>')

        # Fix Guided Tours dropdown categories
        old_dropdown = """<ul class="dm">
        <li><a href="wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        <li><a href="rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""
      
        new_dropdown = """<ul class="dm">
        <span class="dh"><i class="fas fa-leaf"></i> Wildlife Tours</span>
        <li><a href="3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife - Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife - Nuevo Eden</a></li>
        <li><a href="6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife - Blanquillo</a></li>
        <li><a href="6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone - 6 Days</a></li>
        <li><a href="8-day-wildlife-photography-tour/index.html">Wildlife Photography - 8 Days</a></li>
        
        <span class="dh"><i class="fas fa-compass"></i> Expeditions</span>
        <li><a href="rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>"""
      
        # Fallback regex if whitespace differs
        if old_dropdown in content:
            content = content.replace(old_dropdown, new_dropdown)
        else:
            content = re.sub(r'<ul class="dm">\s*<li><a href="wildlife-tours-from-cusco.*?</ul>', new_dropdown, content, flags=re.DOTALL)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# Update rebuild_tours.py
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('<i class="fab fa-tripadvisor"></i>', '<i class="fa-brands fa-tripadvisor"></i>')
    content = content.replace('<i class="fab fa-facebook-f"></i>', '<i class="fa-brands fa-facebook-f"></i>')
    content = content.replace('<i class="fab fa-instagram"></i>', '<i class="fa-brands fa-instagram"></i>')
    content = content.replace('<i class="fab fa-airbnb"></i>', '<i class="fa-brands fa-airbnb"></i>')
    content = content.replace('<i class="fab fa-whatsapp"></i>', '<i class="fa-brands fa-whatsapp"></i>')
    content = content.replace('<i class="fab fa-tiktok"></i>', '<i class="fa-brands fa-tiktok"></i>')
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)
