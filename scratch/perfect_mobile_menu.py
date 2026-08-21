import glob, os, re

# 1. Fix new.css
css_path = 'www.manujungleforever.com/assets/css/new.css'
with open(css_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace line 242 .mb modal box selector
c = c.replace(
    '.mb{background:var(--d);border:1px solid rgba(255,255,255,.09);border-radius:20px;width:100%;max-width:580px;max-height:90vh;overflow-y:auto;padding:44px;position:relative;transform:translateY(20px);transition:transform var(--t)}',
    '.modal-box{background:var(--d);border:1px solid rgba(255,255,255,.09);border-radius:20px;width:100%;max-width:580px;max-height:90vh;overflow-y:auto;padding:44px;position:relative;transform:translateY(20px);transition:transform var(--t)}'
)
c = c.replace('.modal.o .mb{transform:none}', '.modal.o .modal-box{transform:none}')

# Add robust styling for mobile menu toggle button
m_toggle_css = """
/* ─────────────────────────────────────────────────────────────
   MOBILE DRAWER NAVIGATION - SEAMLESS MENU ITEMS
   ───────────────────────────────────────────────────────────── */
.mo .ml {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.mo .ml > li {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  margin: 0 !important;
  padding: 0 !important;
}

.mo .ml > li > a,
.mo .ml > li > button,
.mo .ml > li > .m-toggle-btn,
.mo .ml > li > .mb,
.mo .ml > li > .m-btn,
#mbt {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  width: 100% !important;
  max-width: 100% !important;
  padding: 16px 0 !important;
  margin: 0 !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  color: #ffffff !important;
  font-family: inherit !important;
  font-size: 1.1rem !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  text-align: left !important;
  box-shadow: none !important;
  transform: none !important;
  cursor: pointer !important;
  outline: none !important;
  -webkit-appearance: none !important;
  appearance: none !important;
  box-sizing: border-box !important;
}

.mo .ml > li > a:hover,
.mo .ml > li > button:hover,
.mo .ml > li > .m-toggle-btn:hover,
#mbt:hover {
  color: var(--a, #2dd4bf) !important;
  background: transparent !important;
}

.mo .ml > li > button i,
.mo .ml > li > .m-toggle-btn i,
#mbt i {
  color: var(--a, #2dd4bf) !important;
  font-size: 0.95rem !important;
  margin-left: auto !important;
  transition: transform 0.3s ease !important;
}

.mo .ml > li > button.active i,
.mo .ml > li > .m-toggle-btn.active i,
#mbt.active i {
  transform: rotate(180deg) !important;
}

.md {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease;
  padding-left: 10px;
}
.md.o {
  max-height: 850px;
  overflow-y: auto;
}
"""

if 'MOBILE DRAWER NAVIGATION - SEAMLESS MENU ITEMS' not in c:
    c += '\n' + m_toggle_css
else:
    c = re.sub(r'/\* ─+[\s\S]*?MOBILE DRAWER NAVIGATION - SEAMLESS MENU ITEMS[\s\S]*?\*/[\s\S]*?(?=\n/\*|\Z)', m_toggle_css, c)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated new.css")

# 2. Fix style.css
style_css_path = 'www.manujungleforever.com/assets/css/style.css'
if os.path.exists(style_css_path):
    with open(style_css_path, 'r', encoding='utf-8') as f:
        sc = f.read()
    if 'MOBILE DRAWER NAVIGATION - SEAMLESS MENU ITEMS' not in sc:
        sc += '\n' + m_toggle_css
    with open(style_css_path, 'w', encoding='utf-8') as f:
        f.write(sc)
    print("Updated style.css")

# 3. Update all public HTML files
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if not f.replace('\\', '/').startswith('www.manujungleforever.com/admin')]

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace <button class="mb" id="mbt"> with <button class="m-toggle-btn" id="mbt" type="button">
    html = re.sub(
        r'<button[^>]*id="mbt"[^>]*>([\s\S]*?)</button>',
        r'<button class="m-toggle-btn" id="mbt" type="button">\1</button>',
        html
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

print(f"Updated all {len(html_files)} public HTML files with class='m-toggle-btn'.")
