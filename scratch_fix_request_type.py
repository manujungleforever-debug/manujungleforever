import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# The block to replace
old_block_pattern = r'3\. Complaint Details</h2>.*?<label>Request Type \*</label>.*?<textarea name="detalle" rows="4" required placeholder="Describe the events clearly..."></textarea>\s*</div>'

new_block = '''3. Detalle de la Reclamación y Pedido</h2>
        <div class="fr" style="margin-bottom: 24px;">
            <label>Tipo de Reclamación *</label>
            <div style="display:flex; flex-direction:column; gap:16px;">
                <label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid #1a8bb3; border-radius:8px; background:rgba(26,139,179,0.05); cursor:pointer; transition:all 0.3s ease;" onmouseover="this.style.background='rgba(26,139,179,0.1)'" onmouseout="this.style.background='rgba(26,139,179,0.05)'">
                    <input type="radio" name="tipo" value="Reclamo" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Reclamo</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Disconformidad relacionada a los productos o servicios.</span>
                    </div>
                </label>
                <label style="display:flex; align-items:flex-start; gap:16px; padding:20px; border:1px solid #1a8bb3; border-radius:8px; background:rgba(26,139,179,0.05); cursor:pointer; transition:all 0.3s ease;" onmouseover="this.style.background='rgba(26,139,179,0.1)'" onmouseout="this.style.background='rgba(26,139,179,0.05)'">
                    <input type="radio" name="tipo" value="Queja" required style="margin-top:4px;">
                    <div style="display:flex; flex-direction:column;">
                        <span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Queja</span>
                        <span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Disconformidad no relacionada a los productos o servicios; o, malestar o descontento respecto a la atención al público.</span>
                    </div>
                </label>
            </div>
        </div>
        
        <div class="fr" style="margin-bottom: 24px;">
            <label>Detalle de lo ocurrido *</label>
            <textarea name="detalle" rows="4" required placeholder="Explique de manera clara su inconformidad..."></textarea>
        </div>'''

new_html, count = re.subn(old_block_pattern, new_block, html, flags=re.DOTALL)

if count > 0:
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(new_html)
    print(f"Replaced successfully {count} time(s).")
else:
    print("Regex could not find the block to replace.")
