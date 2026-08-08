import os
import re

base_dir = "www.manujungleforever.com"
map_url = "https://www.google.com/maps/d/embed?mid=1CkYt9KUrq9Jjp9tgxChYmOYvyNaLZnxF"
pattern = r'<\?php echo htmlspecialchars\(GOOGLE_MAP\);\s*\?>'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if re.search(pattern, content):
                content = re.sub(pattern, map_url, content)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

# Update standardize_all_pages.py to include GOOGLE_MAP
std_script = "standardize_all_pages.py"
if os.path.exists(std_script):
    with open(std_script, "r", encoding="utf-8") as f:
        std_content = f.read()
    
    if "GOOGLE_MAP" not in std_content:
        replacement_entry = f"    r'<\?php echo htmlspecialchars\(GOOGLE_MAP\);\s*\?>': '{map_url}',\n"
        std_content = std_content.replace(
            "r'<\?php require_once __DIR__.\'/config\.php\'; \?>': ''",
            replacement_entry + "    r'<\?php require_once __DIR__.\'/config\.php\'; \?>': ''"
        )
        with open(std_script, "w", encoding="utf-8") as f:
            f.write(std_content)

print("Map URL restored successfully.")
