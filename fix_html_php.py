import os
import re

base_dir = "www.manujungleforever.com"

# Values to replace the PHP tags with in HTML files
replacements = {
    r'<\?php echo htmlspecialchars\(SITE_NAME\);\s*\?>': 'Manu Jungle Forever',
    r'<\?php echo htmlspecialchars\(SITE_URL\);\s*\?>': 'https://www.manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_EMAIL\);\s*\?>': 'discover@manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_PHONE\);\s*\?>': '', # EMPTY as requested
    r'<\?php echo htmlspecialchars\(SITE_ADDRESS\);\s*\?>': '', # EMPTY as requested
    r'<\?php echo htmlspecialchars\(SOCIAL_FACEBOOK\);\s*\?>': 'https://www.facebook.com/manujungleforever',
    r'<\?php echo htmlspecialchars\(SOCIAL_INSTAGRAM\);\s*\?>': 'https://www.instagram.com/manujungleforever/',
    r'<\?php echo htmlspecialchars\(SOCIAL_TRIPADVISOR\);\s*\?>': 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html',
    r'<\?php echo htmlspecialchars\(SOCIAL_AIRBNB\);\s*\?>': 'https://abnb.me/Ri8XQWoA19',
    r'<\?php echo htmlspecialchars\(SOCIAL_WHATSAPP\);\s*\?>': 'https://wa.me/51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_TIKTOK\);\s*\?>': 'https://www.tiktok.com/@manujungleforever',
    r'<\?php echo htmlspecialchars\(GTM_ID\);\s*\?>': 'GTM-5476BC9',
    r'<\?php require_once __DIR__.\'/config\.php\'; \?>': ''
}

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # First, we also need to fix the TripAdvisor icon class. Let's use fab fa-tripadvisor.
            content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', '<i class="fab fa-tripadvisor"></i>')

            for pattern, replacement in replacements.items():
                content = re.sub(pattern, replacement, content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

# We must also do this for index.php but ONLY fix the TripAdvisor icon class there (PHP should stay PHP)
index_php_path = os.path.join(base_dir, "index.php")
if os.path.exists(index_php_path):
    with open(index_php_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', '<i class="fab fa-tripadvisor"></i>')
    with open(index_php_path, "w", encoding="utf-8") as f:
        f.write(content)

# Also update rebuild_tours.py so future rebuilds use fab fa-tripadvisor and static replacements if it does them
