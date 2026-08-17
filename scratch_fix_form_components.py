import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Update check_menor checkbox markup to use reclamo-checkbox
old_check_menor = '''            <div class="fr">
                <label style="display:flex; align-items:center; gap:12px; cursor:pointer;">
                    <input type="checkbox" id="check_menor">
                    <span>I am under 18 years old</span>
                </label>
            </div>'''

new_check_menor = '''            <div class="fr">
                <label class="reclamo-checkbox">
                    <input type="checkbox" id="check_menor">
                    <span>I am under 18 years old</span>
                </label>
            </div>'''

html = html.replace(old_check_menor, new_check_menor)

# 2. Update Section 3 (Complaint Details) Request Type section to use native reclamo-card classes
old_section_3 = '''    <!-- 3. DETALLE DE LA RECLAMACIÓN Y PEDIDO -->
    <div class="contact-info-card" style="margin-bottom: 24px;">
        <h2 class="h2" style="margin-bottom:24px; font-size:1.4rem; color:#10b981;">3. Complaint Details</h2>
        <div class="fr" style="margin-bottom: 24px;">
            <label>Request Type *</label>
            <div style="display:flex; flex-direction:column; gap:16px;">
                <label style="display:flex; align-items:flex-start; gap:12px; padding:16px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor=\'#10b981\'" onmouseout="this.style.borderColor=\'#1e293b\'">
                    <input type="radio" name="tipo" value="Reclamo" required>
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; margin-bottom:4px;">Complaint (Reclamo)</span>
                        <span style="color:rgba(255,255,255,0.6); font-size:0.875rem;">Dissatisfaction related to the products or services provided.</span>
                    </div>
                </label>
                <label style="display:flex; align-items:flex-start; gap:12px; padding:16px; border:1px solid rgba(255,255,255,0.08); border-radius:12px; background:rgba(255,255,255,0.02); cursor:pointer; transition:border-color 0.3s ease;" onmouseover="this.style.borderColor=\'#10b981\'" onmouseout="this.style.borderColor=\'#1e293b\'">
                    <input type="radio" name="tipo" value="Queja" required>
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:700; margin-bottom:4px;">Query / Grievance (Queja)</span>
                        <span style="color:rgba(255,255,255,0.6); font-size:0.875rem;">Dissatisfaction not directly related to products or services; or discomfort regarding customer service.</span>
                    </div>
                </label>
            </div>
        </div>'''

new_section_3 = '''    <!-- 3. DETALLE DE LA RECLAMACIÓN Y PEDIDO -->
    <div class="contact-info-card" style="margin-bottom: 24px;">
        <h2 class="h2" style="margin-bottom:24px; font-size:1.4rem; color:#10b981;">3. Complaint Details</h2>
        <div class="fr" style="margin-bottom: 24px;">
            <label style="margin-bottom: 12px; display: block;">Request Type *</label>
            <div class="reclamo-cards">
                <label class="reclamo-card">
                    <input type="radio" name="tipo" value="Reclamo" required>
                    <div>
                        <span class="reclamo-card-title">Complaint (Reclamo)</span>
                        <span class="reclamo-card-desc">Dissatisfaction related to the products or services provided.</span>
                    </div>
                </label>
                <label class="reclamo-card">
                    <input type="radio" name="tipo" value="Queja" required>
                    <div>
                        <span class="reclamo-card-title">Query / Grievance (Queja)</span>
                        <span class="reclamo-card-desc">Dissatisfaction not directly related to products or services; or discomfort regarding customer service.</span>
                    </div>
                </label>
            </div>
        </div>'''

html = html.replace(old_section_3, new_section_3)

# 3. Update the Privacy Policy checkbox at the end
old_privacy_check = '''    <!-- DECLARACIÓN JURADA -->
    <div class="contact-info-card" style="margin-bottom: 24px;">
        <label style="display:flex; align-items:center; gap:12px; cursor:pointer;">
            <input type="checkbox" id="declaracion" required>
            <span>
                I declare that the content of my complaint is true, and I accept the <a href="../privacy-policy/index.html" target="_blank">Privacy Policy</a> regarding the processing of my personal data for managing my complaint/query.
            </span>
        </label>
    </div>'''

new_privacy_check = '''    <!-- DECLARACIÓN JURADA -->
    <div class="contact-info-card" style="margin-bottom: 24px;">
        <label class="reclamo-checkbox">
            <input type="checkbox" id="declaracion" required>
            <span>
                I declare that the content of my complaint is true, and I accept the <a href="../privacy-policy/index.html" target="_blank">Privacy Policy</a> regarding the processing of my personal data for managing my complaint/query.
            </span>
        </label>
    </div>'''

html = html.replace(old_privacy_check, new_privacy_check)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
