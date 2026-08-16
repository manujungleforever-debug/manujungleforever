import codecs
import re

html_path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(html_path, 'r', 'utf-8') as f:
    html = f.read()

# Replace classes
html = html.replace('class="reclamo-section"', 'style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:24px; padding:40px; margin-bottom: 24px;"')
html = html.replace('class="reclamo-grid"', 'class="f2c"')
html = html.replace('class="reclamo-group"', 'class="fr"')
html = html.replace('class="reclamo-group full-width"', 'class="fr"')
html = html.replace('class="reclamo-radio-group"', 'style="display:flex; gap:20px; margin-top:10px;"')
html = html.replace('class="reclamo-radio"', 'style="display:flex; align-items:center; gap:8px; cursor:pointer; color:#fff;"')
html = html.replace('class="reclamo-cards"', 'style="display:flex; flex-direction:column; gap:16px;"')
html = html.replace('class="reclamo-card"', 'style="display:flex; align-items:flex-start; gap:12px; padding:16px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor=\'var(--a)\'" onmouseout="this.style.borderColor=\'rgba(255,255,255,0.08)\'"')
html = html.replace('class="reclamo-card-content"', 'style="display:flex; flex-direction:column;"')
html = html.replace('class="reclamo-card-title"', 'style="color:#fff; font-weight:700; margin-bottom:4px;"')
html = html.replace('class="reclamo-card-desc"', 'style="color:rgba(255,255,255,0.6); font-size:0.875rem;"')
html = html.replace('class="reclamo-checkbox"', 'style="display:flex; align-items:center; gap:12px; cursor:pointer;"')
html = html.replace('class="reclamo-btn-submit"', 'class="btn ba" style="width:100%;justify-content:center;margin-top:8px;font-size:1rem;padding:16px;"')

# The form container itself
html = html.replace('class="reclamo-form-container"', 'style="display:flex; flex-direction:column; gap:24px;"')

with codecs.open(html_path, 'w', 'utf-8') as f:
    f.write(html)

print('Transformation complete.')
