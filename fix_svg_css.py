import os
import re

base_dir = "www.manujungleforever.com"

# The pristine SVG for TripAdvisor (Correct path)
ta_svg = '<svg viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="vertical-align: -0.125em;"><path d="M380.2 126.9c-2-3-4.7-6-7.8-8.5C316.5 73.1 230 76.8 178.5 120.7c-5.7 4.9-10.7 10.3-14.8 16.3-2.9 4.3-8.8 5.7-13.6 3.1-6-3.2-12.2-5.7-18.6-7.4-12.7-3.4-26.1-4-39.2-1.9-12.4 2-24.1 6.8-34.5 13.9-9.1 6.2-17 14.1-23.2 23.2-7 10.3-11.8 22-13.8 34.4-2 13 1.4 26.2 8.6 37.1 6.9 10.5 16 19.1 26.6 25 10 5.6 21 8.8 32.3 9.4 12.3 .7 24.6-1.5 36.1-6.5 11.2-4.9 21.2-12.3 29.3-21.7l14.1-16.5c3.5 3.3 7 6.4 10.6 9.4 12.7 10.6 27.2 19.3 42.9 25.6 15 6 30.7 9.8 46.7 11.1 14.1 1.2 28.3 1.2 42.4 0 16-1.3 31.7-5.1 46.7-11.1 15.7-6.3 30.2-15 42.9-25.6 3.6-3 7.1-6.1 10.6-9.4l14.1 16.5c8.1 9.4 18.1 16.8 29.3 21.7 11.5 5 23.8 7.2 36.1 6.5 11.3-.6 22.3-3.8 32.3-9.4 10.6-5.9 19.7-14.5 26.6-25 7.2-10.9 10.6-24.1 8.6-37.1-2-12.4-6.8-24.1-13.8-34.4-6.2-9.1-14.1-17-23.2-23.2-10.4-7.1-22.1-11.9-34.5-13.9-13.1-2.1-26.5-1.5-39.2 1.9-6.4 1.7-12.6 4.2-18.6 7.4-4.8 2.6-10.7 1.2-13.6-3.1-4.1-6-9.1-11.4-14.8-16.3-51.5-43.9-138-47.6-193.9-2.3zM140.2 291c-19.2 0-34.8-15.6-34.8-34.8s15.6-34.8 34.8-34.8 34.8 15.6 34.8 34.8-15.6 34.8-34.8 34.8zm231.6 0c-19.2 0-34.8-15.6-34.8-34.8s15.6-34.8 34.8-34.8 34.8 15.6 34.8 34.8-15.6 34.8-34.8 34.8zM256 364.5c-44 0-82.6-23.9-103.7-59.5-3.3-5.5-1.6-12.7 3.9-16 5.5-3.3 12.7-1.6 16 3.9 16.8 28.3 47.6 47.3 83.8 47.3 36.2 0 67-19 83.8-47.3 3.3-5.5 10.5-7.2 16-3.9 5.5 3.3 7.2 10.5 3.9 16-21.1 35.6-59.7 59.5-103.7 59.5z"/></svg>'

wrong_svg = '<svg viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="vertical-align: -0.125em;"><path d="M504.6 156.4c-22.9-19-45.7-36.5-70.1-53.1C354.1 52.8 243.6 47.9 146 112.5 125 126.3 105.7 142.1 86 157.9c-8 6.4-15 8-22.6 1.8-9.8-8-20.1-15.5-30.8-22.3C15 126.1-5.1 143.9 1.1 165c3.2 11 12 18.2 22.3 22.5 10.1 4.2 21 7.1 31.7 10.3 7 2.1 9.4 5.2 8.7 12.3-2 20.3 3.6 39.5 13.9 57.3 15.6 27.2 38.3 47.3 67.1 58.7 18 7.1 36.9 10.3 56.4 10.6 8 .1 15.7 2.4 22.4 6.7 17.6 11.4 23.4 25.1 18 45.4-3.1 11.6-11 20-22.4 24.3-15.2 5.7-31.2 5.6-46.8 .4-14.8-4.9-24.3-14.9-29.2-30.1-1.7-5.3-4.4-8.8-10.2-9.7-5.9-.8-11.4 .9-16.1 4.6-9.1 7.2-18 14.5-27.1 21.6-5.7 4.5-5.9 9.3-3.1 15.6 8.3 18.9 22.4 33.1 41.5 42 22 10.3 45.2 13.5 68.9 9.8 19.3-3 36.9-11 51.5-24.1 24.5-22 34.1-50.7 29.5-83.3-1.6-11.4 3-19.1 12.3-25.2 10.2-6.7 20.9-12.2 32-16.7 28.5-11.6 52.8-30.3 69.4-56.3 10.4-16.3 16.6-34 16.7-53.5 .1-7.1 2.3-11.1 9-13.8 9.3-3.8 18.9-7.1 28.1-11.1 9.6-4.2 16.7-10.6 19.7-21.2 5.1-17.7-11.9-33-28.7-21.7zM189.7 220c-18.7-26.6-48.4-32.9-72.9-15.8-25.6 17.9-32 54.1-13.6 80.3 17.6 25.1 52.4 33.6 78 18.5 24-14.2 31.8-48.5 19-75.1-1.7-3.6-5.1-6.1-8-9.1-1.3-1.4-1.2-4.1 .4-6.3-4.5 1.7-2.3 5.4-2.9 7.5zm196.4 75c24 15.4 56.4 7.2 71.9-18.3 16.4-26.9 7.3-64-20-80.4-26.5-15.9-63-5.2-79.3 22.9-16 27.6-3 62 21 78.5 2.1-1.2 4.1-2.4 6.4-3.7z"/></svg>'

count = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(('.html', '.php')):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if wrong_svg in content:
                content = content.replace(wrong_svg, ta_svg)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
            elif '<i class="fab fa-tripadvisor"></i>' in content:
                content = content.replace('<i class="fab fa-tripadvisor"></i>', ta_svg)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
            elif '<i class="fa-brands fa-tripadvisor"></i>' in content:
                content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', ta_svg)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1

print(f"Replaced wrong TripAdvisor SVG with the true OWL in {count} files globally.")

# Update rebuild_tours.py too
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    with open(rebuild_script, "r", encoding="utf-8") as f:
        content = f.read()
    if wrong_svg in content:
        content = content.replace(wrong_svg, ta_svg)
    if '<i class="fab fa-tripadvisor"></i>' in content:
        content = content.replace('<i class="fab fa-tripadvisor"></i>', ta_svg)
    if '<i class="fa-brands fa-tripadvisor"></i>' in content:
        content = content.replace('<i class="fa-brands fa-tripadvisor"></i>', ta_svg)
    with open(rebuild_script, "w", encoding="utf-8") as f:
        f.write(content)

css_file = os.path.join(base_dir, "assets", "css", "new.css")
with open(css_file, "r", encoding="utf-8") as f:
    css = f.read()
css = css.replace('.sc{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:.9rem;color:rgba(255,255,255,.45);transition:var(--t)}', '.sc{width:40px;height:40px;border-radius:50%;background:var(--a);border:1px solid var(--a);display:flex;align-items:center;justify-content:center;font-size:1.05rem;color:#ffffff;transition:var(--t)}')
css = css.replace('.sc:hover{background:var(--a);border-color:var(--a);color:var(--k);transform:translateY(-3px)}', '.sc:hover{background:#ffffff;border-color:#ffffff;color:var(--k);transform:translateY(-3px)}')
with open(css_file, "w", encoding="utf-8") as f:
    f.write(css)

