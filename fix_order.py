import os
import re

index_path = "g:\\Git\\MANUJUNGLEFOREVER\\www.manujungleforever.com\\index.php"

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Swap ls-custom and nb (Book Now)
ls_html = """    <div class="ls-custom" tabindex="0">
      <div class="ls-current"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</div>
      <ul class="ls-options">
        <li onclick="doTranslate('en')"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</li>
        <li onclick="doTranslate('es')"><span class="flg">&#x1F1EA;&#x1F1F8;</span> ES</li>
      </ul>
    </div>"""

nb_html = """    <a href="contact/index.html" class="nb">Book Now</a>"""

old_block = ls_html + "\n" + nb_html
new_block = nb_html + "\n" + ls_html

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Swapped Book Now and Language Selector")
else:
    print("Block not found. Might already be swapped.")
