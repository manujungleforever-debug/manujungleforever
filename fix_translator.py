import os
import re

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")
css_path = os.path.join(base_dir, "assets", "css", "new.css")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the old language selector in the header
old_selector = r'<div class="lang-selector">.*?</div>'
new_selector = """<div class="ls-custom" tabindex="0">
      <div class="ls-current"><span class="flg">🇺🇸</span> EN</div>
      <ul class="ls-options">
        <li onclick="doTranslate('en')"><span class="flg">🇺🇸</span> EN</li>
        <li onclick="doTranslate('es')"><span class="flg">🇪🇸</span> ES</li>
      </ul>
    </div>
    <div id="google_translate_element" style="display:none;"></div>"""

if re.search(old_selector, content, flags=re.DOTALL):
    content = re.sub(old_selector, new_selector, content, flags=re.DOTALL)
else:
    print("Could not find old selector in index.php")

# 2. Replace the old JS script
old_script = r'<script type="text/javascript">\s*function googleTranslateElementInit.*?</script>'
new_script = """<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en', includedLanguages: 'en,es', autoDisplay: false}, 'google_translate_element');
}
function doTranslate(lang) {
  document.cookie = "googtrans=/en/" + lang + "; path=/;";
  window.location.reload();
}
// Set current language display on load
document.addEventListener("DOMContentLoaded", function() {
  if (document.cookie.indexOf("googtrans=/en/es") !== -1) {
    document.querySelector(".ls-current").innerHTML = '<span class="flg">🇪🇸</span> ES';
  }
});
</script>"""

if re.search(old_script, content, flags=re.DOTALL):
    content = re.sub(old_script, new_script, content, flags=re.DOTALL)
else:
    print("Could not find old JS script in index.php")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

# 3. Update CSS
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Remove old .lang-selector rules
css_content = re.sub(r'/\* Language Selector \*/.*', '', css_content, flags=re.DOTALL)

# Add new styles
new_css = """
/* Language Selector */
.ls-custom {
  position: relative;
  display: inline-block;
  margin-right: 12px;
  margin-left: 8px;
  cursor: pointer;
  z-index: 1000;
}
.ls-current {
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.1);
  color: #fff;
  padding: 8px 16px;
  border-radius: 24px;
  font-weight: 600;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 6px;
  backdrop-filter: blur(10px);
  transition: 0.3s;
}
.ls-current:hover {
  background: rgba(255,255,255,.1);
}
.ls-options {
  position: absolute;
  top: 110%;
  left: 0;
  background: var(--k);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 12px;
  list-style: none;
  padding: 8px 0;
  margin: 0;
  width: 100px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: 0.3s;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.ls-custom:focus-within .ls-options, .ls-custom:hover .ls-options {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.ls-options li {
  padding: 8px 16px;
  color: rgba(255,255,255,.8);
  font-weight: 500;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
}
.ls-options li:hover {
  background: rgba(255,255,255,.05);
  color: var(--a);
}
.flg {
  font-size: 1.1rem;
}
"""
css_content += new_css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("Updated translation logic and styles.")
