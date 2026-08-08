import os
import re

base_dir = "www.manujungleforever.com"
css_path = os.path.join(base_dir, "assets", "css", "new.css")

with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Nuke the old rules
css_content = re.sub(r'/\* Hide Google Translate Banner \*/.*?\.nm { flex-wrap: nowrap; white-space: nowrap; }', '', css_content, flags=re.DOTALL)

# Add the ultimate nuke rules
nuke_css = """
/* Hide Google Translate Banner (Ultimate Nuke) */
body { top: 0px !important; position: relative !important; }
.goog-te-banner-frame { display: none !important; visibility: hidden !important; }
.skiptranslate > iframe.skiptranslate { display: none !important; visibility: hidden !important; }
#goog-gt-tt, .goog-te-balloon-frame { display: none !important; }
.VIpgJd-ZVi9od-aZ2wEe-wOHMyf { display: none !important; }
.goog-text-highlight { background-color: transparent !important; box-shadow: none !important; }

/* Keep layout locked */
.nm { flex-wrap: nowrap; white-space: nowrap; }
"""

css_content += nuke_css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("Nuked Google Translate UI elements via CSS.")
