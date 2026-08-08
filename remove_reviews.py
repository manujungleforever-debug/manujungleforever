import re
import os

files = [
    "www.manujungleforever.com/index.php",
    "www.manujungleforever.com/index.html"
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove trustindex widget and replace with a generic placeholder
        new_content = re.sub(
            r'<div class="trustindex-widget" data-url="https://cdn\.trustindex\.io/loader\.js\?[^"]+"></div>\s*<script async defer src="https://cdn\.trustindex\.io/loader\.js\?[^"]+"></script>',
            '''<div style="padding: 40px; background: rgba(255,255,255,0.05); border-radius: 12px; border: 1px dashed rgba(255,255,255,0.2);">
                <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem; margin:0;"><i class="fab fa-google" style="margin-right: 10px; color: #fff;"></i> Reviews Widget Placeholder. Insert your new Manu Jungle Forever Trustindex or Google Reviews script here once your Google Business profile is ready.</p>
            </div>''',
            content
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
