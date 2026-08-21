import glob, os, re

css_2row = """
/* ─── 2-ROW CENTERED ADMIN HEADER ─── */
header {
    position: sticky !important;
    top: 0 !important;
    z-index: 200 !important;
    background: rgba(3, 8, 7, 0.95) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-bottom: 1.5px solid rgba(45, 212, 191, 0.22) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
    width: 100% !important;
}

.header-container, .header-wrap, .hw {
    max-width: 1200px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 12px 20px 14px !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
}

.header-top-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
}

.logo-brand, .logo-wrap, .logo-img-wrap {
    display: inline-flex !important;
    align-items: center !important;
    position: relative !important;
    text-decoration: none !important;
}

.admin-main-logo, .logo-wrap img, .logo-img-wrap img {
    height: 110px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
    filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.65)) !important;
    transition: transform 0.25s ease, filter 0.25s ease !important;
}

.logo-brand:hover .admin-main-logo,
.logo-brand:hover .logo-wrap img,
.logo-brand:hover .logo-img-wrap img {
    transform: scale(1.02) !important;
    filter: drop-shadow(0 6px 20px rgba(45, 212, 191, 0.35)) !important;
}

.logo-glow {
    position: absolute !important;
    inset: -6px !important;
    background: radial-gradient(circle, rgba(45, 212, 191, 0.35) 0%, transparent 70%) !important;
    filter: blur(14px) !important;
    opacity: 0.4 !important;
    border-radius: 50% !important;
    pointer-events: none !important;
}

.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    margin: 0 !important;
    flex-shrink: 0 !important;
}

.user-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    background: rgba(11, 38, 35, 0.8) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.35) !important;
    padding: 4px 14px 4px 4px !important;
    border-radius: 36px !important;
    font-size: 0.90rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    backdrop-filter: blur(8px) !important;
}

.user-pill.superuser {
    border-color: rgba(201, 168, 76, 0.55) !important;
    box-shadow: 0 4px 18px rgba(201, 168, 76, 0.25) !important;
}

.user-pill img {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #2dd4bf !important;
    display: block !important;
    box-shadow: 0 0 12px rgba(45, 212, 191, 0.45) !important;
}

.user-pill.superuser img {
    border-color: #c9a84c !important;
    box-shadow: 0 0 12px rgba(201, 168, 76, 0.45) !important;
}

.user-pill .initial-avatar {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    background: rgba(45, 212, 191, 0.2) !important;
    color: #2dd4bf !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: 2px solid #2dd4bf !important;
}

.user-pill.superuser .initial-avatar {
    background: rgba(201, 168, 76, 0.2) !important;
    color: #fbbf24 !important;
    border-color: #c9a84c !important;
}

.user-pill-name {
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    max-width: 160px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

.btn-logout {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
    color: #fff !important;
    border: none !important;
    cursor: pointer !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    padding: 9px 18px !important;
    border-radius: 10px !important;
    transition: all 0.25s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35) !important;
    white-space: nowrap !important;
}

.btn-logout:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(239, 68, 68, 0.55) !important;
    filter: brightness(1.1) !important;
}

/* Fila 2: Barra de Navegación */
.header-nav-row {
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

nav.mnav {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    flex-wrap: wrap !important;
    background: rgba(11, 38, 35, 0.55) !important;
    border: 1px solid rgba(45, 212, 191, 0.22) !important;
    border-radius: 14px !important;
    padding: 6px 12px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
    backdrop-filter: blur(8px) !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

nav.mnav a {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    padding: 7px 13px !important;
    border-radius: 9px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    text-decoration: none !important;
}

nav.mnav a i {
    font-size: 1.1rem !important;
}

nav.mnav a:hover {
    color: #2dd4bf !important;
    background: rgba(45, 212, 191, 0.12) !important;
}

nav.mnav a.active {
    color: #030807 !important;
    background: #2dd4bf !important;
    box-shadow: 0 0 16px rgba(45, 212, 191, 0.45) !important;
    font-weight: 700 !important;
}

nav.mnav a.active i {
    color: #030807 !important;
}

nav.mnav a.btn-panel-link {
    background: rgba(45, 212, 191, 0.15) !important;
    border: 1px solid rgba(45, 212, 191, 0.35) !important;
    color: #2dd4bf !important;
}

nav.mnav a.btn-panel-link:hover {
    background: #2dd4bf !important;
    color: #030807 !important;
}
"""

def get_header_html(active_slug):
    nav_links = [
        ("panel", "panel.html", "ph-house", "Panel"),
        ("tours", "gestionar-tours.html", "ph-map-trifold", "Tours"),
        ("blog", "gestionar-blog.html", "ph-pencil", "Blog"),
        ("contenido", "gestionar-contenido.html", "ph-file-text", "Contenido"),
        ("salidas", "gestionar-salidas.html", "ph-calendar", "Salidas"),
        ("testimonios", "gestionar-testimonios.html", "ph-star", "Testimonios"),
        ("reclamos", "gestionar-reclamos.html", "ph-scales", "Reclamos"),
        ("medios", "gestionar-medios.html", "ph-image", "Medios"),
        ("usuarios", "gestionar-usuarios.html", "ph-users-three", "Usuarios"),
    ]
    
    links_html = []
    for slug, href, icon, label in nav_links:
        is_active = (slug == active_slug)
        cls = "active" if is_active else ""
        id_attr = ' id="nav-usuarios"' if slug == "usuarios" else ""
        links_html.append(f'        <a href="{href}" class="{cls}"{id_attr}><i class="ph {icon}"></i> {label}</a>')
    
    nav_inner = "\n".join(links_html)
    
    return f"""<header>
  <div class="header-container">
    <!-- Fila 1: Logo grande y grueso a la izquierda, Usuario y Salir a la derecha -->
    <div class="header-top-row">
      <a href="/" class="logo-brand" title="Ir al Home de Manu Jungle Forever">
        <div class="logo-wrap">
          <div class="logo-glow"></div>
          <img src="../assets/img/logo.png" alt="Manu Jungle Forever Logo" class="admin-main-logo">
        </div>
      </a>
      <div class="user-sec">
        <span id="huser"></span>
        <button onclick="logout()" class="btn-logout" title="Cerrar sesión">
          <i class="ph ph-sign-out"></i> Salir
        </button>
      </div>
    </div>

    <!-- Fila 2: Menú de Navegación dedicado -->
    <div class="header-nav-row">
      <nav class="mnav">
{nav_inner}
      </nav>
    </div>
  </div>
</header>"""

admin_dirs = ['admin', 'www.manujungleforever.com/admin']

page_slugs = {
    'panel.html': 'panel',
    'gestionar-tours.html': 'tours',
    'gestionar-blog.html': 'blog',
    'gestionar-contenido.html': 'contenido',
    'gestionar-salidas.html': 'salidas',
    'gestionar-testimonios.html': 'testimonios',
    'gestionar-reclamos.html': 'reclamos',
    'gestionar-medios.html': 'medios',
    'gestionar-usuarios.html': 'usuarios',
}

for d in admin_dirs:
    for fname, slug in page_slugs.items():
        fpath = os.path.join(d, fname)
        if not os.path.exists(fpath):
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean previous header style injections
        content = re.sub(r'<style>\s*/\* Single-line header styles \*/.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Grand single-line header styles.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Compact Unified Admin Header.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Responsive Single-Line Header.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* ─── 2-ROW CENTERED ADMIN HEADER ───.*?</style>', '', content, flags=re.DOTALL)
        
        # Replace <header>...</header>
        header_markup = get_header_html(slug)
        content = re.sub(r'<header>.*?</header>', header_markup, content, flags=re.DOTALL)
        
        # Inject new CSS before </head>
        content = content.replace('</head>', f'<style>\n{css_2row}\n</style>\n</head>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied 2-row centered header in {fpath}")

print("Done updating all admin files to 2-row centered header.")
