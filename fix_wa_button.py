import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

wa_new_html = """<div class="wa-wrap">
    <span class="wa-ring"></span>
    <span class="wa-ring"></span>
    <span class="wa-ring"></span>
    <a href="https://api.whatsapp.com/send?phone=51901525679&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
</div>"""

# Replace in all html/php
for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # The regex matches the existing wa tag which might have id="whats-flotante" and different quotes
            new_content = re.sub(r'<a href="https://api\.whatsapp\.com/send\?phone=[0-9]+[^"]*" class="wa"[^>]*>.*?</a>', wa_new_html, content, flags=re.DOTALL)
            
            # Also replace any existing `whats-flotante` ones just in case
            new_content = re.sub(r'<a href="[^"]*" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" id="whats-flotante">.*?</a>', wa_new_html, new_content, flags=re.DOTALL)
            
            # Update phone number in footer/header if present (+51979808013 -> +51901525679)
            new_content = new_content.replace('+51979808013', '+51901525679')
            new_content = new_content.replace('+51 979 808 013', '+51 901 525 679')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)

# Update CSS
css_path = os.path.join(base_dir, 'assets', 'css', 'new.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

wa_css = """
/* WA Neon Float */
.wa-wrap {
  position: fixed; bottom: 28px; right: 28px;
  width: 60px; height: 60px; z-index: 9998;
  display: flex; align-items: center; justify-content: center;
}
.wa-ring {
  position: absolute; top: 0; left: 0;
  width: 60px; height: 60px; border-radius: 50%;
  border: 2px solid #25D366; opacity: 0;
  animation: waPulse 2.6s ease-out infinite;
}
.wa-ring:nth-child(2) { animation-delay: 0.8s; }
.wa-ring:nth-child(3) { animation-delay: 1.6s; }
@keyframes waPulse {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.6); opacity: 0; }
}
.wa-wrap .wa {
  position: relative; z-index: 2;
  width: 58px; height: 58px; border-radius: 50%;
  background: #25D366; color: #fff; font-size: 1.7rem;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 15px rgba(37,211,102,0.4);
  transition: transform 0.3s ease;
  animation: none; /* override old wa animation */
}
.wa-wrap .wa:hover { transform: scale(1.1); box-shadow: 0 12px 40px rgba(37,211,102,0.65); }
"""

# replace old .wa rules in css
css = re.sub(r'/\* WA \*/.*?\@keyframes wp.*?\}', wa_css, css, flags=re.DOTALL)
if 'wa-wrap' not in css:
    css += wa_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated WhatsApp button and number!")
