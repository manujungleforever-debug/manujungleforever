import os
import re

base_dir = "www.manujungleforever.com"

# 1. Update index.php and index.html
for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Logo
        content = content.replace(
            '<img src="assets/media_to_upload/photos/placeholder.jpg" alt="<?php echo htmlspecialchars(SITE_NAME); ?>" width="190" height="54" loading="eager">',
            '<img src="assets/img/hike.png" alt="<?php echo htmlspecialchars(SITE_NAME); ?>" width="190" height="54" loading="eager" style="object-fit:cover; border-radius:4px;">'
        )
        content = content.replace(
            '<img src="assets/media_to_upload/photos/placeholder.jpg" alt="Manu Jungle Forever" width="190" height="54" loading="eager">',
            '<img src="assets/img/hike.png" alt="Manu Jungle Forever" width="190" height="54" loading="eager" style="object-fit:cover; border-radius:4px;">'
        )
        
        # Wildlife Quest
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Wildlife quest at Machu Wasi',
            'src="assets/img/hike.png" alt="Wildlife quest at Machu Wasi'
        )
        # Tour 1
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Manu National Park wildlife tour from Cusco"',
            'src="assets/img/tour_boat.png" alt="Manu National Park wildlife tour from Cusco"'
        )
        # Tour 2
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Rainforest Road Trip',
            'src="assets/img/hero.png" alt="Rainforest Road Trip'
        )
        # Tour 3
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Manu Amazon Expedition from Cusco"',
            'src="assets/img/hike.png" alt="Manu Amazon Expedition from Cusco"'
        )
        # Legacy
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Manu Jungle Forever Family',
            'src="assets/img/hike.png" alt="Manu Jungle Forever Family'
        )
        # Jaguar
        content = content.replace(
            'src="assets/media_to_upload/photos/placeholder.jpg" alt="Manu National Park wildlife - Jaguar"',
            'src="assets/img/jaguar.png" alt="Manu National Park wildlife - Jaguar"'
        )
        
        # Catch any remaining ones
        content = content.replace('assets/media_to_upload/photos/placeholder.jpg', 'assets/img/hero.png')

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# 2. Update about-2/index.html
about_path = os.path.join(base_dir, "about-2", "index.html")
if os.path.exists(about_path):
    with open(about_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('../assets/media_to_upload/photos/placeholder.jpg', '../assets/img/hero.png')
    with open(about_path, "w", encoding="utf-8") as f:
        f.write(content)

# 3. Update rebuild_tours.py and run it
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(
        "background-image:url('../assets/media_to_upload/photos/placeholder.jpg')",
        "background-image:url('../assets/img/hero.png')"
    )
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)

