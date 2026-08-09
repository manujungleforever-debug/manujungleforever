import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css'

with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

# Remove the bad WhatsApp block that came from hiddenjunglecusco
bad_wa_regex = re.compile(r'/\* ── WhatsApp ── \*/.*?@keyframes waBeat \{.*?\}', re.DOTALL)
css = bad_wa_regex.sub('', css)

# Now, we need to improve the original WA animation.
# Let's find the original WA block:
# /* WA */
# .wa{position:fixed;bottom:28px;right:28px;z-index:800;...}
# .wa:hover{...}
# @keyframes wp{...}

original_wa_regex = re.compile(r'/\* WA \*/\s*\.wa\{.*?\}.*?@keyframes wp\{.*?\}', re.DOTALL)

better_wa_css = """/* WA */
.wa {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 9999;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #25D366, #128C50);
  color: #fff;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(37,211,102,0.4);
  animation: waPulseGlow 2s infinite, waFloat 4s ease-in-out infinite;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.wa::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 50%;
  border: 2px solid #25D366;
  animation: waRipple 2s linear infinite;
  z-index: -1;
}

.wa:hover {
  transform: scale(1.15) translateY(-5px);
  box-shadow: 0 15px 40px rgba(37,211,102,0.6);
  background: linear-gradient(135deg, #28E16D, #159C5A);
}

@keyframes waPulseGlow {
  0% { box-shadow: 0 0 0 0 rgba(37,211,102,0.6); }
  70% { box-shadow: 0 0 0 20px rgba(37,211,102,0); }
  100% { box-shadow: 0 0 0 0 rgba(37,211,102,0); }
}

@keyframes waFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes waRipple {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.6); opacity: 0; }
}"""

if original_wa_regex.search(css):
    css = original_wa_regex.sub(better_wa_css, css)
else:
    # Append if not found
    css += "\n" + better_wa_css

# Write back to new.css
with open(path, 'w', encoding='utf-8') as f:
    f.write(css)

print("WhatsApp CSS updated successfully.")
