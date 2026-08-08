import os
import re
import urllib.parse

base_dir = "www.manujungleforever.com"

# The pristine SVG for TripAdvisor (ACTUAL OWL)
svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M528.91,178.82,576,127.58H471.66a326.11,326.11,0,0,0-367,0H0l47.09,51.24A143.911,143.911,0,0,0,241.86,390.73L288,440.93l46.11-50.17A143.94,143.94,0,0,0,575.88,285.18h-.03A143.56,143.56,0,0,0,528.91,178.82ZM144.06,382.57a97.39,97.39,0,1,1,97.39-97.39A97.39,97.39,0,0,1,144.06,382.57ZM288,282.37c0-64.09-46.62-119.08-108.09-142.59a281,281,0,0,1,216.17,0C334.61,163.3,288,218.29,288,282.37Zm143.88,100.2h-.01a97.405,97.405,0,1,1,.01,0ZM144.06,234.12h-.01a51.06,51.06,0,1,0,51.06,51.06v-.11A51,51,0,0,0,144.06,234.12Zm287.82,0a51.06,51.06,0,1,0,51.06,51.06A51.06,51.06,0,0,0,431.88,234.12Z"/></svg>'

# URL encode for CSS
encoded_svg = urllib.parse.quote(svg_content)
css_rule = f'''
.custom-tripadvisor-icon {{
    display: inline-block;
    width: 1em;
    height: 1em;
    background-color: currentColor;
    -webkit-mask: url('data:image/svg+xml;utf8,{encoded_svg}') no-repeat center / contain;
    mask: url('data:image/svg+xml;utf8,{encoded_svg}') no-repeat center / contain;
}}
'''

css_file = os.path.join(base_dir, "assets", "css", "new.css")
with open(css_file, "r", encoding="utf-8") as f:
    css = f.read()

# Replace the old bad rule
css = re.sub(r'\.custom-tripadvisor-icon\s*\{[^}]*\}', css_rule, css)
if '.custom-tripadvisor-icon' not in css:
    css += css_rule

# Fix font-size so it matches the other icons nicely
# FontAwesome brands usually are 1em height but width can be larger. The viewbox is 576x512.
# So it's slightly wider. width: 1.125em; height: 1em;
css = css.replace('width: 1em;\n    height: 1em;', 'width: 1.125em;\n    height: 1em;')

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css)

