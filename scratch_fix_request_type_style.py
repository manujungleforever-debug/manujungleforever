import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Reclamo box replacement
old_reclamo = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid #1a8bb3; border-radius:8px; background:rgba(26,139,179,0.05); cursor:pointer; transition:all 0.3s ease;" onmouseover="this.style.background='rgba(26,139,179,0.1)'" onmouseout="this.style.background='rgba(26,139,179,0.05)'">
                    <input type="radio" name="tipo" value="Reclamo" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Complaint (Reclamo)</span>'''

new_reclamo = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Reclamo" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">Complaint (Reclamo)</span>'''

# Queja box replacement
old_queja = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid #1a8bb3; border-radius:8px; background:rgba(26,139,179,0.05); cursor:pointer; transition:all 0.3s ease;" onmouseover="this.style.background='rgba(26,139,179,0.1)'" onmouseout="this.style.background='rgba(26,139,179,0.05)'">
                    <input type="radio" name="tipo" value="Queja" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Query / Grievance (Queja)</span>'''

new_queja = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Queja" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">Query / Grievance (Queja)</span>'''


html = html.replace(old_reclamo, new_reclamo)
html = html.replace(old_queja, new_queja)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
