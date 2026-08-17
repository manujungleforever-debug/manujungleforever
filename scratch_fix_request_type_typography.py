import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# Replace the Reclamo card
old_reclamo = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Reclamo" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">Complaint (Reclamo)</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Dissatisfaction related to the products or services provided.</span>
                    </div>
                </label>'''

new_reclamo = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease; text-transform: none !important; letter-spacing: normal !important;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Reclamo" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2);">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-family:'Outfit', sans-serif; font-size:1.15rem; margin-bottom:6px; text-transform: none !important; letter-spacing: normal !important;">Complaint (Reclamo)</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5; font-family:'Inter', sans-serif; text-transform: none !important; letter-spacing: normal !important; font-weight:400;">Dissatisfaction related to the products or services provided.</span>
                    </div>
                </label>'''

# Replace the Queja card
old_queja = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Queja" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; font-size:1.1rem; margin-bottom:8px;">Query / Grievance (Queja)</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Dissatisfaction not directly related to products or services; or discomfort regarding customer service.</span>
                    </div>
                </label>'''

new_queja = '''<label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease; text-transform: none !important; letter-spacing: normal !important;" onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                    <input type="radio" name="tipo" value="Queja" required style="margin-top:5px; accent-color: #10b981; transform: scale(1.2);">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-family:'Outfit', sans-serif; font-size:1.15rem; margin-bottom:6px; text-transform: none !important; letter-spacing: normal !important;">Query / Grievance (Queja)</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5; font-family:'Inter', sans-serif; text-transform: none !important; letter-spacing: normal !important; font-weight:400;">Dissatisfaction not directly related to products or services; or discomfort regarding customer service.</span>
                    </div>
                </label>'''

html = html.replace(old_reclamo, new_reclamo)
html = html.replace(old_queja, new_queja)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
