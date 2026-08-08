import os
import re

base_dir = "www.manujungleforever.com"
css_path = os.path.join(base_dir, "assets", "css", "new.css")

with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Fix the overly greedy iframe hider
css_content = css_content.replace(".skiptranslate iframe,", "iframe.goog-te-banner-frame,")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("Fixed the greedy iframe CSS rule.")
