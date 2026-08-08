import os
import re

base_dir = "www.manujungleforever.com"

# Values from config.php
SITE_NAME = 'Manu Jungle Forever'
SITE_URL = 'https://www.manujungleforever.com'
SITE_EMAIL = 'discover@manujungleforever.com'
SITE_PHONE = '+51 979 808 013 / +51 923 289 231'
WHATSAPP_NUMBER = '51923289231'
SITE_ADDRESS = 'Manu Jungle Forever - La Casa Escondida 17800, Nuevo Eden, Peru'
GTM_ID = 'GTM-5476BC9'
GOOGLE_MAP = 'https://www.google.com/maps/d/embed?mid=1CkYt9KUrq9Jjp9tgxChYmOYvyNaLZnxF'

for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix the video iframe issue by replacing the entire hero section background
        # We replace the .hv div with nothing, and add inline style to .hero
        content = re.sub(
            r'<section class="hero">.*?<div class="hv">.*?</iframe></div>',
            '<section class="hero" style="background: url(\'assets/img/hero.png\') no-repeat center center/cover;">\n  <div class="hv"></div>',
            content,
            flags=re.DOTALL
        )
        # Just in case the previous regex didn't match (if there were minor whitespace diffs)
        content = content.replace(
            '<div class="hv"><iframe src="https://www.youtube-nocookie.com/embed/osF2gQHSCdo?autoplay=1&mute=1&loop=1&playlist=osF2gQHSCdo&controls=0&rel=0&modestbranding=1&start=4&end=56&playsinline=1" title="Amazon Rainforest - Manu Jungle Forever" frameborder="0" allow="autoplay;encrypted-media" loading="lazy"></iframe></div>',
            ''
        )
        content = content.replace(
            '<div class="hv"><iframe src="https://www.youtube-nocookie.com/embed/osF2gQHSCdo?autoplay=1&mute=1&loop=1&playlist=osF2gQHSCdo&controls=0&rel=0&modestbranding=1&start=4&end=56&playsinline=1" title="Amazon Rainforest – Manu Jungle Forever" frameborder="0" allow="autoplay;encrypted-media" loading="lazy"></iframe></div>',
            ''
        )
        content = content.replace('<section class="hero">', '<section class="hero" style="background: url(\'assets/img/hero.png\') no-repeat center center/cover;">')
        
        # If it's index.html, we must replace all PHP tags with literal values
        if file_name == "index.html":
            content = content.replace('<?php echo htmlspecialchars(SITE_NAME); ?>', SITE_NAME)
            content = content.replace('<?php echo htmlspecialchars(SITE_URL); ?>', SITE_URL)
            content = content.replace('<?php echo htmlspecialchars(SITE_EMAIL); ?>', SITE_EMAIL)
            content = content.replace('<?php echo htmlspecialchars(SITE_PHONE); ?>', SITE_PHONE)
            content = content.replace('<?php echo htmlspecialchars(SITE_ADDRESS); ?>', SITE_ADDRESS)
            content = content.replace('<?php echo htmlspecialchars(GTM_ID); ?>', GTM_ID)
            content = content.replace('<?php echo htmlspecialchars(GOOGLE_MAP); ?>', GOOGLE_MAP)
            
            # Remove the require_once if it's there
            content = re.sub(r'<\?php require_once.*?\?>\n?', '', content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

