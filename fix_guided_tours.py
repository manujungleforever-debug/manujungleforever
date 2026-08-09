import os
import re

base_dir_manu = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
base_dir_hidden = r"g:\Git\MANUJUNGLEFOREVER\www.hiddenjunglecusco.com"

# 1. Append missing CSS to new.css
with open('temp_style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace fonts in CSS to match manujungleforever
css_content = css_content.replace("'Montserrat', sans-serif", "'Syne', sans-serif")
css_content = css_content.replace("'Inter', sans-serif", "'Outfit', sans-serif")

css_path = os.path.join(base_dir_manu, "assets", "css", "new.css")
with open(css_path, "a", encoding="utf-8") as f:
    f.write("\n/* MISSING GUIDED TOURS CSS */\n")
    f.write(css_content)

print("CSS appended to new.css.")

# 2. Restore the original HTML block for guided-tours
manu_path = os.path.join(base_dir_manu, "guided-tours", "index.html")
hidden_path = os.path.join(base_dir_hidden, "guided-tours", "index.html")

with open(manu_path, "r", encoding="utf-8") as f:
    manu_html = f.read()
    
with open(hidden_path, "r", encoding="utf-8") as f:
    hidden_html = f.read()

# Extract the block from <div class="cat-bar" to <!-- Footer -->
hidden_match = re.search(r'(<!-- Sticky Category Filter Bar -->.*?)(<!-- Footer -->)', hidden_html, re.DOTALL)
if hidden_match:
    hidden_block = hidden_match.group(1)
    
    # We need to replace the image paths in hidden_block with placeholders because Manu uses placeholders for now
    hidden_block = re.sub(
        r'<img src="\.\./wp-content/uploads/[^"]+"',
        r'<img src="../assets/media_to_upload/photos/placeholder.jpg"',
        hidden_block
    )
    
    # We also need to fix the onerror attribute which has wp-content path
    hidden_block = re.sub(
        r'onerror="this\.src=\'\.\./wp-content/uploads/[^\']+\'"',
        r'onerror="this.src=\'../assets/media_to_upload/photos/placeholder.jpg\'"',
        hidden_block
    )

    # Now replace the same block in manu_html
    manu_match = re.search(r'(<!-- Sticky Category Filter Bar -->.*?)(<!-- Footer -->)', manu_html, re.DOTALL)
    if manu_match:
        new_manu_html = manu_html[:manu_match.start(1)] + hidden_block + manu_html[manu_match.start(2):]
        with open(manu_path, "w", encoding="utf-8") as f:
            f.write(new_manu_html)
        print("Restored HTML structure from hiddenjunglecusco in guided-tours/index.html")
    else:
        print("Could not find the target block in manu_html.")
else:
    print("Could not find the source block in hidden_html.")
