import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Clean the inline <style> block
html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)

# 2. Restore the original <main> and <section> tags without #060b13
html = html.replace('<main id="main" style="background-color: #060b13 !important; background-image: none !important;">', '<main id="main">')
html = html.replace('<section class="sec" style="background-color: #060b13 !important; background-image: none !important;">', '<section class="sec" style="background:var(--k)">')

# Also the hero
html = html.replace('<section class="in-hero-custom">', '<section class="in-hero" style="background-image: url(\'../assets/img/hero.png\');">')

# 3. Replace the explicit card styles with contact-info-card
html = html.replace('<div style="background-color: #0b1019 !important; border: 1px solid #1e293b !important; border-radius:24px; padding:40px; margin-bottom: 24px;">', '<div class="contact-info-card" style="margin-bottom: 24px;">')

# Ensure section titles don't have hardcoded emerald colors if they shouldn't, but wait, the prompt says:
# "Las tarjetas del formulario ("Business Information", "Consumer Details", etc.) deben usar el contenedor oscuro con bordes sutiles de la web, NO un fondo azul plano superpuesto. Reutiliza exactamente las mismas clases CSS de contenedor/card que utiliza la página /contact/."
# It does NOT say to remove the green from the titles, but I should probably just leave the title color as is, or strip it back to var(--a) just in case. Let's leave the title as #10b981 since that was specifically requested before, or change it back to var(--a). I'll leave the title colors as #10b981 for now since they are fine.

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
