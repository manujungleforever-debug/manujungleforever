import os
import re

css_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css"

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    # Make the default logo HUGE
    css = re.sub(r'\.nl img\{height:\d+px;', '.nl img{height:140px;', css)
    
    # Add a CSS rule so the logo shrinks when the user scrolls down
    # We will append it right after the .nl img hover rule
    if '#N.s .nl img' not in css:
        css = css.replace('.nl:hover img{transform:scale(1.03);}', '.nl:hover img{transform:scale(1.03);}\n#N.s .nl img{height:65px;}')

    # Ensure transition is applied to height as well
    css = css.replace('.nl img{height:140px;width:auto;position:relative;z-index:1;transition:all 0.3s ease;}', '.nl img{height:140px;width:auto;position:relative;z-index:1;transition:height 0.4s ease, transform 0.3s ease;}')

    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)
    print("CSS successfully updated for massive logo with scroll shrink!")
