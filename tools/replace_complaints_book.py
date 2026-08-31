import os
import re

directory = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# The pattern we want to replace
pattern = re.compile(
    r'<div class="libro-box" style="max-width:170px; border:1px solid rgba\(201,168,76,0\.25\); border-radius:12px; padding:16px; text-align:center; transition:0\.3s; box-sizing:border-box;">\s*'
    r'<div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px;">\s*'
    r'<div style="color:#002e24; font-weight:900; font-size:0\.85rem; line-height:1\.1; font-family:\'Montserrat\',sans-serif; text-align:center; text-transform:uppercase; margin-bottom:6px;">Complaints<br>Book</div>\s*'
    r'<i class="fas fa-book-open" style="color:#c9a84c; font-size:2\.2rem; margin-top:4px;"></i>\s*'
    r'</div>\s*'
    r'<p style="font-size:0\.65rem; color:rgba\(255,255,255,0\.7\); line-height:1\.4; margin:0;">In accordance with the Consumer Protection Code, we have a Virtual Complaints Book available\.</p>\s*'
    r'</div>',
    re.MULTILINE | re.DOTALL
)

replacement = """<div class="libro-box" style="max-width:200px; border:1px solid rgba(201,168,76,0.25); border-radius:12px; padding:16px; text-align:center; transition:0.3s; box-sizing:border-box;">
            <img src="/assets/img/libro_reclamaciones.png" alt="Complaints Book" style="width:100%; height:auto; border-radius:8px; margin-bottom:12px;">
            <p style="font-size:0.65rem; color:rgba(255,255,255,0.7); line-height:1.4; margin:0;">In accordance with the Consumer Protection Code, we have a Virtual Complaints Book available.</p>
          </div>"""

count = 0

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = pattern.sub(replacement, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {filepath}")

print(f"Total files updated: {count}")
