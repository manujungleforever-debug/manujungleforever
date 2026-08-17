import os
import codecs
import glob

# Path to the admin directory
admin_dir = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin'

# The exact snippet to replace in the subpages
old_logo_snippet = '''                <a href="panel.html" class="logo-brand">
                    <div class="logo-img-wrap">
                        <div class="logo-glow"></div>
                        <img src="../assets/img/logo.png" alt="Manu Jungle Logo">
                    </div>
                    <span class="brand-text">Manu Jungle</span>
                </a>'''

new_logo_snippet = '''                <a href="/" class="logo-brand" title="Ir al Home de Manu Jungle Forever">
                    <div class="logo-img-wrap">
                        <div class="logo-glow"></div>
                        <img src="../assets/img/logo.png" alt="Manu Jungle Logo" style="height: 80px; width: auto; max-width: none;">
                    </div>
                </a>'''

files_changed = 0

for filepath in glob.glob(os.path.join(admin_dir, '*.html')):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        content = f.read()
    
    if old_logo_snippet in content:
        content = content.replace(old_logo_snippet, new_logo_snippet)
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
        print(f"Updated logo in {os.path.basename(filepath)}")
        files_changed += 1

print(f"Total files updated with new logo: {files_changed}")

# Now, update panel.html to fix the special home button
panel_path = os.path.join(admin_dir, 'panel.html')
with codecs.open(panel_path, 'r', 'utf-8') as f:
    panel_content = f.read()

# Add the css for bg-home
css_insertion_point = ".btn-card-content {"
bg_home_css = '''        .menu-btn-card.bg-home {
            background-image: linear-gradient(to right, rgba(3,8,7,0.85), rgba(3,8,7,0.7)), url('../assets/img/tour2.webp');
            background-size: cover;
            background-position: center;
            border-color: rgba(16, 185, 129, 0.4);
        }
        .menu-btn-card.bg-home:hover {
            border-color: #10b981;
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);
        }
        
        .btn-card-content {'''

if "menu-btn-card.bg-home" not in panel_content:
    panel_content = panel_content.replace(css_insertion_point, bg_home_css)

# Update the button HTML
old_btn = '''                <!-- Regresar al panel -->
                <div class="menu-btn-card" onclick="window.location.href='panel.html'">
                    <div class="btn-card-icon card-icon-web"><i class="ph ph-squares-four"></i></div>
                    <div class="btn-card-content">
                        <span class="btn-card-title">Regresar al Panel</span>
                        <span class="btn-card-desc">Vuelve a la vista principal del administrador.</span>
                    </div>
                </div>'''

new_btn = '''                <!-- Regresar a la web -->
                <div class="menu-btn-card bg-home" onclick="window.location.href='/'">
                    <div class="btn-card-icon card-icon-web"><i class="ph ph-globe-hemisphere-west"></i></div>
                    <div class="btn-card-content">
                        <span class="btn-card-title" style="color: #10b981;">Ver Sitio Web</span>
                        <span class="btn-card-desc">Ir a la página pública de Manu Jungle Forever.</span>
                    </div>
                </div>'''

panel_content = panel_content.replace(old_btn, new_btn)

with codecs.open(panel_path, 'w', 'utf-8') as f:
    f.write(panel_content)

print("Updated panel.html with special bg-home button")
