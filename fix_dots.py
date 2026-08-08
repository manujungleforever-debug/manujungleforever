import os

base_dir = "www.manujungleforever.com"

# The old text and the new text
old_text = "Local. Wild. Authentic."
new_text = "Local, wild, and authentic."

for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace(old_text, new_text)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_text, new_text)
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)
