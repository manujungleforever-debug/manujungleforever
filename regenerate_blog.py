import os
import re
from bs4 import BeautifulSoup

articles = [
    'amazon-rainforest-tour-to-manu-national-park-from-cusco',
    'climate-change-manu-national-park-peru',
    'everything-you-need-to-know-before-visiting-machu-picchu',
    'five-reasons-to-visit-manu-national-park',
    'how-tourism-helps-the-manu-national-park',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon',
    'off-the-beaten-path-places-to-visit-from-cusco',
    'packing-list-for-your-trip-to-the-peruvian-amazon',
    'peru-travel-tips',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands',
    'ten-days-in-peru',
    'the-sacred-valley-of-the-incas-a-comprehensive-guide',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026',
    'why-visit-the-manu-national-park'
]

def generate_cards():
    html_cards = []
    classes = ['rl', 'r', 'rr']
    for idx, a in enumerate(articles):
        cls = classes[idx % 3]
        path = f"www.hiddenjunglecusco.com/{a}/index.html"
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        title_tag = soup.find('title')
        h1 = soup.find('h1')
        title = h1.text.strip() if h1 and "Hidden Jungle Cusco" not in h1.text else ""
        if not title and title_tag:
            title = title_tag.text.split('–')[0].split('|')[0].strip()
        if not title:
            title = a.replace('-', ' ').title()
        
        # Get excerpt
        p = soup.select_one('.article-content p')
        excerpt = p.text.strip()[:150] + "..." if p else "Read the full guide..."
        
        # Get image
        img = soup.select_one('.article-content img')
        img_src = img['src'] if img else "../wp-content/uploads/2024/06/Cusco-Photo-scaled.jpg"
        
        card = f"""
      <div class="blog-card {cls}">
        <div class="blog-img" style="height:250px; overflow:hidden">
          <img src="{img_src}" alt="{title}" loading="lazy" style="width:100%; height:100%; object-fit:cover;">
        </div>
        <div class="blog-desc">
          <span class="blog-meta">Jungle Guide</span>
          <h3 style="font-size:1.4rem; margin-bottom:12px; line-height:1.4"><a href="../{a}/index.html">{title}</a></h3>
          <p>{excerpt}</p>
          <a href="../{a}/index.html" class="blog-btn">Read Article <i class="fas fa-arrow-right"></i></a>
        </div>
      </div>"""
        html_cards.append(card)
        
    return "\\n".join(html_cards)

def update_blog_page():
    path = "www.hiddenjunglecusco.com/blog/index.html"
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace everything inside <div class="blog-grid">...</div>
    new_html = re.sub(
        r'(<div class="blog-grid">).*?(</div>\s*</div>\s*</section>)',
        r'\1\n' + generate_cards() + r'\n\2',
        html,
        flags=re.DOTALL
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)

update_blog_page()
print("Updated blog page with 14 items.")
