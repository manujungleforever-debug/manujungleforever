import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# The regex captures the img src in group 2.
# It matches from <div class="libro-box" to </div> just before </a>
pattern = re.compile(r'(<div class="libro-box"[^>]*>.*?<img src="([^"]+)"[^>]*>.*?</div>)\s*(</a>)', re.DOTALL | re.IGNORECASE)

# This is the exact old HTML, with max-width increased to 90px.
old_libro_template = """<div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(201,168,76,0.3); border-radius:12px; padding:16px 12px; text-align:center; transition:0.3s; box-sizing:border-box;">
  <div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
    <div style="color:#002e24; font-weight:800; font-size:0.8rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Complaints<br>Book</div>
    <img src="{img_src}" alt="Complaints Book" style="max-width:120px; width:100%; margin-top:8px;">
  </div>
  <p style="font-size:0.65rem; color:rgba(255,255,255,0.6); line-height:1.4; margin:0;">In accordance with the Consumer Protection and Defense Code, we have a Virtual Complaints Book.</p>
</div>
\\3"""

files_updated = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            def replacer(match):
                img_src = match.group(2)
                return old_libro_template.format(img_src=img_src).replace('\\3', match.group(3))
                
            content = pattern.sub(replacer, content)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                files_updated += 1
                print(f"Reverted libro-box in: {filepath}")

print(f"Done reverting libro-box in {files_updated} files.")
