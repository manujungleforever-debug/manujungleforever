import os
import re
import urllib.parse

base_dir = "www.manujungleforever.com"

# Revert to standard <i> tag in HTML
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(('.html', '.php')):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Strip out any previously injected SVG
            content = re.sub(r'<svg.*?</svg>', '<i class="custom-tripadvisor-icon"></i>', content, flags=re.DOTALL)
            
            # If they had fa-brands fa-tripadvisor, replace with custom
            content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', '<i class="custom-tripadvisor-icon"></i>')
            content = content.replace('<i class="fab fa-tripadvisor"></i>', '<i class="custom-tripadvisor-icon"></i>')

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

# The pristine SVG for TripAdvisor (OWL)
svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M380.2 126.9c-2-3-4.7-6-7.8-8.5C316.5 73.1 230 76.8 178.5 120.7c-5.7 4.9-10.7 10.3-14.8 16.3-2.9 4.3-8.8 5.7-13.6 3.1-6-3.2-12.2-5.7-18.6-7.4-12.7-3.4-26.1-4-39.2-1.9-12.4 2-24.1 6.8-34.5 13.9-9.1 6.2-17 14.1-23.2 23.2-7 10.3-11.8 22-13.8 34.4-2 13 1.4 26.2 8.6 37.1 6.9 10.5 16 19.1 26.6 25 10 5.6 21 8.8 32.3 9.4 12.3 .7 24.6-1.5 36.1-6.5 11.2-4.9 21.2-12.3 29.3-21.7l14.1-16.5c3.5 3.3 7 6.4 10.6 9.4 12.7 10.6 27.2 19.3 42.9 25.6 15 6 30.7 9.8 46.7 11.1 14.1 1.2 28.3 1.2 42.4 0 16-1.3 31.7-5.1 46.7-11.1 15.7-6.3 30.2-15 42.9-25.6 3.6-3 7.1-6.1 10.6-9.4l14.1 16.5c8.1 9.4 18.1 16.8 29.3 21.7 11.5 5 23.8 7.2 36.1 6.5 11.3-.6 22.3-3.8 32.3-9.4 10.6-5.9 19.7-14.5 26.6-25 7.2-10.9 10.6-24.1 8.6-37.1-2-12.4-6.8-24.1-13.8-34.4-6.2-9.1-14.1-17-23.2-23.2-10.4-7.1-22.1-11.9-34.5-13.9-13.1-2.1-26.5-1.5-39.2 1.9-6.4 1.7-12.6 4.2-18.6 7.4-4.8 2.6-10.7 1.2-13.6-3.1-4.1-6-9.1-11.4-14.8-16.3-51.5-43.9-138-47.6-193.9-2.3zM140.2 291c-19.2 0-34.8-15.6-34.8-34.8s15.6-34.8 34.8-34.8 34.8 15.6 34.8 34.8-15.6 34.8-34.8 34.8zm231.6 0c-19.2 0-34.8-15.6-34.8-34.8s15.6-34.8 34.8-34.8 34.8 15.6 34.8 34.8-15.6 34.8-34.8 34.8zM256 364.5c-44 0-82.6-23.9-103.7-59.5-3.3-5.5-1.6-12.7 3.9-16 5.5-3.3 12.7-1.6 16 3.9 16.8 28.3 47.6 47.3 83.8 47.3 36.2 0 67-19 83.8-47.3 3.3-5.5 10.5-7.2 16-3.9 5.5 3.3 7.2 10.5 3.9 16-21.1 35.6-59.7 59.5-103.7 59.5z"/></svg>'

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

if '.custom-tripadvisor-icon' not in css:
    css += css_rule
    
# Make sure .sc styles are correct
css = css.replace('.sc{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:.9rem;color:rgba(255,255,255,.45);transition:var(--t)}', '.sc{width:40px;height:40px;border-radius:50%;background:var(--a);border:1px solid var(--a);display:flex;align-items:center;justify-content:center;font-size:1.05rem;color:#ffffff;transition:var(--t)}')
css = css.replace('.sc:hover{background:var(--a);border-color:var(--a);color:var(--k);transform:translateY(-3px)}', '.sc:hover{background:#ffffff;border-color:#ffffff;color:var(--k);transform:translateY(-3px)}')

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css)

# Also update rebuild_tours.py
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'<svg.*?</svg>', '<i class="custom-tripadvisor-icon"></i>', content, flags=re.DOTALL)
    content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', '<i class="custom-tripadvisor-icon"></i>')
    content = content.replace('<i class="fab fa-tripadvisor"></i>', '<i class="custom-tripadvisor-icon"></i>')
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)
