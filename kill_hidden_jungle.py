import os
import re

directory = "www.manujungleforever.com"
placeholder = "assets/media_to_upload/photos/placeholder.jpg"
img_pattern = re.compile(r'wp-content/uploads/[^"\'>\s\)]+\.(jpg|jpeg|png|gif|webp|svg)', re.IGNORECASE)

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(('.html', '.php', '.css', '.json', '.js')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace image URLs
                new_content = img_pattern.sub(placeholder, content)
                
                # Catch remaining HiddenJungleCusco variants
                new_content = new_content.replace('HiddenJungleCusco', 'ManuJungleForever')
                new_content = new_content.replace('Hidden-Jungle-Cusco', 'Manu-Jungle-Forever')
                new_content = new_content.replace('hidden-jungle-cusco', 'manu-jungle-forever')
                new_content = new_content.replace('Hidden Jungle Cusco', 'Manu Jungle Forever')
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                pass
