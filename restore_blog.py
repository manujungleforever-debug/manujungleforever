import os
import re

template = open('www.hiddenjunglecusco.com/index.html', 'r', encoding='utf-8').read()

# Make blog
blog_html = re.sub(r'<main id="main">.*?</main>', '''<main id="main">
<section class="in-hero">
  <div class="cx">
    <span class="ey">Guides &amp; Insights</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">Jungle Blog</h1>
    <p class="hs" style="margin:0 auto">Read expert tips, wildlife checklists, and packing advice curated directly by our local family guides.</p>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="blog-grid">
    </div>
  </div>
</section>
</main>''', template, flags=re.DOTALL)

# Fix paths for blog since it's 1 level deep
blog_html = blog_html.replace('href="', 'href="../').replace('src="', 'src="../')
# Fix the absolute paths that might have gotten double ../
blog_html = blog_html.replace('href="../http', 'href="http')
blog_html = blog_html.replace('src="../http', 'src="http')
# Fix the nav link
blog_html = blog_html.replace('href="../blog/index.html"', 'href="index.html" class="on"')

open('www.hiddenjunglecusco.com/blog/index.html', 'w', encoding='utf-8').write(blog_html)

print("Blog restored!")
