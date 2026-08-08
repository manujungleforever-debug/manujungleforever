import os
import re

file_path = "www.manujungleforever.com/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

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

for pattern, replacement in replacements.items():
    html_content = re.sub(pattern, replacement, html_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)
