import os
import codecs
import glob
import re

admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

css_to_inject = '''
        .card-icon-tours { background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; box-shadow: 0 6px 20px rgba(245,158,11,0.35); }
        .card-icon-blog { background: linear-gradient(135deg, #14b8a6, #0d9488); color: #fff; box-shadow: 0 6px 20px rgba(20,184,166,0.35); }
        .card-icon-testim { background: linear-gradient(135deg, #8b5cf6, #6d28d9); color: #fff; box-shadow: 0 6px 20px rgba(139,92,246,0.35); }
        .card-icon-reclamos { background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff; box-shadow: 0 6px 20px rgba(239,68,68,0.35); }
        .card-icon-contenido { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; box-shadow: 0 6px 20px rgba(59,130,246,0.35); }
        .card-icon-salidas { background: linear-gradient(135deg, #ec4899, #be185d); color: #fff; box-shadow: 0 6px 20px rgba(236,72,153,0.35); }
        .card-icon-medios { background: linear-gradient(135deg, #10b981, #059669); color: #fff; box-shadow: 0 6px 20px rgba(16,185,129,0.35); }
        .btn-card-icon {
            width: 52px;
            height: 52px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
            margin-right: 16px;
        }
'''

# Use regex to match the inner HTML of the container div that has the pt and ps tags
replacements = [
    # Tours (has ps)
    (r'<div><p class="pt">🌿 Tours</p><p class="ps">\$\{ts\.length\} tours registrados</p></div>',
     r'<div style="display:flex;align-items:center;"><div class="btn-card-icon card-icon-tours"><i class="ph ph-map-trifold"></i></div><div><p class="pt" style="margin-bottom:0">Tours</p><p class="ps">${ts.length} tours registrados</p></div></div>'),
    
    # Testimonios (has ps)
    (r'<div><p class="pt">⭐ Testimonios de Clientes</p><p class="ps">\$\{ts\.length\} testimonios</p></div>',
     r'<div style="display:flex;align-items:center;"><div class="btn-card-icon card-icon-testim"><i class="ph ph-chat-circle-text"></i></div><div><p class="pt" style="margin-bottom:0">Testimonios de Clientes</p><p class="ps">${ts.length} testimonios</p></div></div>'),
    
    # Salidas (has ps)
    (r'<div><p class="pt">📅 Gestión de Salidas Programadas</p><p class="ps">Control de cupos, logística y ventas</p></div>',
     r'<div style="display:flex;align-items:center;"><div class="btn-card-icon card-icon-salidas"><i class="ph ph-calendar"></i></div><div><p class="pt" style="margin-bottom:0">Salidas Programadas</p><p class="ps">Control de cupos, logística y ventas</p></div></div>'),
    
    # Medios (has ps)
    (r'<div><p class="pt">🖼️ Biblioteca de Medios</p><p class="ps">Gestiona todas las imágenes y videos \(Cloudflare R2\)</p></div>',
     r'<div style="display:flex;align-items:center;"><div class="btn-card-icon card-icon-medios"><i class="ph ph-image"></i></div><div><p class="pt" style="margin-bottom:0">Biblioteca de Medios</p><p class="ps">Gestiona todas las imágenes y videos (Cloudflare R2)</p></div></div>'),

    # Blog (no surrounding div, just a p)
    (r'<p class="pt">✍️ Artículos del Blog</p>',
     r'<div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-blog"><i class="ph ph-pencil"></i></div><p class="pt" style="margin-bottom:0">Artículos del Blog</p></div>'),
    
    # Reclamos (h2, no surrounding div)
    (r'<h2 class="pt">Libro de Reclamaciones</h2>',
     r'<div style="display:flex;align-items:center;margin-bottom:20px;"><div class="btn-card-icon card-icon-reclamos"><i class="ph ph-scales"></i></div><h2 class="pt" style="margin-bottom:0">Libro de Reclamaciones</h2></div>'),
    
    # Contenido - individual tabs (no surrounding div, just a p and a ps immediately after, but the structure might be `<p class="pt">...</p><p class="ps">...</p>`)
    # Wait, looking closely at grep search earlier: `<p class="pt">🏠 Página de Inicio</p><p class="ps">Contenido principal del sitio</p>`
    (r'<p class="pt">🏠 Página de Inicio</p><p class="ps">Contenido principal del sitio</p>',
     r'<div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-contenido"><i class="ph ph-house"></i></div><div><p class="pt" style="margin-bottom:0">Página de Inicio</p><p class="ps">Contenido principal del sitio</p></div></div>'),

    (r'<p class="pt">ℹ️ Página Sobre Nosotros</p><p class="ps">Contenido de "About Us"</p>',
     r'<div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-contenido"><i class="ph ph-info"></i></div><div><p class="pt" style="margin-bottom:0">Página Sobre Nosotros</p><p class="ps">Contenido de "About Us"</p></div></div>'),

    (r'<p class="pt">📞 Página de Contacto</p><p class="ps">Información de contacto y datos de la empresa</p>',
     r'<div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-contenido"><i class="ph ph-phone"></i></div><div><p class="pt" style="margin-bottom:0">Página de Contacto</p><p class="ps">Información de contacto y datos de la empresa</p></div></div>'),

    (r'<p class="pt">⚙️ Datos Globales del Sitio</p><p class="ps">Información general del negocio</p>',
     r'<div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-contenido"><i class="ph ph-gear"></i></div><div><p class="pt" style="margin-bottom:0">Datos Globales del Sitio</p><p class="ps">Información general del negocio</p></div></div>'),
]

files_changed = 0

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    if os.path.basename(filepath) in ['panel.html', 'index.html']:
        continue
        
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Inject CSS
    if '.card-icon-tours' not in content:
        content = content.replace('</style>', css_to_inject + '</style>')
    
    # Apply HTML replacements using regex
    for old_regex, new_html in replacements:
        content = re.sub(old_regex, new_html, content)
        
    if content != original_content:
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Updated headers in {os.path.basename(filepath)}")
        files_changed += 1

print(f"Total files updated safely: {files_changed}")
