import os
import re

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")
css_path = os.path.join(base_dir, "assets", "css", "new.css")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the leftover <select> block
leftover_regex = r'<select id="custom_lang_selector".*?</select>'
if re.search(leftover_regex, content, flags=re.DOTALL):
    content = re.sub(leftover_regex, '', content, flags=re.DOTALL)
else:
    print("Could not find the leftover select to delete.")

# We also need to fix the emojis, they got corrupted as '????'
# Let's fix the emojis directly using standard unicode strings
content = content.replace('????', '') # strip corrupted
# Actually, it's better to just fix the whole block
clean_block = """<div class="ls-custom" tabindex="0">
      <div class="ls-current"><span class="flg">🇺🇸</span> EN</div>
      <ul class="ls-options">
        <li onclick="doTranslate('en')"><span class="flg">🇺🇸</span> EN</li>
        <li onclick="doTranslate('es')"><span class="flg">🇪🇸</span> ES</li>
      </ul>
    </div>
    <div id="google_translate_element" style="display:none;"></div>"""

# Let's completely replace the broken ls-custom block
block_regex = r'<div class="ls-custom" tabindex="0">.*?<div id="google_translate_element" style="display:none;"></div>'
content = re.sub(block_regex, clean_block, content, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Update CSS to hide the ugly Google Translate top bar
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

if "goog-te-banner-frame" not in css_content:
    hide_banner_css = """
/* Hide Google Translate Banner */
.skiptranslate iframe,
.goog-te-banner-frame.skiptranslate { display: none !important; }
body { top: 0px !important; }
"""
    css_content += hide_banner_css
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

print("Fixed selector and hidden banner.")
