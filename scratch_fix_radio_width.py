import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Replace the Reclamo card radio
old_reclamo_radio = '<input type="radio" name="tipo" value="Reclamo" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2);">'
new_reclamo_radio = '<input type="radio" name="tipo" value="Reclamo" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2); width: auto !important; padding: 0 !important; border: none !important; background: transparent !important; flex-shrink: 0; min-width: 18px;">'

# Replace the Queja card radio
old_queja_radio = '<input type="radio" name="tipo" value="Queja" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2);">'
new_queja_radio = '<input type="radio" name="tipo" value="Queja" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2); width: auto !important; padding: 0 !important; border: none !important; background: transparent !important; flex-shrink: 0; min-width: 18px;">'

html = html.replace(old_reclamo_radio, new_reclamo_radio)
html = html.replace(old_queja_radio, new_queja_radio)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
