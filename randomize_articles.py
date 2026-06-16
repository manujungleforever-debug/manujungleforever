import os
import re
import json

base_dir = 'www.hiddenjunglecusco.com'

blog_folders = [
    'discovering-the-mysteries-of-the-peruvian-amazon',
    'amazon-rainforest-tour-to-manu-national-park-from-cusco',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026',
    'climate-change-manu-national-park-peru',
    'how-tourism-helps-the-manu-national-park',
    'everything-you-need-to-know-before-visiting-machu-picchu',
    'peru-travel-tips',
    'packing-list-for-your-trip-to-the-peruvian-amazon',
    'five-reasons-to-visit-manu-national-park',
    'ten-days-in-peru'
]

def extract_articles_from_blog_index(lang_prefix):
    articles = []
    
    paths = [
        os.path.join(base_dir, lang_prefix, 'blog/index.html'),
        os.path.join(base_dir, lang_prefix, 'blog/page/2/index.html')
    ]
    
    for p in paths:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cards = re.findall(r'<a href="([^"]+)" class="blog-card [^"]*"[^>]*>.*?<img src="([^"]+)"[^>]*>.*?<h2>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
            
            for url, img, title in cards:
                if not url.startswith('../'):
                    if url.startswith('./'):
                        url = '.' + url
                    else:
                        url = '../' + url
                        
                if img.startswith('../../'):
                    img = img[3:]
                elif img.startswith('../'):
                    pass
                else:
                    img = '../' + img
                
                articles.append({'url': url, 'title': title.strip(), 'img': img})
                
    return articles

en_articles = extract_articles_from_blog_index('')
es_articles = extract_articles_from_blog_index('es')

# Because es/blog doesn't exist? Wait, earlier script output: "Extracted 12 EN articles and 0 ES articles"
# There is no es/blog/index.html. We will just use EN articles for ES too if it's missing, or fallback to the manual list
if len(es_articles) == 0:
    es_articles = en_articles # fallback

print(f"Extracted {len(en_articles)} EN articles and {len(es_articles)} ES articles from blog pages.")

def update_files(lang_prefix, articles_list):
    if not articles_list:
        return
        
    new_section = f"""
  <!-- RELATED POSTS -->
  <section style="background:var(--f); border-top:1px solid rgba(255,255,255,.05)">
    <div class="related-posts">
      <h2 class="comments-title"><i class="fas fa-newspaper" style="color:var(--a)"></i> More Articles</h2>
      <div class="related-grid" id="related-grid"></div>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    const articles = {json.dumps(articles_list)};
    const current = window.location.pathname;
    const valid = articles.filter(a => !current.includes(a.url.replace('../', '')));
    valid.sort(() => 0.5 - Math.random());
    const grid = document.querySelector('.related-grid');
    if(grid) {{
        grid.innerHTML = valid.slice(0, 3).map(a => `<a href="${{a.url}}" class="related-card"><img src="${{a.img}}" alt="${{a.title}}" loading="lazy"><div class="related-card-body"><h3>${{a.title}}</h3></div></a>`).join('');
    }}
}});
</script>
    </div>
  </section>
</main>"""

    updated = 0
    for bf in blog_folders:
        path = os.path.join(base_dir, lang_prefix, bf, 'index.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(r'<!-- RELATED POSTS -->\s*<section.*?</section>\s*</main>', lambda m: new_section, content, flags=re.DOTALL)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
                
    print(f"Updated {updated} files in '{lang_prefix}'")

update_files('', en_articles)
update_files('es', es_articles)
