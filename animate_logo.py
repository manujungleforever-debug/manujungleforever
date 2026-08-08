import os

css_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css"

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    # Define the new animations
    animations = """
@keyframes logoEntrance {
  0% { opacity: 0; transform: scale(0.6) translateY(-30px); filter: drop-shadow(0 0 0 rgba(16,185,129,0)); }
  40% { opacity: 1; transform: scale(1.15) translateY(0); filter: drop-shadow(0 0 40px rgba(16,185,129,0.9)); }
  70% { transform: scale(0.95); filter: drop-shadow(0 0 15px rgba(16,185,129,0.4)); }
  100% { transform: scale(1); filter: drop-shadow(0 0 20px rgba(16,185,129,0.35)); }
}
@keyframes logoHeartbeat {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 20px rgba(16,185,129,0.35)); }
  50% { transform: scale(1.05); filter: drop-shadow(0 0 35px rgba(16,185,129,0.65)); }
}
"""
    # Prepend the animations to the file (after imports)
    if "@keyframes logoEntrance" not in css:
        css = css.replace(':root{', animations + '\n:root{', 1)

    # Replace the existing .nl img styling with the animated version
    old_rule = ".nl img{height:140px;width:auto;position:relative;z-index:1;transition:height 0.4s ease, transform 0.3s ease;}"
    new_rule = ".nl img{height:140px;width:auto;position:relative;z-index:1;animation: logoEntrance 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards, logoHeartbeat 3.5s ease-in-out 1.8s infinite; transition: height 0.4s ease;}"
    
    if old_rule in css:
        css = css.replace(old_rule, new_rule)
    else:
        # Fallback if there are spacing differences
        import re
        css = re.sub(r'\.nl img\{height:140px;.*?\}', new_rule, css)

    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)
    print("Logo animation added successfully!")
