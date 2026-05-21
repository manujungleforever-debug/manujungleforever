"""
clone_articles.py  –  Clona todos los artículos del blog del sitio en vivo
https://www.hiddenjunglecusco.com

Extrae correctamente el contenido de elementor-widget-theme-post-content.
Incluye formato de blog tradicional + sección de comentarios.

Uso: python clone_articles.py
Para agregar nuevos artículos: añadir el slug a la lista ALL_ARTICLES y ejecutar de nuevo.
"""
import urllib.request, sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

BASE_URL = 'https://www.hiddenjunglecusco.com'
REL      = '../'
BASE_DIR = 'www.hiddenjunglecusco.com'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

# ── Lista de TODOS los artículos (añadir nuevos aquí) ─────────────────────────
ALL_ARTICLES = [
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
    'ten-days-in-peru',
    # ← Añadir nuevos slugs de WordPress aquí
]

HERO_IMAGES = {
    'amazon-rainforest-tour-to-manu-national-park-from-cusco':                                              'wp-content/uploads/2022/10/FullSizeRender.jpg',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands':    'wp-content/uploads/2022/10/Group-Shot_-exploring-the-beach-.jpg',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon':                            'wp-content/uploads/2022/10/Wildlife-quest-6dyas-blanquillo_.jpg',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026':                                'wp-content/uploads/2022/10/Road-trip-4-days_1.jpg',
    'climate-change-manu-national-park-peru':                                                               'wp-content/uploads/2025/08/Hidden_Jungle_Drone__optimized.jpg',
    'how-tourism-helps-the-manu-national-park':                                                             'wp-content/uploads/2021/01/family-fishing-e1609677595723.jpg',
    'everything-you-need-to-know-before-visiting-machu-picchu':                                             'wp-content/uploads/2023/11/Everything-You-Need-to-Know-Before-Visiting-Machu-Picchu-1.webp',
    'peru-travel-tips':                                                                                     'wp-content/uploads/2019/07/DSC07062-überarbeitet-e1562085886902.jpg',
    'packing-list-for-your-trip-to-the-peruvian-amazon':                                                    'wp-content/uploads/2022/12/packing-list-for-your-trip-to-the-peruvian-jungle.webp',
    'five-reasons-to-visit-manu-national-park':                                                             'wp-content/uploads/2022/12/five-reasons-to-visit-manu-national-park.webp',
    'ten-days-in-peru':                                                                                     'wp-content/uploads/2022/12/ten-days-in-peru.webp',
}

ARTICLE_DATES = {
    'amazon-rainforest-tour-to-manu-national-park-from-cusco':                                              'May 15, 2026',
    'sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands':    'May 12, 2026',
    'manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon':                            'April 6, 2026',
    'what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026':                                'March 23, 2026',
    'climate-change-manu-national-park-peru':                                                               'March 5, 2026',
    'how-tourism-helps-the-manu-national-park':                                                             'June 22, 2024',
    'everything-you-need-to-know-before-visiting-machu-picchu':                                             'November 16, 2023',
    'peru-travel-tips':                                                                                     'September 20, 2023',
    'packing-list-for-your-trip-to-the-peruvian-amazon':                                                    'December 31, 2022',
    'five-reasons-to-visit-manu-national-park':                                                             'December 31, 2022',
    'ten-days-in-peru':                                                                                     'December 30, 2022',
}

# ── CSS del artículo ───────────────────────────────────────────────────────────
ARTICLE_CSS = """
/* ── Article layout ── */
.article-container { max-width: 820px; margin: 0 auto; padding: 60px 24px 0; }
.article-meta { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 40px; padding-bottom: 28px; border-bottom: 1px solid rgba(255,255,255,.07); }
.article-meta-item { display: flex; align-items: center; gap: 7px; font-size: .8rem; color: rgba(255,255,255,.45); }
.article-meta-item i { color: var(--a); }
.article-cat { display: inline-flex; align-items: center; gap: 6px; padding: 4px 14px; background: rgba(201,168,76,.12); border: 1px solid rgba(201,168,76,.3); border-radius: 30px; color: var(--a); font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }

/* ── Article body ── */
.article-body { font-size: 1.06rem; line-height: 1.9; color: rgba(255,255,255,.78); }
.article-body h1, .article-body h2 { font-family: 'Syne', sans-serif; font-weight: 800; color: var(--w); margin: 48px 0 20px; line-height: 1.2; }
.article-body h1 { font-size: clamp(1.6rem, 3vw, 2.2rem); }
.article-body h2 { font-size: clamp(1.3rem, 2.5vw, 1.8rem); }
.article-body h3, .article-body h4 { font-family: 'Syne', sans-serif; font-weight: 800; color: var(--w); margin: 36px 0 16px; font-size: 1.15rem; }
.article-body p { margin-bottom: 24px; }
.article-body ul, .article-body ol { margin: 0 0 28px 28px; }
.article-body li { margin-bottom: 10px; line-height: 1.8; }
.article-body img { max-width: 100%; height: auto; border-radius: 16px; margin: 36px 0; border: 1px solid rgba(255,255,255,.06); display: block; }
.article-body a { color: var(--a); text-decoration: underline; text-underline-offset: 3px; }
.article-body a:hover { color: var(--al); }
.article-body strong, .article-body b { color: var(--w); font-weight: 700; }
.article-body blockquote { border-left: 3px solid var(--a); padding: 16px 24px; margin: 32px 0; background: rgba(201,168,76,.06); border-radius: 0 12px 12px 0; font-style: italic; color: rgba(255,255,255,.65); }
.article-body .wp-block-image, .article-body figure { margin: 36px 0; }
.article-body figcaption { font-size: .82rem; color: rgba(255,255,255,.35); text-align: center; margin-top: 10px; }

/* ── Nav prev/next ── */
.article-nav { display: flex; gap: 16px; margin: 64px 0 0; padding-top: 40px; border-top: 1px solid rgba(255,255,255,.07); }
.article-nav a { flex: 1; padding: 20px 24px; background: var(--f); border: 1px solid rgba(255,255,255,.06); border-radius: 16px; font-size: .88rem; color: rgba(255,255,255,.6); transition: all .3s; text-decoration: none; }
.article-nav a:hover { border-color: rgba(201,168,76,.35); color: var(--a); transform: translateY(-3px); }
.article-nav .nav-label { font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: rgba(255,255,255,.28); margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
.article-nav .nav-title { font-family: 'Syne', sans-serif; font-weight: 800; font-size: .95rem; color: var(--w); margin-top: 4px; }

/* ── Comments ── */
.comments-section { max-width: 820px; margin: 0 auto; padding: 64px 24px 100px; }
.comments-title { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: var(--w); margin-bottom: 32px; display: flex; align-items: center; gap: 12px; }
.comments-title::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,.07); }
.comment-form-wrap { background: var(--f); border: 1px solid rgba(255,255,255,.07); border-radius: 20px; padding: 36px; }
.comment-form-wrap p { font-size: .9rem; color: rgba(255,255,255,.45); margin-bottom: 28px; }
.cf-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.cf-field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.cf-field label { font-size: .75rem; font-weight: 700; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .08em; }
.cf-field input, .cf-field textarea { padding: 13px 16px; background: rgba(255,255,255,.04); border: 1.5px solid rgba(255,255,255,.1); border-radius: 10px; color: var(--w); font-family: 'Outfit', sans-serif; font-size: .93rem; transition: all .3s; width: 100%; }
.cf-field input:focus, .cf-field textarea:focus { outline: none; border-color: var(--a); background: rgba(255,255,255,.07); }
.cf-field textarea { resize: vertical; min-height: 130px; }
.cf-notice { font-size: .78rem; color: rgba(255,255,255,.3); margin-top: 12px; }
.comment-sent { display:none; padding: 16px 20px; background: rgba(82,183,136,.1); border: 1px solid rgba(82,183,136,.25); border-radius: 12px; color: #74C69D; font-size: .9rem; margin-top: 16px; }

/* ── Related posts ── */
.related-posts { max-width: 820px; margin: 0 auto; padding: 0 24px 80px; }
.related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 24px; }
.related-card { background: var(--f); border: 1px solid rgba(255,255,255,.06); border-radius: 16px; overflow: hidden; text-decoration: none; transition: transform .3s, border-color .3s; display: block; }
.related-card:hover { transform: translateY(-4px); border-color: rgba(201,168,76,.3); }
.related-card img { width: 100%; height: 150px; object-fit: cover; }
.related-card-body { padding: 16px 18px 20px; }
.related-card-body h3 { font-family: 'Syne', sans-serif; font-size: .9rem; font-weight: 800; color: var(--w); line-height: 1.35; transition: color .3s; }
.related-card:hover .related-card-body h3 { color: var(--a); }

@media(max-width:768px) {
  .cf-row { grid-template-columns: 1fr; }
  .related-grid { grid-template-columns: 1fr 1fr; }
  .article-nav { flex-direction: column; }
}
@media(max-width:480px) { .related-grid { grid-template-columns: 1fr; } }
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def fix_urls(html_str):
    html_str = html_str.replace(BASE_URL + '/wp-content/', REL + 'wp-content/')
    html_str = html_str.replace('/wp-content/', REL + 'wp-content/')
    html_str = re.sub(
        r'href=["\']https://www\.hiddenjunglecusco\.com/([^"\'#?]+)/["\']',
        lambda m: f'href="{REL}{m.group(1).strip("/")}/index.html"',
        html_str
    )
    return html_str

def extract_content(soup):
    """Extrae contenido del widget theme-post-content (Elementor) con fallbacks."""
    # 1. El contenido real está dentro del widget theme-post-content
    post_widget = soup.select_one('.elementor-widget-theme-post-content')
    if post_widget:
        inner = post_widget.select_one('.elementor-widget-container')
        if inner:
            # Dentro hay otro Elementor con las secciones reales del artículo
            inner_elementor = inner.select_one('.elementor[data-elementor-type="wp-post"]')
            if inner_elementor:
                # Extraer todos los widgets dentro del post
                result = ''
                for w in inner_elementor.select('.elementor-widget'):
                    wtype = ''
                    for c in w.get('class', []):
                        if c.startswith('elementor-widget-') and c != 'elementor-widget-wrap':
                            wtype = c.replace('elementor-widget-', '')
                            break

                    container = w.select_one('.elementor-widget-container')
                    if not container:
                        continue

                    if wtype == 'heading':
                        h = container.find(['h1','h2','h3','h4','h5','h6'])
                        if h:
                            text = h.get_text(' ', strip=True)
                            if len(text) > 4:
                                result += f'<{h.name}>{text}</{h.name}>\n'

                    elif wtype == 'text-editor':
                        inner_html = container.decode_contents().strip()
                        if len(BeautifulSoup(inner_html, 'html.parser').get_text().strip()) > 3:
                            result += inner_html + '\n'

                    elif wtype == 'image':
                        img = container.find('img')
                        if img:
                            src = img.get('src','')
                            alt = img.get('alt','')
                            result += f'<img src="{src}" alt="{alt}" loading="lazy">\n'

                    elif wtype in ('divider', 'spacer'):
                        result += '<hr style="border:none;border-top:1px solid rgba(255,255,255,.07);margin:40px 0">\n'

                    elif wtype == 'button':
                        a = container.find('a')
                        if a:
                            href = a.get('href','')
                            text = a.get_text(strip=True)
                            result += f'<p><a href="{href}" class="btn ba" style="display:inline-flex"><i class="fas fa-arrow-right"></i> {text}</a></p>\n'

                if result.strip():
                    return fix_urls(result)

    # 2. Fallback: entry-content (WordPress classic)
    entry = soup.select_one('.entry-content, .post-content, article .content')
    if entry:
        for tag in entry.select('script, style, .sharedaddy, .post-navigation'):
            tag.decompose()
        return fix_urls(entry.decode_contents())

    return ''

def get_related(current_slug):
    """Devuelve 3 artículos relacionados (excluyendo el actual)."""
    others = [s for s in ALL_ARTICLES if s != current_slug][:3]
    cards = ''
    for s in others:
        hero = REL + HERO_IMAGES.get(s, 'wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg')
        title = s.replace('-', ' ').title()[:55]
        cards += f'''<a href="{REL}{s}/index.html" class="related-card">
          <img src="{hero}" alt="{title}" loading="lazy">
          <div class="related-card-body"><h3>{title}</h3></div>
        </a>\n'''
    return cards

def get_prev_next(current_slug):
    """Devuelve los links anterior/siguiente."""
    idx = ALL_ARTICLES.index(current_slug) if current_slug in ALL_ARTICLES else -1
    prev_link = next_link = ''
    if idx > 0:
        s = ALL_ARTICLES[idx - 1]
        t = s.replace('-', ' ').title()[:50]
        prev_link = f'<a href="{REL}{s}/index.html"><div class="nav-label"><i class="fas fa-arrow-left"></i> Previous</div><div class="nav-title">{t}</div></a>'
    if idx >= 0 and idx < len(ALL_ARTICLES) - 1:
        s = ALL_ARTICLES[idx + 1]
        t = s.replace('-', ' ').title()[:50]
        next_link = f'<a href="{REL}{s}/index.html" style="text-align:right"><div class="nav-label">Next <i class="fas fa-arrow-right"></i></div><div class="nav-title">{t}</div></a>'
    if not prev_link and not next_link:
        return ''
    return f'<nav class="article-nav" aria-label="Article navigation">{prev_link}{next_link}</nav>'

def build_page(slug, title, description, hero_rel, date, content_html, prev_next_html, related_html):
    disqus_shortname = 'hiddenjunglecusco'  # Disqus shortname del sitio
    return f'''<!doctype html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Hidden Jungle Cusco</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://www.hiddenjunglecusco.com/{hero_rel.lstrip("../").lstrip("/")}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.hiddenjunglecusco.com/{slug}/">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://www.hiddenjunglecusco.com/{slug}/">
<link rel="icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="{REL}assets/css/new.css">
<style>{ARTICLE_CSS}</style>
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

<!-- HERO -->
<section class="in-hero" style="background-image: url('{hero_rel}');">
  <div class="cx">
    <span class="ey"><a href="{REL}blog/index.html" style="color:var(--a);text-decoration:none">← Blog</a></span>
    <h1 class="h1" style="font-size:clamp(1.8rem,4.5vw,3.4rem); max-width:900px; margin:16px auto 0">{title}</h1>
  </div>
</section>

<!-- ARTICLE -->
<section style="background:var(--k)">
  <div class="article-container">

    <!-- Meta -->
    <div class="article-meta">
      <span class="article-cat"><i class="fas fa-leaf"></i> Hidden Jungle Blog</span>
      <span class="article-meta-item"><i class="far fa-calendar-alt"></i> {date}</span>
      <span class="article-meta-item"><i class="fas fa-user"></i> Hidden Jungle Cusco</span>
      <span class="article-meta-item"><i class="fas fa-map-marker-alt"></i> Manu National Park, Peru</span>
    </div>

    <!-- Content -->
    <div class="article-body">
{content_html}
    </div>

    <!-- Comments (below content, above navigation) -->
    <div style="margin-top:64px; padding-top:48px; border-top:1px solid rgba(255,255,255,.07)">
      <h2 class="comments-title"><i class="fas fa-comments" style="color:var(--a)"></i> Leave a Comment</h2>
      <div class="comment-form-wrap">
        <p>We'd love to hear your thoughts! Share your questions or experiences about visiting Manu National Park.</p>
        <form id="comment-form" onsubmit="submitComment(event)">
          <div class="cf-row">
            <div class="cf-field">
              <label for="cf-name">Your Name <span style="color:var(--a)">*</span></label>
              <input type="text" id="cf-name" name="name" placeholder="e.g. Maria Garcia" required>
            </div>
            <div class="cf-field">
              <label for="cf-email">Email Address <span style="color:var(--a)">*</span></label>
              <input type="email" id="cf-email" name="email" placeholder="your@email.com" required>
            </div>
          </div>
          <div class="cf-field">
            <label for="cf-comment">Comment <span style="color:var(--a)">*</span></label>
            <textarea id="cf-comment" name="comment" placeholder="Share your thoughts, questions or experiences..." required></textarea>
          </div>
          <button type="submit" class="btn ba" style="width:100%; justify-content:center"><i class="fas fa-paper-plane"></i> Post Comment</button>
          <p class="cf-notice">Your email will not be published. Required fields marked with *</p>
        </form>
        <div class="comment-sent" id="comment-sent">
          <i class="fas fa-check-circle"></i> Thank you for your comment! We'll review it and publish it shortly.
        </div>
      </div>
    </div>

    <!-- Prev / Next (below comments) -->
    {prev_next_html}

    <!-- CTA -->
    <div style="margin:64px 0 80px; padding:48px 40px; background:var(--f); border-radius:20px; border:1px solid rgba(255,255,255,.06); text-align:center">
      <span class="ey">Ready to go?</span>
      <h2 class="h2" style="font-size:1.7rem; max-width:500px; margin:0 auto 16px">Plan Your Manu Adventure</h2>
      <p style="color:rgba(255,255,255,.5); margin-bottom:28px; max-width:460px; margin-left:auto; margin-right:auto">Guided tours from Cusco deep into the Peruvian Amazon. Local. Wild. Authentic.</p>
      <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap">
        <a href="{REL}guided-tours/index.html" class="btn ba"><i class="fas fa-binoculars"></i> See All Tours</a>
        <a href="{REL}contact/index.html" class="btn bg2"><i class="fas fa-envelope"></i> Contact Us</a>
      </div>
    </div>

  </div><!-- /.article-container -->
</section>

<!-- RELATED POSTS -->
<section style="background:var(--f); border-top:1px solid rgba(255,255,255,.05)">
  <div class="related-posts">
    <h2 class="comments-title"><i class="fas fa-newspaper" style="color:var(--a)"></i> More Articles</h2>
    <div class="related-grid">
      {related_html}
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
    <div><p class="fh">Blog</p><ul class="fli">{''.join(f'<li><a href="{REL}{s}/index.html">{s.replace("-"," ").title()[:40]}</a></li>' for s in ALL_ARTICLES[:6])}</ul></div>
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

// Comment form – sends to the same PHP handler used for bookings
async function submitComment(e) {{
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('[type=submit]');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
  try {{
    const payload = {{
      name: document.getElementById('cf-name').value,
      email: document.getElementById('cf-email').value,
      comment: document.getElementById('cf-comment').value,
      page: window.location.pathname,
      type: 'blog_comment'
    }};
    await fetch('{REL}handlers/send-booking.php', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(payload)
    }});
  }} catch(err) {{}}
  form.style.display = 'none';
  document.getElementById('comment-sent').style.display = 'block';
}}
</script>
</body></html>'''

# ── MAIN ──────────────────────────────────────────────────────────────────────
import argparse
parser = argparse.ArgumentParser(description='Clona artículos del blog')
parser.add_argument('--only', nargs='*', help='Slugs específicos a clonar (omitir = todos)')
parser.add_argument('--force', action='store_true', help='Forzar re-clonado aunque el archivo exista y no esté vacío')
args = parser.parse_args()

slugs_to_clone = args.only if args.only else ALL_ARTICLES

success = skipped = errors = 0
for slug in slugs_to_clone:
    out_path = os.path.join(BASE_DIR, slug, 'index.html')

    # Skip si ya existe y tiene contenido (a menos que --force)
    if not args.force and os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f'⏭  Omitiendo (ya existe): {slug}')
        skipped += 1
        continue

    url = f'{BASE_URL}/{slug}/'
    print(f'\nClonando: {url}')
    try:
        raw = fetch(url)
        print(f'  {len(raw):,} bytes descargados')
    except Exception as e:
        print(f'  ❌ ERROR descargando: {e}')
        errors += 1
        continue

    soup = BeautifulSoup(raw, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.text.split('–')[0].split('|')[0].strip() if title_tag else slug.replace('-',' ').title()
    desc_tag = soup.find('meta', {'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else title

    hero_rel = REL + HERO_IMAGES.get(slug, 'wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg')
    date = ARTICLE_DATES.get(slug, '2024')
    content = extract_content(soup)

    if not content.strip():
        print(f'  ⚠  Sin contenido extraído')
        content = f'<p style="color:rgba(255,255,255,.5);text-align:center;padding:40px 0">Article content coming soon. <a href="{REL}blog/index.html" style="color:var(--a)">← Back to blog</a></p>'

    prev_next = get_prev_next(slug)
    related   = get_related(slug)
    html      = build_page(slug, title, description, hero_rel, date, content, prev_next, related)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ Guardado: {out_path}  ({len(html):,} bytes)')
    success += 1

print(f'\n{"="*55}')
print(f'✅ {success} clonados  |  ⏭  {skipped} omitidos  |  ❌ {errors} errores')
print(f'\n💡 Para agregar un nuevo artículo de WordPress:')
print(f'   1. Añadir el slug a ALL_ARTICLES en este script')
print(f'   2. Añadir la imagen hero a HERO_IMAGES')
print(f'   3. Ejecutar: python clone_articles.py --only nuevo-slug')
print(f'   4. Ejecutar: python clone_blog.py   (actualiza el índice)')
