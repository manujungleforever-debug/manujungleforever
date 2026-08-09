import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

with open(base_dir + r"\index.html", 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract full footer from index.html
footer_match = re.search(r'(<footer class="ft">.*?</footer>)', index_html, re.DOTALL)
if footer_match:
    full_footer = footer_match.group(1)
    
    # Let's adjust paths if necessary. In index.html, paths are like `assets/img/logo.png`.
    # But book-now is one level deep, so it needs `../assets/...`
    # Let's see if index.html uses `assets/` or `../assets/`.
    # Wait, `index.html` is in the root, so it uses `assets/`.
    # I'll replace `assets/` with `../assets/` for book-now.
    full_footer = full_footer.replace('assets/', '../assets/')
    full_footer = full_footer.replace('href="about-2/', 'href="../about-2/')
    full_footer = full_footer.replace('href="contact/', 'href="../contact/')
    full_footer = full_footer.replace('href="guided-tours/', 'href="../guided-tours/')
    full_footer = full_footer.replace('href="departures/', 'href="../departures/')
    full_footer = full_footer.replace('href="news-and-gallery/', 'href="../news-and-gallery/')
    full_footer = full_footer.replace('href="blog/', 'href="../blog/')
    # fix links that might point to index.html
    full_footer = full_footer.replace('href="index.html"', 'href="../index.html"')
    # fix other tour links
    # Actually, the footer is mostly links. A simpler way is to just grab the footer from another page like contact/index.html!
else:
    print("Could not find footer in index.html")

# Let's grab it from contact/index.html which is already 1 level deep and has correct paths.
with open(base_dir + r"\contact\index.html", 'r', encoding='utf-8') as f:
    contact_html = f.read()

footer_match = re.search(r'(<footer class="ft">.*?</footer>)', contact_html, re.DOTALL)
if footer_match:
    full_footer = footer_match.group(1)
    
    with open(base_dir + r"\book-now\index.html", 'r', encoding='utf-8') as f:
        book_now_html = f.read()
    
    # replace the broken footer in book-now
    book_now_html = re.sub(r'<footer class="ft">.*?</footer>', full_footer, book_now_html, flags=re.DOTALL)
    
    with open(base_dir + r"\book-now\index.html", 'w', encoding='utf-8') as f:
        f.write(book_now_html)
    print("Fixed footer in book-now/index.html")
else:
    print("Could not find footer in contact/index.html")
