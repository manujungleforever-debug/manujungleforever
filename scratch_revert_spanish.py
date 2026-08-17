import codecs

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

replacements = [
    ('3. Detalle de la Reclamación y Pedido</h2>', '3. Complaint Details</h2>'),
    ('<label>Tipo de Reclamación *</label>', '<label>Request Type *</label>'),
    ('<span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Reclamo</span>', '<span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Complaint (Reclamo)</span>'),
    ('<span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Disconformidad relacionada a los productos o servicios.</span>', '<span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Dissatisfaction related to the products or services provided.</span>'),
    ('<span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Queja</span>', '<span style="color:#fff; font-weight:800; font-size:1.1rem; margin-bottom:8px;">Query / Grievance (Queja)</span>'),
    ('<span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Disconformidad no relacionada a los productos o servicios; o, malestar o descontento respecto a la atención al público.</span>', '<span style="color:rgba(255,255,255,0.65); font-size:0.875rem; line-height:1.5;">Dissatisfaction not directly related to products or services; or discomfort regarding customer service.</span>'),
    ('<label>Detalle de lo ocurrido *</label>', '<label>Details of the Incident *</label>'),
    ('Explique de manera clara su inconformidad...', 'Describe the events clearly...')
]

for old_str, new_str in replacements:
    html = html.replace(old_str, new_str)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
