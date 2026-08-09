import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

# 1. Update new.css
css_path = os.path.join(base, 'assets', 'css', 'new.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = """
/* --- Accordion / Itinerary Cards --- */
.itinerary-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.itinerary-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
}
.itinerary-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.15);
}
.itinerary-toggle {
  width: 100%;
  text-align: left;
  padding: 24px;
  background: none;
  border: none;
  color: #fff;
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}
.itinerary-toggle i {
  color: var(--a);
  transition: transform 0.3s;
}
.itinerary-toggle.active i {
  transform: rotate(180deg);
}
.itinerary-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease-out, padding 0.4s ease-out;
  padding: 0 24px;
}
.itinerary-toggle.active + .itinerary-content {
  padding-bottom: 24px;
}
.itinerary-content p {
  color: rgba(255,255,255,0.7);
  font-size: 0.95rem;
  line-height: 1.7;
  margin-bottom: 12px;
}
.itinerary-content p:last-child {
  margin-bottom: 0;
}
"""

if ".itinerary-card {" not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(new_css)


# 2. Update HTML/PHP files to inject JS
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

js_to_inject = """
// Accordion
window.toggleAccordion = function(btn) {
  const content = btn.nextElementSibling;
  const isActive = btn.classList.contains('active');
  
  document.querySelectorAll('.itinerary-toggle').forEach(function(otherBtn) {
    otherBtn.classList.remove('active');
    if(otherBtn.nextElementSibling) {
       otherBtn.nextElementSibling.style.maxHeight = null;
    }
  });
  
  if (!isActive) {
    btn.classList.add('active');
    if(content) {
       content.style.maxHeight = content.scrollHeight + "px";
    }
  }
};
"""

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'window.toggleAccordion' not in content:
            # We look for a good place to inject the script.
            # Almost all pages have a <script> tag before <div id="google_translate_element"
            # Let's just insert it right before </script>\n\n<div id="google_translate_element"
            if '</script>\n\n<div id="google_translate_element"' in content:
                content = content.replace('</script>\n\n<div id="google_translate_element"', js_to_inject + '\n</script>\n\n<div id="google_translate_element"')
            elif '</body>' in content:
                # Fallback
                content = content.replace('</body>', '<script>' + js_to_inject + '</script>\n</body>')
                
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error {fpath}: {e}")

print("Done.")
