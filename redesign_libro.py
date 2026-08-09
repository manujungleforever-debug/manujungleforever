import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# The regex captures the img src in group 1.
# It matches from <div class="libro-box" to </div> just before </a>
pattern = re.compile(r'(<div class="libro-box"[^>]*>.*?<img src="([^"]+)"[^>]*>.*?</div>)\s*(</a>)', re.DOTALL | re.IGNORECASE)

new_libro_template = """<div class="libro-box" style="background: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 24px 16px; text-align: center; transition: all 0.3s ease; box-shadow: 0 8px 32px rgba(0,0,0,0.2); backdrop-filter: blur(10px); box-sizing:border-box;">
  <div style="background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%); border-radius: 12px; padding: 16px; display: inline-flex; flex-direction: column; align-items: center; margin-bottom: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.15), inset 0 2px 0 rgba(255,255,255,0.5); transform: translateY(0); transition: transform 0.3s ease;">
    <div style="color: #002e24; font-weight: 800; font-size: 1rem; line-height: 1.1; font-family: 'Syne', sans-serif; text-align: center; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Complaints<br>Book</div>
    <img src="{img_src}" alt="Complaints Book" style="max-width: 80px; width: 100%; height: auto; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
  </div>
  <p style="font-size: 0.75rem; color: rgba(255,255,255,0.7); line-height: 1.5; font-family: 'Outfit', sans-serif; margin: 0; padding: 0 10px;">In accordance with the Consumer Protection and Defense Code, we have a Virtual Complaints Book.</p>
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
                return new_libro_template.format(img_src=img_src).replace('\\3', match.group(3))
                
            content = pattern.sub(replacer, content)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                files_updated += 1
                print(f"Updated libro-box in: {filepath}")

print(f"Done updating libro-box in {files_updated} files.")
