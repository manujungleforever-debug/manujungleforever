import os
import re
import subprocess

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update copyright
content = content.replace('Site design: Meyer Consulting and Management', 'Creado con amor <i class="fas fa-heart" style="color:red;"></i>: por Kemmesik')

# 2. Add Libro de Reclamaciones
libro_html = '''
      <div style="margin-top:20px;">
        <a href="<?php echo htmlspecialchars(SITE_URL); ?>/libro-de-reclamaciones/index.html" style="text-decoration:none; display:block;">
          <div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(201,168,76,0.3); border-radius:12px; padding:16px 12px; text-align:center; transition:0.3s; box-sizing:border-box;">
            <div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
              <div style="color:#002e24; font-weight:800; font-size:0.8rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Libro de<br>Reclamaciones</div>
              <i class="fas fa-book-open" style="color:#c9a84c; font-size:1.5rem; margin-top:8px;"></i>
            </div>
            <p style="font-size:0.65rem; color:rgba(255,255,255,0.6); line-height:1.4; margin:0;">Conforme a lo establecido en el código de Protección y Defensa del Consumidor, contamos con un Libro de Reclamaciones Virtual.</p>
          </div>
        </a>
      </div>
'''

if 'Libro de' not in content:
    content = content.replace('<a href="<?php echo htmlspecialchars(SOCIAL_TIKTOK); ?>" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>\n      </div>',
                              '<a href="<?php echo htmlspecialchars(SOCIAL_TIKTOK); ?>" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>\n      </div>\n' + libro_html)


with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

# 3. Run rebuild_tours.py to propagate the new header/footer
subprocess.run(['python', 'rebuild_tours.py'], check=True)

# 4. Now replace ALL PHP remnants in all .html files, especially WHATSAPP_NUMBER
replacements = {
    r'<\?php echo htmlspecialchars\(SITE_NAME\);\s*\?>': 'Manu Jungle Forever',
    r'<\?php echo htmlspecialchars\(SITE_URL\);\s*\?>': 'https://www.manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_EMAIL\);\s*\?>': 'discover@manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_PHONE\);\s*\?>': '', 
    r'<\?php echo htmlspecialchars\(SITE_ADDRESS\);\s*\?>': '', 
    r'<\?php echo htmlspecialchars\(SOCIAL_FACEBOOK\);\s*\?>': 'https://www.facebook.com/manujungleforever',
    r'<\?php echo htmlspecialchars\(SOCIAL_INSTAGRAM\);\s*\?>': 'https://www.instagram.com/manujungleforever/',
    r'<\?php echo htmlspecialchars\(SOCIAL_TRIPADVISOR\);\s*\?>': 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html',
    r'<\?php echo htmlspecialchars\(SOCIAL_AIRBNB\);\s*\?>': 'https://abnb.me/Ri8XQWoA19',
    r'<\?php echo htmlspecialchars\(SOCIAL_WHATSAPP\);\s*\?>': 'https://wa.me/51923289231',
    r'<\?php echo htmlspecialchars\(WHATSAPP_NUMBER\);\s*\?>': '51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_TIKTOK\);\s*\?>': 'https://www.tiktok.com/@manujungleforever',
    r'<\?php echo htmlspecialchars\(GTM_ID\);\s*\?>': 'GTM-5476BC9',
    r'<\?php echo date\(\'Y\'\);\s*\?>': '2026',
    r'<\?php require_once __DIR__.\'/config\.php\'; \?>': ''
}

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            modified = False
            for pattern, replacement in replacements.items():
                if re.search(pattern, html_content):
                    html_content = re.sub(pattern, replacement, html_content)
                    modified = True
            
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)

print("Done fixing everything!")
