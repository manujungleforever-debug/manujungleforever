"""
clone_blog.py  –  Clona TODAS las páginas del blog del sitio en vivo
https://www.hiddenjunglecusco.com

Uso: python clone_blog.py
"""
import urllib.request, sys, re, os, math
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

BASE_URL = 'https://www.hiddenjunglecusco.com'
REL      = '../'   # relativo desde /blog/
OUT_FILE = 'www.hiddenjunglecusco.com/blog/index.html'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

# ─── URLs de paginación del blog ──────────────────────────────────────────────
BLOG_PAGES = [
    'https://www.hiddenjunglecusco.com/blog/',
    'https://www.hiddenjunglecusco.com/blog/2/',     # página 2
]

CATS = {
    'amazon-rainforest-tour-to-manu-national-park-from-cusco':                                              ('Wildlife',      'fa-binoculars'),
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands':   ('Sustainability','fa-globe-americas'),
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon':                           ('Manu Park',     'fa-map-marked-alt'),
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026':                               ('Wildlife',      'fa-binoculars'),
    'climate-change-manu-national-park-peru':                                                              ('Conservation',  'fa-leaf'),
    'how-tourism-helps-the-manu-national-park':                                                            ('Sustainability','fa-globe-americas'),
    'everything-you-need-to-know-before-visiting-machu-picchu':                                            ('Travel Tips',   'fa-mountain'),
    'peru-travel-tips':                                                                                    ('Travel Tips',   'fa-map-marked-alt'),
    'packing-list-for-your-trip-to-the-peruvian-amazon':                                                   ('Travel Tips',   'fa-suitcase-rolling'),
    'ten-days-in-peru':                                                                                    ('Itinerary',     'fa-calendar-alt'),
    'the-sacred-valley-of-the-incas-a-comprehensive-guide':                                                ('Cusco Region',  'fa-landmark'),
    'off-the-beaten-path-places-to-visit-from-cusco':                                                      ('Hidden Gems',   'fa-compass'),
    'five-reasons-to-visit-manu-national-park':                                                            ('Manu Park',     'fa-map-marked-alt'),
    'why-visit-the-manu-national-park':                                                                    ('Wildlife',      'fa-binoculars'),
}

# ─── 1. Descargar y extraer artículos de todas las páginas ────────────────────
seen  = set()
posts = []

for page_url in BLOG_PAGES:
    print(f'Descargando {page_url} ...')
    req = urllib.request.Request(page_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read()
    except Exception as e:
        print(f'  ERROR: {e}')
        continue
    print(f'  {len(raw):,} bytes recibidos')

    soup = BeautifulSoup(raw, 'html.parser')
    articles = soup.find_all('article', class_='elementor-post')

    page_posts = 0
    for art in articles:
        title_el = art.select_one('.elementor-post__title a')
        if not title_el:
            continue
        href = title_el.get('href', '').rstrip('/')
        if href in seen:
            continue
        seen.add(href)

        img_el  = art.select_one('.elementor-post__thumbnail img')
        exc_el  = art.select_one('.elementor-post__excerpt p')
        date_el = art.select_one('.elementor-post-date')

        title     = title_el.text.strip()
        img_src   = img_el.get('src', '') if img_el else ''
        img_root  = img_src.replace(BASE_URL + '/', '').replace(BASE_URL, '')
        excerpt   = exc_el.text.strip() if exc_el else ''
        date      = date_el.text.strip() if date_el else ''
        slug      = href.split('/')[-1]

        posts.append({
            'title':     title,
            'slug':      slug,
            'img_root':  img_root,
            'img_abs':   img_src,
            'excerpt':   excerpt,
            'date':      date,
        })
        page_posts += 1
        print(f'    [{len(posts)}] {title}')

    print(f'  → {page_posts} artículos nuevos en esta página')

print(f'\nTotal combinado: {len(posts)} artículos únicos\n')

# ─── 2. Generar tarjetas HTML ─────────────────────────────────────────────────
def make_card(p, rel):
    cat_label, cat_icon = CATS.get(p['slug'], ('Travel', 'fa-compass'))
    excerpt = p['excerpt']
    if excerpt.lower().startswith(p['title'].lower()):
        excerpt = excerpt[len(p['title']):].lstrip(' :-–—').strip()
    if len(excerpt) > 140:
        excerpt = excerpt[:137].rstrip() + '...'

    return f'''      <a href="{rel}{p["slug"]}/index.html" class="blog-card r" style="text-decoration:none" aria-label="{p["title"]}">
        <div class="blog-thumb">
          <img src="{rel}{p["img_root"]}" alt="{p["title"]}" loading="lazy">
          <span class="blog-cat"><i class="fas {cat_icon}"></i> {cat_label}</span>
        </div>
        <div class="blog-body">
          <p class="blog-date"><i class="far fa-calendar-alt"></i> {p["date"]}</p>
          <h2>{p["title"]}</h2>
          <p>{excerpt if excerpt else "Read the full article →"}</p>
          <span class="blog-read"><i class="fas fa-arrow-right"></i> Read Article</span>
        </div>
      </a>'''

POSTS_PER_PAGE = 9
total_pages = math.ceil(len(posts) / POSTS_PER_PAGE) if posts else 1

for page_num in range(1, total_pages + 1):
    start_idx = (page_num - 1) * POSTS_PER_PAGE
    end_idx = start_idx + POSTS_PER_PAGE
    page_posts = posts[start_idx:end_idx]
    
    if page_num == 1:
        OUT_FILE = 'www.hiddenjunglecusco.com/blog/index.html'
        REL = '../'
    else:
        OUT_FILE = f'www.hiddenjunglecusco.com/blog/page/{page_num}/index.html'
        REL = '../../../'

    cards_html = '\n'.join(make_card(p, REL) for p in page_posts)
    
    # ─── Paginación HTML ────────────────────────────────────────────────────────
    pag_html = ''
    if total_pages > 1:
        pag_html += '<div class="pagination" style="margin-top:56px; display:flex; justify-content:center; gap:12px; align-items:center;">'
        if page_num > 1:
            prev_link = f'{REL}blog/index.html' if page_num == 2 else f'{REL}blog/page/{page_num-1}/index.html'
            pag_html += f'<a href="{prev_link}" class="btn ba" style="padding:10px 18px" aria-label="Previous page"><i class="fas fa-chevron-left"></i></a>'
        
        for i in range(1, total_pages + 1):
            if i == page_num:
                pag_html += f'<span class="btn bg2" style="padding:10px 18px; pointer-events:none">{i}</span>'
            else:
                link = f'{REL}blog/index.html' if i == 1 else f'{REL}blog/page/{i}/index.html'
                pag_html += f'<a href="{link}" class="btn ba" style="padding:10px 18px">{i}</a>'
                
        if page_num < total_pages:
            next_link = f'{REL}blog/page/{page_num+1}/index.html'
            pag_html += f'<a href="{next_link}" class="btn ba" style="padding:10px 18px" aria-label="Next page"><i class="fas fa-chevron-right"></i></a>'
        pag_html += '</div>'

    # ─── 3. Hero image ────────────────────────────────────────────────────────────
    hero_img = REL + 'wp-content/uploads/2022/11/Hero-Blog-1.jpg'

    # ─── 4. HTML completo ─────────────────────────────────────────────────────────
    html_out = f'''<!doctype html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blog – Hidden Jungle Cusco | Amazon &amp; Manu National Park Travel Tips{" - Page " + str(page_num) if page_num > 1 else ""}</title>
<meta name="description" content="Visit our blog to learn more about us, where we work, what we love about Peru, and tips as you plan your Manu National Park trip.">
<meta property="og:title" content="Blog – Hidden Jungle Cusco">
<meta property="og:description" content="Travel tips, wildlife guides and stories from the Peruvian Amazon.">
<meta property="og:image" content="{hero_img}">
<meta property="og:type" content="website"><meta property="og:url" content="https://www.hiddenjunglecusco.com/blog/">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://www.hiddenjunglecusco.com/blog/">
<link rel="icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="{REL}assets/css/new.css">
<style>
.blog-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin-top: 48px;
}}
.blog-card {{
  background: var(--f);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 20px;
  overflow: hidden;
  transition: transform .35s ease, box-shadow .35s ease, border-color .35s ease;
  display: flex;
  flex-direction: column;
}}
.blog-card:hover {{
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(0,0,0,.45);
  border-color: rgba(201,168,76,.3);
}}
.blog-thumb {{
  position: relative;
  height: 230px;
  overflow: hidden;
}}
.blog-thumb img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .6s ease;
}}
.blog-card:hover .blog-thumb img {{
  transform: scale(1.07);
}}
.blog-thumb::after {{
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 45%, rgba(5,13,8,.55) 100%);
}}
.blog-cat {{
  position: absolute;
  bottom: 14px;
  left: 16px;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: rgba(201,168,76,.18);
  border: 1px solid rgba(201,168,76,.45);
  border-radius: 30px;
  color: var(--a);
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .09em;
  text-transform: uppercase;
  backdrop-filter: blur(8px);
}}
.blog-body {{
  padding: 26px 28px 28px;
  display: flex;
  flex-direction: column;
  flex: 1;
}}
.blog-date {{
  font-size: .74rem;
  color: rgba(255,255,255,.35);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.blog-body h2 {{
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 800;
  line-height: 1.35;
  color: var(--w);
  margin-bottom: 12px;
  transition: color .3s;
}}
.blog-card:hover .blog-body h2 {{
  color: var(--a);
}}
.blog-body p {{
  font-size: .87rem;
  color: rgba(255,255,255,.5);
  line-height: 1.75;
  flex: 1;
  margin-bottom: 18px;
}}
.blog-read {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: .78rem;
  font-weight: 700;
  color: var(--a);
  letter-spacing: .04em;
  text-transform: uppercase;
  transition: gap .3s;
}}
.blog-card:hover .blog-read {{ gap: 12px; }}
@media(max-width:1100px){{ .blog-grid {{ grid-template-columns: repeat(2,1fr); }} }}
@media(max-width:640px){{ .blog-grid {{ grid-template-columns: 1fr; }} }}
</style>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-5476BC9');</script>
</head><body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5476BC9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>

<header id="N"><div class="cx ni">
  <div class="nl"><a href="{REL}index.html"><img src="{REL}wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1.png" alt="Hidden Jungle Cusco" width="190" height="54" loading="eager"></a></div>
  <nav class="nm" aria-label="Main navigation">
    <a href="{REL}index.html">Home</a>
    <div class="hd"><a href="{REL}guided-tours/index.html">Guided Tours <i class="fas fa-caret-down"></i></a>
      <ul class="dm">
        <li><a href="{REL}wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="{REL}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{REL}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{REL}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{REL}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{REL}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{REL}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{REL}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="{REL}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="{REL}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{REL}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
    <a href="{REL}about-2/index.html">About Us</a>
    <a href="{REL}departures/index.html">Departures</a>
    <a href="{REL}news-and-gallery/index.html">Gallery</a>
    <a href="{REL}blog/index.html" class="on">Blog</a>
    <a href="{REL}contact/index.html" class="nb">Book Now</a>
  </nav>
  <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false"><span class="bb"></span><span class="bb"></span><span class="bb"></span></button>
</div></header>

<div class="mo" id="mo" aria-hidden="true">
  <ul class="ml">
    <li><a href="{REL}index.html">Home</a></li>
    <li><button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>
      <ul class="md" id="mdd">
        <li><a href="{REL}wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="{REL}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{REL}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{REL}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{REL}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{REL}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{REL}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{REL}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="{REL}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{REL}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>
        <li><a href="{REL}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{REL}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </li>
    <li><a href="{REL}about-2/index.html">About Us</a></li>
    <li><a href="{REL}departures/index.html">Departures</a></li>
    <li><a href="{REL}news-and-gallery/index.html">Gallery</a></li>
    <li><a href="{REL}blog/index.html">Blog</a></li>
    <li><a href="{REL}contact/index.html">Contact</a></li>
  </ul>
</div>

<main id="main">
<section class="in-hero" style="background-image: url('{hero_img}');">
  <div class="cx">
    <span class="ey">Guides &amp; Insights</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">The Hidden Jungle Blog</h1>
    <p class="hs" style="margin:0 auto">Travel tips, wildlife encounters and insider advice for your Peruvian Amazon adventure — straight from our local family guides.</p>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="r" style="text-align:center; margin-bottom:12px">
      <span class="ey">All Articles</span>
      <h2 class="h2">Stories from the Jungle</h2>
      <p class="ld" style="margin:0 auto">{len(posts)} articles — tips, guides &amp; stories from the Peruvian Amazon</p>
    </div>
    <div class="blog-grid" id="blog-grid">
{cards_html}
    </div>
    
{pag_html}

    <!-- CTA -->
    <div class="r" style="text-align:center; margin-top:80px; padding:64px 40px; background:var(--f); border-radius:24px; border:1px solid rgba(255,255,255,.06)">
      <span class="ey">Ready to go?</span>
      <h2 class="h2" style="max-width:560px;margin:0 auto 18px">Stop Reading — Start Exploring</h2>
      <p class="ld" style="margin:0 auto 32px">Book your guided tour from Cusco to the Manu National Park. Local. Wild. Authentic.</p>
      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
        <a href="{REL}guided-tours/index.html" class="btn ba"><i class="fas fa-binoculars"></i> See All Tours</a>
        <a href="{REL}contact/index.html" class="btn bg2"><i class="fas fa-envelope"></i> Contact Us</a>
      </div>
    </div>
  </div>
</section>
</main>

<footer class="ft"><div class="cx">
  <div class="fg">
    <div>
      <a href="{REL}index.html"><img src="{REL}wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png" alt="Hidden Jungle Cusco" class="fl" loading="lazy"></a>
      <p class="fa">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</p>
      <address class="fc">
        <p><i class="fas fa-map-marker-alt"></i><a href="https://goo.gl/maps/B8NjhLZizA6YKwKD6" target="_blank" rel="noopener">Hidden Jungle Cusco – La Casa Escondida 17800, Nuevo Eden, Peru</a></p>
        <p><i class="fas fa-phone"></i><a href="tel:+51979808013">+51 979 808 013</a> / <a href="tel:+51923289231">+51 923 289 231</a></p>
        <p><i class="fas fa-envelope"></i><a href="mailto:discover@hiddenjunglecusco.com">discover@hiddenjunglecusco.com</a></p>
      </address>
      <div class="so">
        <a href="https://www.facebook.com/hiddenjunglecusco" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/hiddenjunglecusco/?hl=en" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="fab fa-tripadvisor"></i></a>
        <a href="https://abnb.me/Ri8XQWoA19" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fab fa-airbnb"></i></a>
        <a href="https://wa.me/51923289231" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.tiktok.com/@hidden.jungle.cus" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
      </div>
    </div>
    <div><p class="fh">Explore</p><ul class="fli"><li><a href="{REL}index.html">Home</a></li><li><a href="{REL}about-2/index.html">About Us</a></li><li><a href="{REL}guided-tours/index.html">Guided Jungle Tours</a></li><li><a href="{REL}departures/index.html">Departures</a></li><li><a href="{REL}news-and-gallery/index.html">Gallery</a></li><li><a href="{REL}blog/index.html">Blog</a></li><li><a href="{REL}contact/index.html">Contact</a></li></ul></div>
    <div><p class="fh">Wildlife Tours</p><ul class="fli"><li><a href="{REL}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife Tour</a></li><li><a href="{REL}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li><li><a href="{REL}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li><li><a href="{REL}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li><li><a href="{REL}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li><li><a href="{REL}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li><li><a href="{REL}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li></ul></div>
    <div><p class="fh">Blog</p><ul class="fli">
      {''.join(f'<li><a href="{REL}{p["slug"]}/index.html">{p["title"][:45]}{"..." if len(p["title"])>45 else ""}</a></li>' for p in posts[:6])}
    </ul></div>
  </div>
  <div class="fb"><div class="fbi"><span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span><span>Site design: Meyer Consulting and Management</span></div></div>
</div></footer>

<a href="https://api.whatsapp.com/send?phone=51923289231&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="fab fa-whatsapp"></i></a>

<script>
(function(){{
  const N=document.getElementById('N');
  window.addEventListener('scroll',()=>N.classList.toggle('s',scrollY>60),{{passive:true}});
  const bg=document.getElementById('bg'),mo=document.getElementById('mo');
  bg.addEventListener('click',()=>{{const o=mo.classList.toggle('o');bg.classList.toggle('o',o);bg.setAttribute('aria-expanded',o);mo.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';}});
  document.getElementById('mbt').addEventListener('click',()=>document.getElementById('mdd').classList.toggle('o'));
  const obs=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('v');obs.unobserve(e.target);}}}})  ,{{threshold:.1}});
  document.querySelectorAll('.r,.rl,.rr').forEach(el=>obs.observe(el));
}})();
</script>
</body></html>
'''
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f'✅  Guardado: {OUT_FILE}  ({len(html_out):,} bytes) (Página {page_num}/{total_pages})')
