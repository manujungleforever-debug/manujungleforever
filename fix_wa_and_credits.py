import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

# 1. Update new.css
css_path = os.path.join(base, 'assets', 'css', 'new.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = """
/* --- WA Animation & Tooltip --- */
@keyframes waBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.wa-wrap {
  animation: waBounce 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.wa-wrap .wa-tooltip {
  position: absolute;
  right: 75px;
  top: 50%;
  transform: translateY(-50%) translateX(10px);
  background: #fff;
  color: #002e24;
  padding: 8px 16px;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  pointer-events: none;
}
.wa-wrap .wa-tooltip::after {
  content: '';
  position: absolute;
  right: -6px;
  top: 50%;
  transform: translateY(-50%);
  border-width: 6px 0 6px 6px;
  border-style: solid;
  border-color: transparent transparent transparent #fff;
}
.wa-wrap:hover .wa-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateY(-50%) translateX(0);
}

/* --- Footer Credits Responsiveness --- */
.fb { border-top: 1px solid rgba(255,255,255,0.05); padding: 24px 0; margin-top: 40px; width: 100%; }
.fbi { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 15px; font-size: 0.8rem; color: rgba(255,255,255,0.5); font-family: 'Inter', sans-serif; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 20px; }
@media (max-width: 768px) {
  .fbi { flex-direction: column; text-align: center; justify-content: center; }
}
"""

if "waBounce" not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(new_css)

# 2. Update HTML/PHP files
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<div class="wa-wrap">' in content and 'wa-tooltip' not in content:
            content = content.replace('<div class="wa-wrap">', '<div class="wa-wrap">\n    <div class="wa-tooltip">How can I help you?</div>')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
