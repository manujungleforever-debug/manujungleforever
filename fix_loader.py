import os
import re

index_path = "g:\\Git\\MANUJUNGLEFOREVER\\www.manujungleforever.com\\index.php"

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace 1200 with 3000
old_script = "}, 1200); // 1.2s delay to show off the animation"
new_script = "}, 3000); // 3s delay as requested"

content = content.replace(old_script, new_script)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated preloader time in index.php")
