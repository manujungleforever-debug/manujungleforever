import os
import re

base_dir = "www.manujungleforever.com"
index_php = os.path.join(base_dir, "index.php")

# 1. Update config.php
config_php = os.path.join(base_dir, "config.php")
if os.path.exists(config_php):
    with open(config_php, "r", encoding="utf-8") as f:
        config = f.read()
    config = re.sub(r"define\('SITE_ADDRESS',\s*'.*?'\);", "define('SITE_ADDRESS', '');", config)
    config = re.sub(r"define\('SITE_PHONE',\s*'.*?'\);", "define('SITE_PHONE', '');", config)
    with open(config_php, "w", encoding="utf-8") as f:
        f.write(config)

# 2. Extract perfect header and footer from index.php
with open(index_php, "r", encoding="utf-8") as f:
    index_content = f.read()

# First, revert TripAdvisor in index.php content in memory
ta_svg = '<svg viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="vertical-align: -0.125em;"><path d="M504.6 156.4c-22.9-19-45.7-36.5-70.1-53.1C354.1 52.8 243.6 47.9 146 112.5 125 126.3 105.7 142.1 86 157.9c-8 6.4-15 8-22.6 1.8-9.8-8-20.1-15.5-30.8-22.3C15 126.1-5.1 143.9 1.1 165c3.2 11 12 18.2 22.3 22.5 10.1 4.2 21 7.1 31.7 10.3 7 2.1 9.4 5.2 8.7 12.3-2 20.3 3.6 39.5 13.9 57.3 15.6 27.2 38.3 47.3 67.1 58.7 18 7.1 36.9 10.3 56.4 10.6 8 .1 15.7 2.4 22.4 6.7 17.6 11.4 23.4 25.1 18 45.4-3.1 11.6-11 20-22.4 24.3-15.2 5.7-31.2 5.6-46.8 .4-14.8-4.9-24.3-14.9-29.2-30.1-1.7-5.3-4.4-8.8-10.2-9.7-5.9-.8-11.4 .9-16.1 4.6-9.1 7.2-18 14.5-27.1 21.6-5.7 4.5-5.9 9.3-3.1 15.6 8.3 18.9 22.4 33.1 41.5 42 22 10.3 45.2 13.5 68.9 9.8 19.3-3 36.9-11 51.5-24.1 24.5-22 34.1-50.7 29.5-83.3-1.6-11.4 3-19.1 12.3-25.2 10.2-6.7 20.9-12.2 32-16.7 28.5-11.6 52.8-30.3 69.4-56.3 10.4-16.3 16.6-34 16.7-53.5 .1-7.1 2.3-11.1 9-13.8 9.3-3.8 18.9-7.1 28.1-11.1 9.6-4.2 16.7-10.6 19.7-21.2 5.1-17.7-11.9-33-28.7-21.7zM189.7 220c-18.7-26.6-48.4-32.9-72.9-15.8-25.6 17.9-32 54.1-13.6 80.3 17.6 25.1 52.4 33.6 78 18.5 24-14.2 31.8-48.5 19-75.1-1.7-3.6-5.1-6.1-8-9.1-1.3-1.4-1.2-4.1 .4-6.3-4.5 1.7-2.3 5.4-2.9 7.5zm196.4 75c24 15.4 56.4 7.2 71.9-18.3 16.4-26.9 7.3-64-20-80.4-26.5-15.9-63-5.2-79.3 22.9-16 27.6-3 62 21 78.5 2.1-1.2 4.1-2.4 6.4-3.7z"/></svg>'
index_content = index_content.replace(ta_svg, '<i class="fa-brands fa-tripadvisor"></i>')

# Remove phone and address from index_content
index_content = index_content.replace('Manu Jungle Forever - La Casa Escondida 17800, Nuevo Eden, Peru', '')
index_content = index_content.replace('+51 979 808 013 / +51 923 289 231', '')
# Ensure PHP echoes are not messed up, they are fine because config.php is empty

header_match = re.search(r'(<header id="N">.*?</header>)', index_content, flags=re.DOTALL)
footer_match = re.search(r'(<footer class="ft">.*?</footer>)', index_content, flags=re.DOTALL)
preloader_match = re.search(r'(<div id="preloader">.*?</script>)', index_content, flags=re.DOTALL)

if not header_match or not footer_match:
    print("Could not extract header/footer from index.php")
    exit(1)

core_header = header_match.group(1)
core_footer = footer_match.group(1)
core_preloader = preloader_match.group(1) if preloader_match else ""

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(('.html', '.php')):
            filepath = os.path.join(root, file)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Revert SVG if present
            content = content.replace(ta_svg, '<i class="fa-brands fa-tripadvisor"></i>')
            
            # 2. Empty hardcoded address and phone
            content = content.replace('Manu Jungle Forever - La Casa Escondida 17800, Nuevo Eden, Peru', '')
            content = content.replace('+51 979 808 013 / +51 923 289 231', '')

            # Calculate relative depth
            rel_dir = os.path.relpath(root, base_dir)
            depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
            prefix = "../" * depth if depth > 0 else ""

            # Prepare the specific header/footer for this depth
            target_header = core_header
            target_footer = core_footer
            target_preloader = core_preloader
            
            if depth > 0:
                target_header = target_header.replace('href="assets/', f'href="{prefix}assets/')
                target_header = target_header.replace('src="assets/', f'src="{prefix}assets/')
                target_header = target_header.replace('href="index.html"', f'href="{prefix}index.html"')
                # Specific top level links
                for link in ['guided-tours', 'about-2', 'departures', 'news-and-gallery', 'blog', 'contact']:
                    target_header = target_header.replace(f'href="{link}/index.html"', f'href="{prefix}{link}/index.html"')
                    target_footer = target_footer.replace(f'href="{link}/index.html"', f'href="{prefix}{link}/index.html"')
                
                # Tours dropdown links
                target_header = re.sub(r'href="([a-z0-9\-]+)/index\.html"', rf'href="{prefix}\1/index.html"', target_header)
                target_footer = re.sub(r'href="([a-z0-9\-]+)/index\.html"', rf'href="{prefix}\1/index.html"', target_footer)

                target_footer = target_footer.replace('href="assets/', f'href="{prefix}assets/')
                target_footer = target_footer.replace('src="assets/', f'src="{prefix}assets/')
                target_footer = target_footer.replace('href="index.html"', f'href="{prefix}index.html"')
                
                target_preloader = target_preloader.replace('src="assets/', f'src="{prefix}assets/')

            # Replace header
            content = re.sub(r'<header id="N">.*?</header>', target_header, content, flags=re.DOTALL)
            # Replace footer
            content = re.sub(r'<footer class="ft">.*?</footer>', target_footer, content, flags=re.DOTALL)
            
            # Add preloader if missing (and not in root since root already has it usually)
            if 'id="preloader"' not in content and target_preloader:
                content = content.replace('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Skip to content</a>\n' + target_preloader)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

print("Applied changes globally!")
