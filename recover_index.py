import os
import re

src_index = "www.hiddenjunglecusco.com/index.php"
dst_index = "www.manujungleforever.com/index.php"
tour_file = "www.manujungleforever.com/5-day-amazon-expedition/index.html"

# 1. Get the perfect header and footer from the tour page
with open(tour_file, "r", encoding="utf-8") as f:
    tour_content = f.read()

# The header in tour pages ends at <main id="main"> but wait, tour pages have <div class="tr-main"> or something.
# Let's extract everything before <main id="main">
header_match = re.search(r'(.*?)<main id="main">', tour_content, flags=re.DOTALL)
if header_match:
    header = header_match.group(1) + '<main id="main">\n'
else:
    print("Could not find <main> in tour file")
    exit(1)

# The footer starts at </main>
footer_match = re.search(r'</main>(.*)', tour_content, flags=re.DOTALL)
if footer_match:
    footer = '\n</main>' + footer_match.group(1)
else:
    print("Could not find </main> in tour file")
    exit(1)
    
# In tour pages, the header has ../assets/. We need to change that to assets/ for index.php!
header = header.replace('href="../assets/', 'href="assets/')
header = header.replace('src="../assets/', 'src="assets/')
header = header.replace('href="../', 'href="')
footer = footer.replace('href="../assets/', 'href="assets/')
footer = footer.replace('src="../assets/', 'src="assets/')
footer = footer.replace('href="../', 'href="')
footer = footer.replace('action="../', 'action="')

# 2. Get the main body from original index.php
with open(src_index, "r", encoding="utf-8") as f:
    orig_content = f.read()

body_match = re.search(r'<main id="main">(.*?)</main>', orig_content, flags=re.DOTALL)
if body_match:
    body = body_match.group(1)
else:
    # Maybe original index.php didn't have <main id="main">? It had <section class="hero">
    body_match = re.search(r'</header>\s*(<section class="hero">.*?)</main>', orig_content, flags=re.DOTALL)
    if body_match:
        body = body_match.group(1)
    else:
        body_match = re.search(r'<a class="skip" href="#main">Skip to content</a>\s*(<header.*?</header>)?\s*(<section class="hero">.*?)<footer', orig_content, flags=re.DOTALL)
        body = body_match.group(2) if body_match else ""
        if not body:
            print("Could not extract body from original index.php")
            exit(1)

# Apply text replacements on the body (since it's from hiddenjunglecusco)
body = body.replace('hiddenjunglecusco', 'manujungleforever')
body = body.replace('Hidden Jungle Cusco', 'Manu Jungle Forever')
body = body.replace('Hidden Jungle', 'Manu Jungle')

# Assemble new index.php
new_index_content = header + body + footer

with open(dst_index, "w", encoding="utf-8") as f:
    f.write(new_index_content)
    
print("index.php reconstructed!")
