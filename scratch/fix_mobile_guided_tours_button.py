import glob, os, re

# 1. Update new.css
css_path = 'www.manujungleforever.com/assets/css/new.css'
with open(css_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Fix collision on .mb in modal
c = re.sub(r'(?<!\.modal\.o )\b\.mb\s*\{', '.modal .mb, .modal-box {', c)

# Add explicit clean styles for #mbt, .ml>li>button, .mb in mobile menu
mbt_clean_css = """
/* Mobile Menu Guided Tours Dropdown Button */
.ml > li > button,
.ml > li > button.mb,
.ml > li > .m-btn,
#mbt {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  width: 100% !important;
  max-width: 100% !important;
  padding: 14px 0 !important;
  font-size: 1.05rem !important;
  font-weight: 500 !important;
  color: var(--w, #ffffff) !important;
  background: transparent !important;
  border: none !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
  border-radius: 0 !important;
  text-align: left !important;
  cursor: pointer !important;
  transform: none !important;
  margin: 0 !important;
  box-shadow: none !important;
  outline: none !important;
}

.ml > li > button:hover,
#mbt:hover {
  color: var(--a, #2dd4bf) !important;
}

.ml > li > button i,
#mbt i {
  font-size: 0.9rem !important;
  margin-left: auto !important;
  transition: transform 0.3s ease !important;
}
"""

if 'Mobile Menu Guided Tours Dropdown Button' not in c:
    c += '\n' + mbt_clean_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. Update style.css
style_css_path = 'www.manujungleforever.com/assets/css/style.css'
if os.path.exists(style_css_path):
    with open(style_css_path, 'r', encoding='utf-8') as f:
        sc = f.read()
    if 'Mobile Menu Guided Tours Dropdown Button' not in sc:
        sc += '\n' + mbt_clean_css
        with open(style_css_path, 'w', encoding='utf-8') as f:
            f.write(sc)

print("Updated CSS for Guided Tours mobile button.")
