import glob, os, re

# 1. Update CSS with mobile/tablet optimizations
responsive_css = """
/* ─────────────────────────────────────────────────────────────
   MOBILE & TABLET RESPONSIVENESS + ADMIN LOGIN ICON
   ───────────────────────────────────────────────────────────── */
.nav-admin-btn {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #ffffff !important;
  text-decoration: none !important;
  transition: all 0.3s ease;
  flex-shrink: 0;
  cursor: pointer;
}
.nav-admin-btn:hover {
  background: rgba(45, 212, 191, 0.25) !important;
  border-color: #2dd4bf !important;
  color: #2dd4bf !important;
  box-shadow: 0 0 14px rgba(45, 212, 191, 0.45);
}

.header-right-actions {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}

@media (max-width: 1024px) {
  .tour-page-grid {
    grid-template-columns: 1fr !important;
    gap: 36px !important;
  }
  .cx {
    padding-left: 20px !important;
    padding-right: 20px !important;
  }
  .ni {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
  }
  .nl img {
    max-height: 48px;
    width: auto;
  }
}

@media (max-width: 768px) {
  .tour-page-grid {
    grid-template-columns: 1fr !important;
  }
  .in-hero {
    padding: 130px 0 60px !important;
  }
  .h1 {
    font-size: 2.1rem !important;
  }
  .h2 {
    font-size: 1.7rem !important;
  }
  .nl img {
    max-height: 40px !important;
    width: auto;
  }
  .mo {
    padding-top: 90px !important;
  }
  .ml li a {
    font-size: 1.1rem !important;
    padding: 8px 0 !important;
  }
  .fg {
    grid-template-columns: 1fr !important;
    gap: 30px !important;
  }
}
"""

for css_file in ['www.manujungleforever.com/assets/css/new.css', 'www.manujungleforever.com/assets/css/style.css']:
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'MOBILE & TABLET RESPONSIVENESS + ADMIN LOGIN ICON' not in content:
            content += '\n' + responsive_css
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added responsive CSS to {css_file}")

# 2. Update all public HTML files
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if not f.replace('\\', '/').startswith('www.manujungleforever.com/admin')]

admin_btn_markup = '<a href="/admin/index.html" class="nav-admin-btn" aria-label="Admin Login" title="Admin Login"><i class="fa-solid fa-user-shield"></i></a>'
mobile_drawer_item = '<li style="margin-top:14px; border-top:1px solid rgba(255,255,255,0.08); padding-top:10px;"><a href="/admin/index.html" style="display:flex; align-items:center; gap:10px; color:#2dd4bf; font-weight:600;"><i class="fa-solid fa-user-shield" style="font-size:1.1rem;"></i> Admin Access</a></li>'

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # A. Remove old user-shield if inside nav.nm
    c = re.sub(
        r'<a href="https?://www\.manujungleforever\.com/admin/index\.html"[^>]*><i class="fa-solid fa-user-shield"></i></a>',
        '',
        c
    )
    c = re.sub(
        r'<a href="/admin/index\.html"[^>]*class="nav-admin-btn"[^>]*><i class="fa-solid fa-user-shield"></i></a>',
        '',
        c
    )

    # B. Replace hamburger button with header-right-actions containing login icon + hamburger
    # Match <button class="bg" id="bg" ...>...</button>
    old_bg_pattern = re.compile(
        r'(?:<div class="header-right-actions"[^>]*>[\s\S]*?</div>|<button class="bg" id="bg"[^>]*>[\s\S]*?</button>)',
        re.DOTALL
    )
    
    new_header_actions = f"""<div class="header-right-actions">
    {admin_btn_markup}
    <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false"><span class="bb"></span><span class="bb"></span><span class="bb"></span></button>
  </div>"""

    if old_bg_pattern.search(c):
        c = old_bg_pattern.sub(lambda m: new_header_actions, c, count=1)

    # C. Ensure mobile drawer .mo has Admin Access link at end of .ml
    if 'Admin Access' not in c and '<div class="mo"' in c:
        c = re.sub(
            r'(<div class="mo"[\s\S]*?<ul class="ml">[\s\S]*?)(</ul>\s*</div>)',
            f'\\1  {mobile_drawer_item}\n  \\2',
            c
        )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Updated all {len(html_files)} public HTML files with mobile login icon and responsiveness.")
