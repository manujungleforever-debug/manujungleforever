import glob, json, os, re

# 1. Update data/global.json
global_path = 'www.manujungleforever.com/data/global.json'
if os.path.exists(global_path):
    with open(global_path, 'r', encoding='utf-8') as f:
        gdata = json.load(f)

    gdata['redes_sociales'] = {
        "facebook": "https://www.facebook.com/manujungleforever",
        "instagram": "https://www.instagram.com/manujungleforever/",
        "tripadvisor": "#",
        "airbnb": "#",
        "whatsapp": "https://wa.me/51901525679",
        "tiktok": "#"
    }

    with open(global_path, 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=2, ensure_ascii=False)
    print("Updated global.json with all 6 social channels (cleaned)")

# 2. Update all public HTML files
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if not f.replace('\\', '/').startswith('www.manujungleforever.com/admin')]

full_clean_so_block = """<div class="so">
        <a href="https://www.facebook.com/manujungleforever" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/manujungleforever/" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        <a href="#" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="custom-tripadvisor-icon"></i></a>
        <a href="#" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fa-brands fa-airbnb"></i></a>
        <a href="https://wa.me/51901525679" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
        <a href="#" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>
      </div>"""

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace .so block with full 6 clean social icons
    c = re.sub(r'<div class="so">[\s\S]*?</div>', full_clean_so_block, c)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Restored all 6 social icons cleanly in all {len(html_files)} public HTML files.")
