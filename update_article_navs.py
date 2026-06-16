import re

def update_file(path, old_nav, new_nav):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace(old_nav, new_nav)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

# 1. Update the NEW article (Discovering...)
new_article_path = r'www.hiddenjunglecusco.com/discovering-the-mysteries-of-the-peruvian-amazon/index.html'

with open(new_article_path, 'r', encoding='utf-8') as f:
    new_html = f.read()

bad_nav_new = '<nav class="article-nav" aria-label="Article navigation"><a href="../sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">Sustainable Tourism In The Manu Biosphere Reserve </div></a></nav>'

good_nav_new = '<nav class="article-nav" aria-label="Article navigation"><a href="../amazon-rainforest-tour-to-manu-national-park-from-cusco/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">Amazon Rainforest Tour to Manu National Park from Cusco</div></a></nav>'

new_html = new_html.replace(bad_nav_new, good_nav_new)
with open(new_article_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

# 2. Update the OLD first article (Amazon Rainforest Tour...)
old_article_path = r'www.hiddenjunglecusco.com/amazon-rainforest-tour-to-manu-national-park-from-cusco/index.html'

with open(old_article_path, 'r', encoding='utf-8') as f:
    old_html = f.read()

bad_nav_old = '<nav class="article-nav" aria-label="Article navigation"><a href="../sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">Sustainable Tourism In The Manu Biosphere Reserve </div></a></nav>'

good_nav_old = '<nav class="article-nav" aria-label="Article navigation"><a href="../discovering-the-mysteries-of-the-peruvian-amazon/index.html" style="text-align:left"><div class="nav-label"><i class="fas fa-arrow-left"></i> Previous</div><div class="nav-title">Discovering the Mysteries of the Peruvian Amazon</div></a><a href="../sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">Sustainable Tourism In The Manu Biosphere Reserve </div></a></nav>'

old_html = old_html.replace(bad_nav_old, good_nav_old)
with open(old_article_path, 'w', encoding='utf-8') as f:
    f.write(old_html)

print("Navigation updated for both articles!")
