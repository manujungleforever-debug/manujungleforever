import glob, json, os, re

# 1. Update data/global.json
global_path = 'www.manujungleforever.com/data/global.json'
if os.path.exists(global_path):
    with open(global_path, 'r', encoding='utf-8') as f:
        gdata = json.load(f)

    if 'redes_sociales' in gdata:
        gdata['redes_sociales']['whatsapp'] = 'https://wa.me/51901525679'
        gdata['redes_sociales'].pop('tripadvisor', None)
        gdata['redes_sociales'].pop('airbnb', None)
        gdata['redes_sociales'].pop('tiktok', None)
    
    if 'contacto_principal' in gdata:
        gdata['contacto_principal']['whatsapp'] = '51901525679'
        gdata['contacto_principal']['telefono'] = '+51 901 525 679'

    with open(global_path, 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=2, ensure_ascii=False)
    print("Updated data/global.json")

# 2. Update config.php
config_path = 'www.manujungleforever.com/config.php'
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        cc = f.read()
    cc = cc.replace("define('WHATSAPP_NUMBER', '51923289231');", "define('WHATSAPP_NUMBER', '51901525679');")
    cc = cc.replace("define('SOCIAL_WHATSAPP',    'https://wa.me/51923289231');", "define('SOCIAL_WHATSAPP',    'https://wa.me/51901525679');")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(cc)
    print("Updated config.php")

# 3. Update all public HTML files
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if not f.replace('\\', '/').startswith('www.manujungleforever.com/admin')]

clean_so_block = """<div class="so">
        <a href="https://www.facebook.com/manujungleforever" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/manujungleforever/" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        <a href="https://wa.me/51901525679" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
      </div>"""

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Replace .so block
    c = re.sub(r'<div class="so">[\s\S]*?</div>', clean_so_block, c)

    # Replace old whatsapp numbers and hiddenjungle links
    c = c.replace('51923289231', '51901525679')
    c = c.replace('"https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html"', '')
    c = c.replace(',"https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html"', '')
    c = c.replace('"https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html",', '')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Updated social links across all {len(html_files)} public HTML files.")
