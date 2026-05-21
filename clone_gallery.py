import urllib.request, sys, re, os, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

print("Iniciando clone de la galería...")

BASE_URL = 'https://www.hiddenjunglecusco.com'
REL = '../'
OUT_FILE = 'www.hiddenjunglecusco.com/news-and-gallery/index.html'

# 1. Fetch live page
url = f'{BASE_URL}/news-and-gallery/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none'
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8')
except Exception as e:
    print(f"Error descargando {url}: {e}")
    sys.exit(1)

soup = BeautifulSoup(html, 'html.parser')

# 2. Extract hero image
hero_img = ''
for sec in soup.select('.elementor-section-wrap > section.elementor-section, section.elementor-section'):
    style = sec.get('style', '')
    if 'background-image' in style:
        m = re.search(r'url\([\'"]?(.*?)[\'"]?\)', style)
        if m:
            hero_img = m.group(1).replace(BASE_URL + '/', REL).replace(BASE_URL, REL)
            break

if not hero_img:
    hero_img = f'{REL}wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg' # fallback

# 3. Extract Instagram Feed Items
insta_items = []
for item in soup.select('.sbi_item'):
    a_tag = item.select_one('a.sbi_photo')
    if not a_tag: continue
    
    href = a_tag.get('href', '#')
    full_res = a_tag.get('data-full-res', '')
    if not full_res:
        img_tag = a_tag.select_one('img')
        full_res = img_tag.get('src', '') if img_tag else ''
        
    alt_text = ''
    screen_reader = item.select_one('.sbi-screenreader')
    if screen_reader:
        alt_text = screen_reader.text.strip()
        
    is_video = 'sbi_type_video' in item.get('class', [])
    
    insta_items.append({
        'href': href,
        'img': full_res,
        'alt': alt_text,
        'is_video': is_video
    })

# Fallback images in case CDN links are expired (403 Forbidden)
fallback_images = [
    f"{REL}wp-content/uploads/2022/10/tapir7_Snapseed.jpg",
    f"{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Machu-Wasi-1024x576.jpg",
    f"{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Photography-in-the-Jungle.jpg",
    f"{REL}wp-content/uploads/2018/02/HiddenJungleCusco_Sliders_Watercolor.jpg",
    f"{REL}wp-content/uploads/2022/10/andean-cock-of-the-rock-.jpg",
    f"{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Birdwatching-in-Machu-Wasi.jpg"
]

# Download images locally to avoid CDN expiration
insta_dir = 'www.hiddenjunglecusco.com/assets/img/insta'
os.makedirs(insta_dir, exist_ok=True)
for idx, item in enumerate(insta_items):
    local_img_path = f"{insta_dir}/insta_{idx}.jpg"
    fallback = fallback_images[idx % len(fallback_images)]
    
    if item['img'].startswith('http'):
        try:
            req_img = urllib.request.Request(item['img'], headers=headers)
            with urllib.request.urlopen(req_img, timeout=15) as r_img:
                with open(local_img_path, 'wb') as f_img:
                    f_img.write(r_img.read())
            item['local_img'] = f"{REL}assets/img/insta/insta_{idx}.jpg"
        except Exception as e:
            print(f"Error downloading {item['img']}: {e}")
            item['local_img'] = fallback
    else:
        item['local_img'] = item['img'] if item['img'] else fallback

# HTML template
insta_cards = ""
for i in insta_items:
    play_icon = '<div class="play-icon"><i class="fas fa-play"></i></div>' if i['is_video'] else ''
    insta_cards += f'''
      <a href="{i["href"]}" target="_blank" rel="noopener" class="insta-card r" aria-label="{i["alt"]}">
        <img src="{i["local_img"]}" alt="{i["alt"]}" loading="lazy">
        {play_icon}
        <div class="insta-hover">
          <i class="fab fa-instagram"></i>
          <p>{i["alt"][:60] + "..." if len(i["alt"])>60 else i["alt"]}</p>
        </div>
      </a>
'''

html_out = f'''<!doctype html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gallery – Hidden Jungle Cusco</title>
<meta name="description" content="A Look Inside the Jungle. Check out some of the amazing images that we have taken recently in the Amazon Jungle!">
<meta property="og:title" content="Gallery">
<meta property="og:description" content="A Look Inside the Jungle. Check out some of the amazing images!">
<meta property="og:image" content="{hero_img}">
<meta property="og:type" content="website"><meta property="og:url" content="https://www.hiddenjunglecusco.com/news-and-gallery/">
<link rel="canonical" href="https://www.hiddenjunglecusco.com/news-and-gallery/">
<link rel="icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{REL}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="{REL}assets/css/new.css">
<style>
.insta-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 40px;
}}
.insta-card {{
  position: relative;
  display: block;
  overflow: hidden;
  border-radius: 12px;
  background: var(--d);
  aspect-ratio: 1 / 1;
}}
.insta-card img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .5s ease;
}}
.insta-card:hover img {{ transform: scale(1.08); }}
.play-icon {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,.5);
  color: #fff;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  backdrop-filter: blur(4px);
  z-index: 2;
  transition: background .3s;
}}
.insta-card:hover .play-icon {{ background: var(--a); color: var(--k); }}
.insta-hover {{
  position: absolute;
  inset: 0;
  background: rgba(5,13,8,.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity .3s ease;
  z-index: 3;
  padding: 24px;
  text-align: center;
}}
.insta-card:hover .insta-hover {{ opacity: 1; }}
.insta-hover i {{ font-size: 2rem; color: var(--w); }}
.insta-hover p {{ color: rgba(255,255,255,.8); font-size: .85rem; line-height: 1.5; margin: 0; }}
</style>
</head><body>
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
    <a href="{REL}news-and-gallery/index.html" class="on">Gallery</a>
    <a href="{REL}blog/index.html">Blog</a>
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
<section class="in-hero" style="background-image: url('{hero_img}'); background-position:center; background-size:cover;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">Gallery</h1>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="r" style="text-align:center; margin-bottom:48px">
      <span class="ey">Photo Gallery</span>
      <h2 class="h2">A Look inside the Jungle</h2>
      <p class="ld" style="margin:0 auto">Check out some of the amazing moments we have captured recently in the Amazon Jungle!</p>
    </div>
    
    <div class="tour-gallery" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:24px; margin-bottom: 80px;">
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Jaguar.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Jaguar.jpg" alt="Jaguar in the wild" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/04/black-caiman-amazon-discovery-peru.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/04/black-caiman-amazon-discovery-peru.jpg" alt="Black Caiman" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Birdwatching-in-Machu-Wasi.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Birdwatching-in-Machu-Wasi.jpg" alt="Birdwatching in Machu Wasi" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Black-Spider-Monkey-with-Baby.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Black-Spider-Monkey-with-Baby.jpg" alt="Black Spider Monkey with Baby" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Guided-Tour-Hiking.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Guided-Tour-Hiking.jpg" alt="Guided Tour Hiking" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Brown-Capuchin-Monkey.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Brown-Capuchin-Monkey.jpg" alt="Brown Capuchin Monkey" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2022/10/Road-trip-5-days_.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2022/10/Road-trip-5-days_.jpg" alt="Road Trip" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2018/06/HiddenJungleCusco_JungleBungalow7.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2018/06/HiddenJungleCusco_JungleBungalow7.jpg" alt="Jungle Bungalow" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2018/02/HiddenJungleCusco_PeruvianJungle5.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2018/02/HiddenJungleCusco_PeruvianJungle5.jpg" alt="Peruvian Jungle" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Squirrel-Monkey.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Squirrel-Monkey.jpg" alt="Squirrel Monkey" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily.jpg" alt="Jungle Family" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
      <a href="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Cock-of-the-Rock-1024x576.jpg" target="_blank" class="gallery-item">
        <img src="{REL}wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Cock-of-the-Rock-1024x576.jpg" alt="Cock of the Rock" loading="lazy" style="width:100%; height:300px; object-fit:cover; border-radius:16px; transition:transform .4s ease;">
      </a>
    </div>

    <div class="r" style="text-align:center; margin-bottom:48px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 80px;">
      <span class="ey">Social Feed</span>
      <h2 class="h2">Video Highlights</h2>
      <p class="ld" style="margin:0 auto">Check out some of our video reels on Instagram!</p>
    </div>
    
    <div class="insta-grid">
{insta_cards}
    </div>

    <div style="text-align:center; margin-top:40px;">
      <a href="https://www.instagram.com/hiddenjunglecusco/" target="_blank" rel="noopener" class="btn bg2">
        <i class="fab fa-instagram"></i> Follow on Instagram
      </a>
    </div>
    
    <!-- CTA -->
    <div class="r" style="text-align:center; margin-top:80px; padding:64px 40px; background:var(--f); border-radius:24px; border:1px solid rgba(255,255,255,.06)">
      <span class="ey">Experience it yourself</span>
      <h2 class="h2" style="max-width:560px;margin:0 auto 18px">Ready for the Jungle?</h2>
      <p class="ld" style="margin:0 auto 32px">See these amazing animals and landscapes in person.</p>
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
    <div><p class="fh">Expeditions</p><ul class="fli"><li><a href="{REL}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li><li><a href="{REL}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li><li><a href="{REL}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li><li><a href="{REL}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li><li><a href="{REL}live-like-a-local-4d-3n/index.html">Live Like a Local – 4D/3N</a></li><li><a href="{REL}live-like-a-local-5d-4n/index.html">Live Like a Local – 5D/4N</a></li></ul></div>
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

print(f"✅  Página de galería regenerada en {OUT_FILE} con hero image: {hero_img}")
