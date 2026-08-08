import os
import re

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the extra </div>
extra_div_regex = r'</ul>\s*</div>\s*</div>\s*<a href="contact/index.html" class="nb">'
replacement_div = '</ul>\n    </div>\n    <a href="contact/index.html" class="nb">'
content = re.sub(extra_div_regex, replacement_div, content)

# 2. Fix emojis using HTML entities just in case they are actually corrupted
us_flag = '&#x1F1FA;&#x1F1F8;'
es_flag = '&#x1F1EA;&#x1F1F8;'

content = content.replace('<span class="flg">????</span> EN', f'<span class="flg">{us_flag}</span> EN')
content = content.replace('<span class="flg">????</span> ES', f'<span class="flg">{es_flag}</span> ES')
content = content.replace('<span class="flg">🇺🇸</span>', f'<span class="flg">{us_flag}</span>')
content = content.replace('<span class="flg">🇪🇸</span>', f'<span class="flg">{es_flag}</span>')

# Let's also make sure we fix the JS that sets the flag
js_regex = r'<span class=\\"flg\\">.*?</span> ES'
js_replacement = f'<span class=\\"flg\\">{es_flag}</span> ES'
content = re.sub(js_regex, js_replacement, content)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed extra div and encoded flags.")
