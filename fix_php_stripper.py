import os
import re

script_path = "g:\\Git\\MANUJUNGLEFOREVER\\standardize_all_pages.py"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the php_replacements dictionary
old_dict = r"php_replacements = \{.*?\}"
new_dict = r"""php_replacements = {
    r'<\?php echo htmlspecialchars\(SITE_NAME\);\s*\?>': 'Manu Jungle Forever',
    r'<\?php echo htmlspecialchars\(SITE_URL\);\s*\?>': 'https://www.manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_EMAIL\);\s*\?>': 'discover@manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_PHONE\);\s*\?>': '', 
    r'<\?php echo htmlspecialchars\(SITE_ADDRESS\);\s*\?>': '',
    r'<\?php echo htmlspecialchars\(WHATSAPP_NUMBER\);\s*\?>': '51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_FACEBOOK\);\s*\?>': 'https://www.facebook.com/manujungleforever',
    r'<\?php echo htmlspecialchars\(SOCIAL_INSTAGRAM\);\s*\?>': 'https://www.instagram.com/manujungleforever/?hl=en',
    r'<\?php echo htmlspecialchars\(SOCIAL_TRIPADVISOR\);\s*\?>': 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905',
    r'<\?php echo htmlspecialchars\(SOCIAL_AIRBNB\);\s*\?>': 'https://abnb.me/Ri8XQWoA19',
    r'<\?php echo htmlspecialchars\(SOCIAL_WHATSAPP\);\s*\?>': 'https://wa.me/51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_TIKTOK\);\s*\?>': 'https://www.tiktok.com/@hidden.jungle.cus',
    r'<\?php echo htmlspecialchars\(GTM_ID\);\s*\?>': 'GTM-5476BC9',
    r'<\?php echo htmlspecialchars\(GA_ID\);\s*\?>': 'GT-NS9ZNKJP',
    r'<\?php echo htmlspecialchars\(GOOGLE_MAP\);\s*\?>': 'https://www.google.com/maps/d/embed?mid=1CkYt9KUrq9Jjp9tgxChYmOYvyNaLZnxF',
    r'<\?php echo date\(\'Y\'\);\s*\?>': '2026'
}"""
# In re.sub, repl parses \ escapes. To prevent this, wrap in lambda or use re.escape? No, just use lambda match: new_dict
content = re.sub(old_dict, lambda m: new_dict, content, flags=re.DOTALL)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated php_replacements in standardize_all_pages.py")
