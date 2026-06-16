import re

path = 'www.hiddenjunglecusco.com/packing-list-for-your-trip-to-the-peruvian-amazon/index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the image paths
content = content.replace('..../wp-content', '../wp-content')

# 2. Extract the actual article text
# Since we already ran the script once, the first <div class="tour-rich-text"> has our clean text.
article_text_match = re.search(r'(<div class="tour-rich-text">.*?</div>)', content, re.DOTALL)
if article_text_match:
    article_text = article_text_match.group(1)
else:
    print("Article text not found")
    exit(1)

new_inner_html = f"""<div class="article-w" style="max-width:900px; margin:0 auto;"><h1 class="h2" style="font-size:2.5rem; margin-bottom: 24px; color:var(--w);">PACKING LIST FOR YOUR TRIP TO THE PERUVIAN JUNGLE</h1>
{article_text}

    <!-- Prev / Next -->
    <nav class="article-nav" aria-label="Article navigation"><a href="../peru-travel-tips/index.html" style="text-align:left"><div class="nav-label"><i class="fas fa-arrow-left"></i> Previous</div><div class="nav-title">PERU TRAVEL TIPS</div></a><a href="../five-reasons-to-visit-manu-national-park/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">FIVE REASONS TO VISIT MANU NATIONAL PARK</div></a></nav>

    <!-- CTA -->
    <div style="margin:64px 0 80px; padding:48px 40px; background:var(--f); border-radius:20px; border:1px solid rgba(255,255,255,.06); text-align:center">
      <span class="ey">Ready to go?</span>
      <h2 class="h2" style="font-size:1.7rem; max-width:500px; margin:0 auto 16px">Plan Your Manu Adventure</h2>
      <p style="color:rgba(255,255,255,.5); margin-bottom:28px; max-width:460px; margin-left:auto; margin-right:auto">Guided tours from Cusco deep into the Peruvian Amazon. Local. Wild. Authentic.</p>
      <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">
        <a href="../guided-tours/index.html" class="btn ba"><i class="fas fa-binoculars"></i> See All Tours</a>
        <a href="../contact/index.html" class="btn bg2"><i class="fas fa-envelope"></i> Contact Us</a>
      </div>
    </div>
</div>
"""

# Replace everything from <div class="article-w" down to the end of <main>
content = re.sub(r'<div class="article-w"[^>]*>.*?</main>', new_inner_html + '\n  </div>\n</section>\n</main>', content, flags=re.DOTALL)

# Fix the nav class
content = content.replace('<a class="on" href="../guided-tours/index.html">', '<a href="../guided-tours/index.html">')
content = content.replace('<a href="../blog/index.html">Blog</a> <a href="../contact/index.html" class="nb">', '<a class="on" href="../blog/index.html">Blog</a> <a href="../contact/index.html" class="nb">')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed packing list!")
