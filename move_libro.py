import os
import re
import subprocess

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# The user wants it translated to English, using the image asset, and positioned next to/under Explore.
libro_box_regex = r'<div style="margin-top:20px;">\s*<a href="<\?php echo htmlspecialchars\(SITE_URL\); \?>/libro-de-reclamaciones/index\.html" style="text-decoration:none; display:block;">.*?</a>\s*</div>'

# 1. Remove it from its current location (under social icons)
if re.search(libro_box_regex, content, flags=re.DOTALL):
    content = re.sub(libro_box_regex, '', content, flags=re.DOTALL)
else:
    print("Could not find the existing Libro de Reclamaciones block to remove.")

# 2. Re-create it with new specifications
new_libro_html = '''
      <div style="margin-top:30px;">
        <a href="<?php echo htmlspecialchars(SITE_URL); ?>/libro-de-reclamaciones/index.html" style="text-decoration:none; display:block;">
          <div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(201,168,76,0.3); border-radius:12px; padding:16px 12px; text-align:center; transition:0.3s; box-sizing:border-box;">
            <div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
              <div style="color:#002e24; font-weight:800; font-size:0.8rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Complaints<br>Book</div>
              <img src="assets/img/libro_reclamaciones.png" alt="Complaints Book" style="max-width:40px; margin-top:8px;">
            </div>
            <p style="font-size:0.65rem; color:rgba(255,255,255,0.6); line-height:1.4; margin:0;">In accordance with the Consumer Protection and Defense Code, we have a Virtual Complaints Book.</p>
          </div>
        </a>
      </div>
'''

# 3. Inject it inside the "Explore" column, right after the </ul>
explore_col_regex = r'(<div><p class="fh">Explore</p><ul class="fli">.*?</ul>)(</div>)'
content = re.sub(explore_col_regex, r'\1' + new_libro_html + r'\2', content, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.php successfully.")

# Run the standardizer
subprocess.run(["python", "standardize_all_pages.py"])
