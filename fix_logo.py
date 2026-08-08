import os
import re

base_dir = "www.manujungleforever.com"
css_file = os.path.join(base_dir, "assets", "css", "new.css")

# 1. Clean up new.css (remove glowing effects around the logo)
if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Remove the ::before pseudo element which creates the white glow
    css = re.sub(r'\.nl::before\{.*?\}', '', css, flags=re.DOTALL)
    # Remove the animation for the logoPulse
    css = re.sub(r'@keyframes logoPulse\{.*?\}', '', css, flags=re.DOTALL)
    # Remove hover ::before effect
    css = re.sub(r'\.nl:hover::before\{.*?\}', '', css, flags=re.DOTALL)
    # Remove the drop shadow from the image
    css = re.sub(r'filter:drop-shadow.*?rgba\(255,255,255,0\.5\)\);', '', css)
    css = re.sub(r'filter:drop-shadow.*?rgba\(255,255,255,0\.8\)\)', '', css)
    
    # Just to be safe, I'll completely overwrite the .nl img and .nl styles to be clean
    css = re.sub(r'\.nl img\{.*?\}', '.nl img{height:54px;width:auto;position:relative;z-index:1;transition:all 0.3s ease;}', css)
    css = re.sub(r'\.nl:hover img\{.*?\}', '.nl:hover img{transform:scale(1.03);}', css)
    
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)

# 2. Fix href="index.php" to href="index.html" in all html files and php files
for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html") or file.endswith(".php"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if 'href="index.php"' in content or 'href="../index.php"' in content:
                content = content.replace('href="index.php"', 'href="index.html"')
                content = content.replace('href="../index.php"', 'href="../index.html"')
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

# 3. Update rebuild_tours.py
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('href="index.php"', 'href="index.html"')
    content = content.replace('href="../index.php"', 'href="../index.html"')
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)

