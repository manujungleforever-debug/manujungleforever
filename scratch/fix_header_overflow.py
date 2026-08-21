import glob, os, re

# Definitive single-line responsive header CSS
responsive_header_css = """
/* Responsive Single-Line Header - Zero clipping on 1200px - 4K screens */
header {
    position: sticky !important;
    top: 0 !important;
    z-index: 200 !important;
    background: rgba(3, 8, 7, 0.96) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-bottom: 1.5px solid rgba(45, 212, 191, 0.2) !important;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5) !important;
}
header .hw, header .header-wrap {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 8px 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    flex-wrap: nowrap !important;
    box-sizing: border-box !important;
}
.logo-wrap, .logo-img-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    flex-shrink: 0 !important;
}
.logo-wrap img, .logo-img-wrap img {
    height: 58px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.5)) !important;
    transition: transform 0.2s ease !important;
}
.logo-wrap img:hover, .logo-img-wrap img:hover {
    transform: scale(1.02) !important;
}
.logo-brand {
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    text-decoration: none !important;
}
.btn-panel {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    background: rgba(45, 212, 191, 0.12) !important;
    border: 1px solid rgba(45, 212, 191, 0.35) !important;
    color: var(--teal, #2dd4bf) !important;
    padding: 7px 12px !important;
    border-radius: 9px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: .2s !important;
    flex-shrink: 0 !important;
}
.btn-panel:hover {
    background: var(--teal, #2dd4bf) !important;
    color: #030807 !important;
    box-shadow: 0 0 14px rgba(45, 212, 191, 0.4) !important;
}
nav.mnav {
    display: flex !important;
    align-items: center !important;
    gap: 3px !important;
    flex-wrap: nowrap !important;
    flex: 1 1 auto !important;
    justify-content: center !important;
    overflow: visible !important;
    margin: 0 6px !important;
}
nav.mnav a {
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    padding: 7px 9px !important;
    border-radius: 8px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    flex-shrink: 0 !important;
    letter-spacing: -0.2px !important;
    transition: all 0.2s ease !important;
    text-decoration: none !important;
}
nav.mnav a i {
    font-size: 1rem !important;
}
nav.mnav a:hover, nav.mnav a.active {
    color: #2dd4bf !important;
    background: rgba(45, 212, 191, 0.14) !important;
    box-shadow: 0 0 12px rgba(45, 212, 191, 0.15) !important;
}
.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
.user-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    background: rgba(11, 38, 35, 0.75) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.3) !important;
    padding: 3px 12px 3px 3px !important;
    border-radius: 30px !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}
.user-pill.superuser {
    border-color: rgba(201, 168, 76, 0.5) !important;
    box-shadow: 0 4px 18px rgba(201, 168, 76, 0.2) !important;
}
.user-pill img {
    width: 34px !important;
    height: 34px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 1.5px solid #2dd4bf !important;
    display: block !important;
}
.user-pill.superuser img {
    border-color: #c9a84c !important;
}
.user-pill .initial-avatar {
    width: 34px !important;
    height: 34px !important;
    border-radius: 50% !important;
    background: rgba(45, 212, 191, 0.2) !important;
    color: #2dd4bf !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: 1.5px solid #2dd4bf !important;
}
.user-pill.superuser .initial-avatar {
    background: rgba(201, 168, 76, 0.2) !important;
    color: #fbbf24 !important;
    border-color: #c9a84c !important;
}
.user-pill-name {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    max-width: 140px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
.btn-logout {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
    color: #fff !important;
    border: none !important;
    cursor: pointer !important;
    font-size: 0.84rem !important;
    font-weight: 700 !important;
    padding: 8px 15px !important;
    border-radius: 10px !important;
    transition: .2s !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35) !important;
    white-space: nowrap !important;
}
.btn-logout:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(239, 68, 68, 0.55) !important;
}
"""

admin_dirs = ['admin', 'www.manujungleforever.com/admin']
for d in admin_dirs:
    for fpath in glob.glob(f'{d}/*.html'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean previous header style injections
        content = re.sub(r'<style>\s*/\* Single-line header styles \*/.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Grand single-line header styles.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Responsive Single-Line Header.*?</style>', '', content, flags=re.DOTALL)
        
        # Set clean 58px logo height
        content = re.sub(r'style="height:\s*\d+px[^"]*"', 'style="height: 58px; width: auto;"', content)
        
        # Inject responsive header CSS before </head>
        content = content.replace('</head>', f'<style>\n{responsive_header_css}\n</style>\n</head>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied responsive header in {fpath}")
