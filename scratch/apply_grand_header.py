import glob, os, re

# Grand header CSS with 76px majestic logo and perfect single-line layout
grand_header_css = """
/* Grand single-line header styles with large 76px logo */
header {
    position: sticky !important;
    top: 0 !important;
    z-index: 200 !important;
    background: rgba(3, 8, 7, 0.96) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-bottom: 1.5px solid rgba(45, 212, 191, 0.22) !important;
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.55) !important;
}
header .hw, header .header-wrap {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 10px 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 16px !important;
    flex-wrap: nowrap !important;
    box-sizing: border-box !important;
    min-height: 90px !important;
}
.logo-wrap, .logo-img-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    flex-shrink: 0 !important;
}
.logo-wrap img, .logo-img-wrap img {
    height: 76px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
    filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.5)) !important;
    transition: transform 0.25s ease !important;
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
    border: 1.5px solid rgba(45, 212, 191, 0.35) !important;
    color: var(--teal, #2dd4bf) !important;
    padding: 8px 14px !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: .25s !important;
    flex-shrink: 0 !important;
}
.btn-panel:hover {
    background: var(--teal, #2dd4bf) !important;
    color: #030807 !important;
    box-shadow: 0 0 16px rgba(45, 212, 191, 0.4) !important;
}
nav.mnav {
    display: flex !important;
    align-items: center !important;
    gap: 5px !important;
    flex-wrap: nowrap !important;
    flex: 1 1 auto !important;
    justify-content: center !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    margin: 0 10px !important;
}
nav.mnav::-webkit-scrollbar { display: none; }
nav.mnav a {
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    padding: 8px 12px !important;
    border-radius: 9px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-shrink: 0 !important;
    letter-spacing: -0.2px !important;
    transition: all 0.25s ease !important;
    text-decoration: none !important;
}
nav.mnav a i {
    font-size: 1.12rem !important;
}
nav.mnav a:hover, nav.mnav a.active {
    color: #2dd4bf !important;
    background: rgba(45, 212, 191, 0.14) !important;
    box-shadow: 0 0 16px rgba(45, 212, 191, 0.15) !important;
}
.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
.user-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    background: rgba(11, 38, 35, 0.75) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.3) !important;
    padding: 4px 14px 4px 4px !important;
    border-radius: 36px !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}
.user-pill.superuser {
    border-color: rgba(201, 168, 76, 0.5) !important;
    box-shadow: 0 4px 18px rgba(201, 168, 76, 0.2) !important;
}
.user-pill img {
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #2dd4bf !important;
    display: block !important;
    box-shadow: 0 0 12px rgba(45, 212, 191, 0.4) !important;
}
.user-pill.superuser img {
    border-color: #c9a84c !important;
    box-shadow: 0 0 12px rgba(201, 168, 76, 0.4) !important;
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
    font-size: 0.94rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    max-width: 150px !important;
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
    border-radius: 11px !important;
    transition: .25s !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35) !important;
    white-space: nowrap !important;
}
.btn-logout:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.55) !important;
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
        
        # Replace inline logo height with 76px
        content = re.sub(r'style="height:\s*\d+px[^"]*"', 'style="height: 76px; width: auto;"', content)
        
        # Inject Grand CSS before </head>
        content = content.replace('</head>', f'<style>\n{grand_header_css}\n</style>\n</head>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied 76px grand header in {fpath}")
