import glob, os, re

# Grand single-line header CSS with large 110px logo
grand_header_css = """
/* Grand single-line header styles with large logo */
header {
    position: sticky !important;
    top: 0 !important;
    z-index: 200 !important;
    background: rgba(3, 8, 7, 0.96) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-bottom: 1.5px solid rgba(45, 212, 191, 0.22) !important;
    box-shadow: 0 8px 36px rgba(0, 0, 0, 0.6) !important;
}
header .hw, header .header-wrap {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 8px 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 24px !important;
    flex-wrap: nowrap !important;
    box-sizing: border-box !important;
    min-height: 115px !important;
}
.logo-wrap, .logo-img-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    flex-shrink: 0 !important;
}
.logo-wrap img, .logo-img-wrap img {
    height: 110px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.6)) !important;
    transition: transform 0.25s ease !important;
}
.logo-wrap img:hover, .logo-img-wrap img:hover {
    transform: scale(1.03) !important;
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
    gap: 8px !important;
    background: rgba(45, 212, 191, 0.14) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.4) !important;
    color: var(--teal, #2dd4bf) !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: .25s !important;
    flex-shrink: 0 !important;
}
.btn-panel:hover {
    background: var(--teal, #2dd4bf) !important;
    color: #030807 !important;
    box-shadow: 0 0 20px rgba(45, 212, 191, 0.5) !important;
}
nav.mnav {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-wrap: nowrap !important;
    flex: 1 1 auto !important;
    justify-content: center !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    margin: 0 16px !important;
}
nav.mnav::-webkit-scrollbar { display: none; }
nav.mnav a {
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    padding: 10px 15px !important;
    border-radius: 11px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
    letter-spacing: -0.2px !important;
    transition: all 0.25s ease !important;
}
nav.mnav a i {
    font-size: 1.2rem !important;
}
nav.mnav a:hover, nav.mnav a.active {
    color: #2dd4bf !important;
    background: rgba(45, 212, 191, 0.16) !important;
    box-shadow: 0 0 20px rgba(45, 212, 191, 0.2) !important;
}
.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 14px !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
.user-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 12px !important;
    background: rgba(11, 38, 35, 0.75) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.3) !important;
    padding: 6px 16px 6px 6px !important;
    border-radius: 40px !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.user-pill.superuser {
    border-color: rgba(201, 168, 76, 0.5) !important;
    box-shadow: 0 4px 22px rgba(201, 168, 76, 0.22) !important;
}
.user-pill img {
    width: 46px !important;
    height: 46px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #2dd4bf !important;
    display: block !important;
    box-shadow: 0 0 14px rgba(45, 212, 191, 0.5) !important;
}
.user-pill.superuser img {
    border-color: #c9a84c !important;
    box-shadow: 0 0 14px rgba(201, 168, 76, 0.5) !important;
}
.user-pill .initial-avatar {
    width: 46px !important;
    height: 46px !important;
    border-radius: 50% !important;
    background: rgba(45, 212, 191, 0.2) !important;
    color: #2dd4bf !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    border: 2px solid #2dd4bf !important;
}
.user-pill.superuser .initial-avatar {
    background: rgba(201, 168, 76, 0.2) !important;
    color: #fbbf24 !important;
    border-color: #c9a84c !important;
}
.user-pill-name {
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    max-width: 160px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
.badge.superuser {
    background: rgba(201, 168, 76, 0.25) !important;
    color: #fbbf24 !important;
    border: 1px solid rgba(201, 168, 76, 0.5) !important;
    font-size: 0.74rem !important;
    padding: 4px 10px !important;
    border-radius: 14px !important;
}
.badge.normal {
    background: rgba(45, 212, 191, 0.2) !important;
    color: #2dd4bf !important;
    border: 1px solid rgba(45, 212, 191, 0.4) !important;
    font-size: 0.74rem !important;
    padding: 4px 10px !important;
    border-radius: 14px !important;
}
.btn-logout {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
    color: #fff !important;
    border: none !important;
    cursor: pointer !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    transition: .25s !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4) !important;
    white-space: nowrap !important;
}
.btn-logout:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(239, 68, 68, 0.6) !important;
}
"""

admin_dirs = ['admin', 'www.manujungleforever.com/admin']
for d in admin_dirs:
    for fpath in glob.glob(f'{d}/*.html'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean previous header style injection
        content = re.sub(r'<style>\s*/\* Single-line header styles \*/.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Grand single-line header styles.*?</style>', '', content, flags=re.DOTALL)
        
        # Replace inline logo height with 110px
        content = re.sub(r'style="height:\s*\d+px[^"]*"', 'style="height: 110px; width: auto;"', content)
        
        # Inject CSS before </head>
        content = content.replace('</head>', f'<style>\n{grand_header_css}\n</style>\n</head>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied 110px logo and grand header in {fpath}")

