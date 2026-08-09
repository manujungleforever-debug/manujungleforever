import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

replacements = {
    r"<\?php echo htmlspecialchars\(SITE_NAME\); \?>": "Manu Jungle Forever",
    r"<\?php echo htmlspecialchars\(SITE_ADDRESS\); \?>": "Nuevo Eden, Manu National Park, Peru",
    r"<\?php echo htmlspecialchars\(SITE_PHONE\); \?>": "+51 901 525 679",
    r"<\?php echo htmlspecialchars\(SITE_EMAIL\); \?>": "discover@manujungleforever.com",
    r"<\?php echo htmlspecialchars\(SOCIAL_FACEBOOK\); \?>": "https://www.facebook.com/manujungleforever",
    r"<\?php echo htmlspecialchars\(SOCIAL_INSTAGRAM\); \?>": "https://www.instagram.com/manujungleforever/?hl=en",
    r"<\?php echo htmlspecialchars\(SOCIAL_TRIPADVISOR\); \?>": "https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html",
    r"<\?php echo htmlspecialchars\(SOCIAL_AIRBNB\); \?>": "#",
    r"<\?php echo htmlspecialchars\(SOCIAL_WHATSAPP\); \?>": "https://wa.me/51901525679",
    r"<\?php echo htmlspecialchars\(SOCIAL_TIKTOK\); \?>": "#",
    r"<\?php echo date\('Y'\); \?>": "2026",
    r"<\?php require_once __DIR__.'/config\.php'; \?>\n": "",
    r"<\?php require_once __DIR__.'/\.\./config\.php'; \?>\n": "",
    r"<\?php require_once __DIR__.'/\.\./\.\./config\.php'; \?>\n": ""
}

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            for regex, replacement in replacements.items():
                content = re.sub(regex, replacement, content)
            
            # just in case
            content = content.replace("<?php echo htmlspecialchars(SITE_NAME); ?>", "Manu Jungle Forever")
            
            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Removed PHP from: {path}")

print("Done fixing PHP in HTML.")
