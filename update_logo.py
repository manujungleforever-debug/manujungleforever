import os
import re

base_dir = "www.manujungleforever.com"

# 1. Update index.php and index.html
for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Navbar logo: replace anything inside <div class="nl"><a href="index.php">...</a></div>
        if file_name == "index.php":
            alt_text = '<?php echo htmlspecialchars(SITE_NAME); ?>'
        else:
            alt_text = 'Manu Jungle Forever'
            
        content = re.sub(
            r'<div class="nl"><a href="index.php"><img.*?></a></div>',
            f'<div class="nl"><a href="index.php"><img src="assets/img/logo.png" alt="{alt_text}" loading="eager"></a></div>',
            content
        )
        # Footer logo: replace <img src="..." alt="..." class="fl" loading="lazy"> inside <a>
        content = re.sub(
            r'<a href="index\.php"><img.*?class="fl".*?></a>',
            f'<a href="index.php"><img src="assets/img/logo.png" alt="{alt_text}" class="fl" loading="lazy"></a>',
            content
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# 2. Since rebuild_tours.py reads from index.php and I just updated index.php,
# I don't need to manually modify rebuild_tours.py. It will extract the new header/footer.
# I just need to run it.
