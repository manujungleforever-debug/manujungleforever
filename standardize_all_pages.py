import os
import re
import shutil

base_dir = "www.manujungleforever.com"
index_php_path = os.path.join(base_dir, "index.php")
root_index_html = os.path.join(base_dir, "index.html")

# 1. Extract Master Header and Footer from index.php
with open(index_php_path, "r", encoding="utf-8") as f:
    master_content = f.read()

match = re.search(r'(.*?)<main id="main">(.*?)</main>(.*)', master_content, flags=re.DOTALL)
if not match:
    print("Could not parse index.php")
    exit(1)

master_header = match.group(1) + '<main id="main">'
master_footer = '</main>' + match.group(3)

# Add Preloader into the master header if it's missing (wait, it's already in index.php? Let's check. Wait, add_preloader.py put it in index.php)
# Let's verify if preloader is in master_header
preloader_html = """
<div id="preloader">
  <img src="assets/img/logo.png" alt="Loading Manu Jungle Forever">
</div>
<script>
  var _preloaderStart = Date.now();
  window.addEventListener('load', function() {
    var elapsed = Date.now() - _preloaderStart;
    var minDuration = 3000; 
    var delay = Math.max(500, minDuration - elapsed);
    setTimeout(function() {
      var preloader = document.getElementById('preloader');
      if (preloader) {
        preloader.classList.add('loaded');
        setTimeout(function() { preloader.style.display = 'none'; }, 700);
      }
    }, delay);
  });
</script>
"""
if 'id="preloader"' not in master_header:
    master_header = master_header.replace(
        '<a class="skip" href="#main">Skip to content</a>', 
        '<a class="skip" href="#main">Skip to content</a>\n' + preloader_html
    )

# 2. PHP Variable Replacements Dictionary
php_replacements = {
    r'<\?php echo htmlspecialchars\(SITE_NAME\);\s*\?>': 'Manu Jungle Forever',
    r'<\?php echo htmlspecialchars\(SITE_URL\);\s*\?>': 'https://www.manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_EMAIL\);\s*\?>': 'discover@manujungleforever.com',
    r'<\?php echo htmlspecialchars\(SITE_PHONE\);\s*\?>': '', 
    r'<\?php echo htmlspecialchars\(SITE_ADDRESS\);\s*\?>': '',
    r'<\?php echo htmlspecialchars\(WHATSAPP_NUMBER\);\s*\?>': '51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_FACEBOOK\);\s*\?>': 'https://www.facebook.com/manujungleforever',
    r'<\?php echo htmlspecialchars\(SOCIAL_INSTAGRAM\);\s*\?>': 'https://www.instagram.com/manujungleforever/?hl=en',
    r'<\?php echo htmlspecialchars\(SOCIAL_TRIPADVISOR\);\s*\?>': 'https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905',
    r'<\?php echo htmlspecialchars\(SOCIAL_AIRBNB\);\s*\?>': 'https://abnb.me/Ri8XQWoA19',
    r'<\?php echo htmlspecialchars\(SOCIAL_WHATSAPP\);\s*\?>': 'https://wa.me/51923289231',
    r'<\?php echo htmlspecialchars\(SOCIAL_TIKTOK\);\s*\?>': 'https://www.tiktok.com/@hidden.jungle.cus',
    r'<\?php echo htmlspecialchars\(GTM_ID\);\s*\?>': 'GTM-5476BC9',
    r'<\?php echo htmlspecialchars\(GA_ID\);\s*\?>': 'GT-NS9ZNKJP',
    r'<\?php echo htmlspecialchars\(GOOGLE_MAP\);\s*\?>': 'https://www.google.com/maps/d/embed?mid=1CkYt9KUrq9Jjp9tgxChYmOYvyNaLZnxF',
    r'<\?php echo date\(\'Y\'\);\s*\?>': '2026'
}

def strip_php(html_str):
    for pattern, replacement in php_replacements.items():
        html_str = re.sub(pattern, replacement, html_str)
    return html_str

def adapt_paths(html_str, rel_prefix):
    if not rel_prefix:
        return html_str
    # Fix asset paths
    html_str = html_str.replace('href="assets/', f'href="{rel_prefix}assets/')
    html_str = html_str.replace('src="assets/', f'src="{rel_prefix}assets/')
    # Fix common root links
    html_str = html_str.replace('href="index.html"', f'href="{rel_prefix}index.html"')
    html_str = html_str.replace('href="about-2/index.html"', f'href="{rel_prefix}about-2/index.html"')
    html_str = html_str.replace('href="contact/index.html"', f'href="{rel_prefix}contact/index.html"')
    html_str = html_str.replace('href="guided-tours/index.html"', f'href="{rel_prefix}guided-tours/index.html"')
    html_str = html_str.replace('href="departures/index.html"', f'href="{rel_prefix}departures/index.html"')
    html_str = html_str.replace('href="blog/index.html"', f'href="{rel_prefix}blog/index.html"')
    html_str = html_str.replace('href="news-and-gallery/index.html"', f'href="{rel_prefix}news-and-gallery/index.html"')
    
    # Fix all root-level directory links
    root_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d not in ("assets", "admin", "data", "handlers", "partials")]
    for t in root_dirs:
        html_str = html_str.replace(f'href="{t}/index.html"', f'href="{rel_prefix}{t}/index.html"')
    return html_str

# 3. Walk all HTML files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            # Calculate depth relative to base_dir
            rel_dir = os.path.relpath(root, base_dir)
            if rel_dir == '.':
                rel_prefix = ''
            else:
                depth = len(rel_dir.split(os.sep))
                rel_prefix = '../' * depth
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if rel_prefix == '': # Root level
                if file == 'index.html':
                    # Fully overwrite index.html with stripped index.php
                    new_content = strip_php(master_content)
                    # Also ensure preloader is in root index.html
                    if 'id="preloader"' not in new_content:
                        new_content = new_content.replace('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Skip to content</a>\n' + preloader_html)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Synced root {file_path}")
                    continue
            
            # For nested pages, extract their unique main block
            m = re.search(r'<main id="main">(.*?)</main>', content, flags=re.DOTALL)
            if not m:
                # If they don't have <main id="main">, maybe they have <div class="main"> or something?
                # Actually hiddenjunglecusco uses elementor, but we migrated some.
                # If we can't find it, just skip or print a warning
                print(f"Warning: Could not find <main id=\"main\"> in {file_path}")
                continue
                
            unique_main = m.group(1)
            
            # Adapt header and footer paths
            local_header = adapt_paths(master_header, rel_prefix)
            local_footer = adapt_paths(master_footer, rel_prefix)
            
            # Combine
            full_html = local_header + unique_main + local_footer
            
            # Strip PHP
            full_html = strip_php(full_html)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_html)
            print(f"Standardized {file_path}")

print("All pages standardized successfully.")
