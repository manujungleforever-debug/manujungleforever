import os
import re

css_file = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\assets\css\new.css"

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()

    # Add responsive sizing for the logo inside the 768px media query
    # Find @media(max-width:768px){...}
    
    if '@media(max-width:768px){' in css:
        css = css.replace(
            '@media(max-width:768px){',
            '@media(max-width:768px){.nl img{height:90px;}#N.s .nl img{height:60px;}'
        )
        
    # Add responsive sizing for the logo inside the 480px media query
    if '@media(max-width:480px){' in css:
        css = css.replace(
            '@media(max-width:480px){',
            '@media(max-width:480px){.nl img{height:70px;}#N.s .nl img{height:50px;}'
        )

    # Let's ensure the hero section text sizes are perfectly responsive too
    # They already have some rules, but let's double check.
    # .h1{font-size:2.6rem;} is in 480px. That's good.
    
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css)
    print("Responsive CSS for logo updated!")
