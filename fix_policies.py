import os

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

# 1. Update new.css
css_path = os.path.join(base, 'assets', 'css', 'new.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = """
/* --- Policy & Legal Pages --- */
.policy-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 60px;
  max-width: 900px;
  margin: 0 auto;
  color: rgba(255, 255, 255, 0.7);
  font-family: 'Inter', sans-serif;
  line-height: 1.8;
}
.policy-card h2, .policy-card h3, .policy-card h4 {
  color: #fff;
  font-family: 'Syne', sans-serif;
  margin-top: 40px;
  margin-bottom: 20px;
}
.policy-card h2:first-child { margin-top: 0; }
.policy-card p { margin-bottom: 20px; }
.policy-card ul, .policy-card ol { margin-bottom: 20px; padding-left: 20px; }
.policy-card li { margin-bottom: 10px; }
.policy-card a { color: var(--a); text-decoration: underline; }
.policy-card a:hover { color: #fff; }

.policy-img-placeholder {
  width: 100%;
  height: 350px;
  background: rgba(255,255,255,0.03);
  border: 2px dashed rgba(255,255,255,0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.4);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 40px;
  transition: all 0.3s;
}
.policy-img-placeholder:hover {
  background: rgba(255,255,255,0.05);
  border-color: var(--a);
  color: var(--a);
}
@media (max-width: 768px) {
  .policy-card { padding: 30px; }
  .policy-img-placeholder { height: 200px; margin-bottom: 30px; }
}
"""

if ".policy-card {" not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(new_css)

# 2. Update Legal Pages
pages = [
    'cookies-policy/index.html',
    'privacy-policy/index.html',
    'terms-and-conditions/index.html',
    'libro-de-reclamaciones/index.html',
    'faq/index.html'
]

placeholder_html = '\n      <div class="policy-img-placeholder">Image Placeholder (Owner will insert image here)</div>\n'

for page in pages:
    fpath = os.path.join(base, os.path.normpath(page))
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<div class="policy-card">' in content and 'policy-img-placeholder' not in content:
            content = content.replace('<div class="policy-card">', '<div class="policy-card">' + placeholder_html, 1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
