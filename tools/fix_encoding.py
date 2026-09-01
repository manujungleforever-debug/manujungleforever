import glob
import re
import html

# Unescape all HTML entities first, specifically looking for the Spanish ones that were corrupted
# We can just run html.unescape() because it safely converts &aacute; to á, etc.

files = glob.glob('g:/Git/MANUJUNGLEFOREVER/www.manujungleforever.com/admin/*.html')

icon_replacements = {
    # Toolbars and Buttons
    '?? Link': '<i class="ph ph-link"></i> Link',
    '?? Subir archivo(s)': '<i class="ph ph-upload-simple"></i> Subir archivo(s)',
    '?? Subir carpeta': '<i class="ph ph-folder-plus"></i> Subir carpeta',
    '??? Eliminar': '<i class="ph ph-trash"></i> Eliminar',
    '?? Editar': '<i class="ph ph-pencil-simple"></i> Editar',
    '?? Exportar': '<i class="ph ph-export"></i> Exportar',
    
    # State Labels inside JS
    '? PUBLICADO': '<i class="ph ph-check-circle"></i> PUBLICADO',
    '?? BORRADOR': '<i class="ph ph-pencil-simple"></i> BORRADOR',
    '? Publicado': '🟢 Publicado',
    '?? Borrador': '🟡 Borrador',
    
    # Select Options
    '? Activo': '🟢 Activo',
    '?? Pausado': '⏸️ Pausado',
    '? Inactivo': '🔴 Inactivo',
    
    '? Visible': '🟢 Visible',
    '? Oculto': '🔴 Oculto',
    '? Completado': '🟢 Completado',
    '? Error Crítico': '🚨 Error Crítico',
    '? Error': '🔴 Error',
    
    # Menu Items
    '??? Medios': '<i class="ph ph-image"></i> Medios',
    '??? Biblioteca': '<i class="ph ph-books"></i> Biblioteca',
    '?? Archivo': '<i class="ph ph-file"></i> Archivo',
    '?? Carpeta': '<i class="ph ph-folder"></i> Carpeta',
    '?? Tours': '<i class="ph ph-map-pin"></i> Tours',
    '?? Artículos': '<i class="ph ph-article"></i> Artículos',
    '? Testimonios': '<i class="ph ph-chat-centered-text"></i> Testimonios',
    '? Blog': '<i class="ph ph-notebook"></i> Blog',

    # Specifics
    '?? De': 'De',
    '???': '<i class="ph ph-trash"></i>', # Catch-all for standalone ??? like delete buttons
}

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # Step 1: Unescape all HTML entities recursively until no more HTML entities exist 
    # to fix double encoding like &amp;iacute; -> &iacute; -> í
    for _ in range(3):
        content = html.unescape(content)
        
    # Step 2: Fix the specific icons
    for bad, good in icon_replacements.items():
        content = content.replace(bad, good)
        
    # Step 3: Specific fixes for lingering `?` that are corruptions
    content = content.replace('? Error Crítico', '🚨 Error Crítico')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath.split('/')[-1]}")
