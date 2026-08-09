import os
import re

base_dir_manu = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"
base_dir_hidden = r"g:\Git\MANUJUNGLEFOREVER\www.hiddenjunglecusco.com"

manu_path = os.path.join(base_dir_manu, "guided-tours", "index.html")
hidden_path = os.path.join(base_dir_hidden, "guided-tours", "index.html")

with open(manu_path, "r", encoding="utf-8") as f:
    manu_html = f.read()
    
with open(hidden_path, "r", encoding="utf-8") as f:
    hidden_html = f.read()

# Extract the block from <div class="cat-bar" to right before <footer class="ft">
hidden_match = re.search(r'(<!-- Sticky Category Filter Bar -->.*?)(<!-- Footer -->|<footer)', hidden_html, re.DOTALL)
if hidden_match:
    hidden_block = hidden_match.group(1)
    
    hidden_block = re.sub(
        r'<img src="\.\./wp-content/uploads/[^"]+"',
        r'<img src="../assets/media_to_upload/photos/placeholder.jpg"',
        hidden_block
    )
    
    hidden_block = re.sub(
        r'onerror="this\.src=\'\.\./wp-content/uploads/[^\']+\'"',
        r'onerror="this.src=\'../assets/media_to_upload/photos/placeholder.jpg\'"',
        hidden_block
    )

    manu_match = re.search(r'(<!-- Sticky Category Filter Bar -->.*?)(<!-- Footer -->|<footer)', manu_html, re.DOTALL)
    if manu_match:
        new_manu_html = manu_html[:manu_match.start(1)] + hidden_block + manu_html[manu_match.start(2):]
        with open(manu_path, "w", encoding="utf-8") as f:
            f.write(new_manu_html)
        print("Restored HTML structure from hiddenjunglecusco in guided-tours/index.html")
    else:
        print("Could not find the target block in manu_html.")
else:
    print("Could not find the source block in hidden_html.")
