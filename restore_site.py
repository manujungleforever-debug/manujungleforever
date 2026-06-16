import os
import requests
from bs4 import BeautifulSoup

# Same base templates as before
HEADER_TEMPLATE = """<!doctype html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_description}">
<meta property="og:image" content="{og_image}">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{rel_prefix}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{rel_prefix}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="{rel_prefix}assets/css/new.css">
<style>
{local_style}
</style>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-5476BC9');</script>
</head><body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5476BC9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>

<header id="N"><div class="cx ni">
  <div class="nl"><a href="{rel_prefix}index.html"><img src="{rel_prefix}wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1.png" alt="Hidden Jungle Cusco" width="190" height="54" loading="eager"></a></div>
  <nav class="nm" aria-label="Main navigation">
    <a href="{rel_prefix}index.html">Home</a>
    <div class="hd"><a href="{rel_prefix}guided-tours/index.html" class="on">Guided Tours <i class="fas fa-caret-down"></i></a>
      <ul class="dm">
        <li><a href="{rel_prefix}wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="{rel_prefix}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel_prefix}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel_prefix}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel_prefix}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel_prefix}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{rel_prefix}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{rel_prefix}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="{rel_prefix}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="{rel_prefix}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{rel_prefix}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
    <a href="{rel_prefix}about-2/index.html">About Us</a>
    <a href="{rel_prefix}departures/index.html">Departures</a>
    <a href="{rel_prefix}news-and-gallery/index.html">Gallery</a>
    <a href="{rel_prefix}blog/index.html">Blog</a>
    <a href="{rel_prefix}contact/index.html" class="nb">Book Now</a>
  </nav>
  <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false"><span class="bb"></span><span class="bb"></span><span class="bb"></span></button>
</div></header>

<div class="mo" id="mo" aria-hidden="true">
  <ul class="ml">
    <li><a href="{rel_prefix}index.html">Home</a></li>
    <li><button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>
      <ul class="md" id="mdd">
        <li><a href="{rel_prefix}wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="{rel_prefix}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel_prefix}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel_prefix}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel_prefix}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel_prefix}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{rel_prefix}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{rel_prefix}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="{rel_prefix}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="{rel_prefix}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>
        <li><a href="{rel_prefix}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{rel_prefix}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </li>
    <li><a href="{rel_prefix}about-2/index.html">About Us</a></li>
    <li><a href="{rel_prefix}departures/index.html">Departures</a></li>
    <li><a href="{rel_prefix}news-and-gallery/index.html">Gallery</a></li>
    <li><a href="{rel_prefix}blog/index.html">Blog</a></li>
    <li><a href="{rel_prefix}contact/index.html">Contact</a></li>
  </ul>
</div>
"""

FOOTER_TEMPLATE = """
<footer class="ft"><div class="cx">
  <div class="fg">
    <div>
      <a href="{rel_prefix}index.html"><img src="{rel_prefix}wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png" alt="Hidden Jungle Cusco" class="fl" loading="lazy"></a>
      <p class="fa">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</p>
      <address class="fc">
        <p><i class="fas fa-map-marker-alt"></i><a href="https://goo.gl/maps/B8NjhLZizA6YKwKD6" target="_blank" rel="noopener">Hidden Jungle Cusco – La Casa Escondida 17800, Nuevo Eden, Peru</a></p>
        <p><i class="fas fa-phone"></i><a href="tel:+51979808013">+51 979 808 013</a> / <a href="tel:+51923289231">+51 923 289 231</a></p>
        <p><i class="fas fa-envelope"></i><a href="mailto:discover@hiddenjunglecusco.com">discover@hiddenjunglecusco.com</a></p>
      </address>
      <div class="so">
        <a href="https://www.facebook.com/hiddenjunglecusco" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/hiddenjunglecusco/?hl=en" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="fab fa-tripadvisor"></i></a>
        <a href="https://abnb.me/Ri8XQWoA19" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fab fa-airbnb"></i></a>
        <a href="https://wa.me/51923289231" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.tiktok.com/@hidden.jungle.cus" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
      </div>
    </div>
    <div><p class="fh">Explore</p><ul class="fli"><li><a href="{rel_prefix}index.html">Home</a></li><li><a href="{rel_prefix}about-2/index.html">About Us</a></li><li><a href="{rel_prefix}guided-tours/index.html">Guided Jungle Tours</a></li><li><a href="{rel_prefix}departures/index.html">Departures</a></li><li><a href="{rel_prefix}news-and-gallery/index.html">Gallery</a></li><li><a href="{rel_prefix}blog/index.html">Blog</a></li><li><a href="{rel_prefix}contact/index.html">Contact</a></li></ul></div>
    <div><p class="fh">Wildlife Tours</p><ul class="fli"><li><a href="{rel_prefix}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife Tour</a></li><li><a href="{rel_prefix}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li><li><a href="{rel_prefix}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li><li><a href="{rel_prefix}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li><li><a href="{rel_prefix}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li><li><a href="{rel_prefix}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li><li><a href="{rel_prefix}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li></ul></div>
    <div><p class="fh">Expeditions</p><ul class="fli"><li><a href="{rel_prefix}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li><li><a href="{rel_prefix}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li><li><a href="{rel_prefix}2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li><li><a href="{rel_prefix}5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li><li><a href="{rel_prefix}live-like-a-local-4d-3n/index.html">Live Like a Local – 4D/3N</a></li><li><a href="{rel_prefix}live-like-a-local-5d-4n/index.html">Live Like a Local – 5D/4N</a></li></ul></div>
  </div>
  <div class="fb"><div class="fbi"><span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span><span>Site design: kemmesik</span></div></div>
</div></footer>

<a href="https://api.whatsapp.com/send?phone=51923289231&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" id="whats-flotante"><i class="fab fa-whatsapp"></i></a>

<!-- Universal enquiry modal -->
<div class="modal" id="modal" aria-hidden="true">
  <div class="mb">
    <button class="mc" onclick="closeModal()" aria-label="Close modal"><i class="fas fa-times"></i></button>
    <h2 class="h2" style="margin-bottom:20px; font-size:1.8rem">Book Your Adventure</h2>
    <div class="fm" id="modal-msg"></div>
    <form id="booking-form" onsubmit="submitBooking(event)">
      <div class="fr">
        <label for="b-name">Full Name <span class="req">*</span></label>
        <input type="text" id="b-name" required placeholder="e.g. John Doe">
      </div>
      <div class="fr">
        <label for="b-email">Email Address <span class="req">*</span></label>
        <input type="email" id="b-email" required placeholder="e.g. john@example.com">
      </div>
      <div class="f2c">
        <div class="fr">
          <label for="b-phone">Phone / WhatsApp</label>
          <input type="tel" id="b-phone" placeholder="e.g. +1 555-0199">
        </div>
        <div class="fr">
          <label for="b-date">Preferred Date</label>
          <input type="date" id="b-date">
        </div>
      </div>
      <div class="fr">
        <label for="b-msg">Your Message / Dietary Requests</label>
        <textarea id="b-msg" placeholder="Let us know how we can customize your adventure..."></textarea>
      </div>
      <button type="submit" class="btn ba" style="width:100%; justify-content:center"><i class="fas fa-paper-plane"></i> Send Booking Inquiry</button>
    </form>
  </div>
</div>

<script>
(function(){{
  const N=document.getElementById('N');
  window.addEventListener('scroll',()=>N.classList.toggle('s',scrollY>60),{{passive:true}});
  const bg=document.getElementById('bg'),mo=document.getElementById('mo');
  bg.addEventListener('click',()=>{{const o=mo.classList.toggle('o');bg.classList.toggle('o',o);bg.setAttribute('aria-expanded',o);mo.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';}});
  document.getElementById('mbt').addEventListener('click',()=>document.getElementById('mdd').classList.toggle('o'));
  const obs=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('v');obs.unobserve(e.target);}}}}),{{threshold:.1}});
  document.querySelectorAll('.r,.rl,.rr').forEach(el=>obs.observe(el));
}})();
function openModal() {{ const m = document.getElementById('modal'); m.classList.add('o'); m.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; }}
function closeModal() {{ const m = document.getElementById('modal'); m.classList.remove('o'); m.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; }}
async function submitBooking(e) {{
  e.preventDefault();
  const msg = document.getElementById('modal-msg'); msg.className = 'fm'; msg.innerText = '';
  const payload = {{
    name: document.getElementById('b-name').value,
    email: document.getElementById('b-email').value,
    phone: document.getElementById('b-phone').value,
    date: document.getElementById('b-date').value,
    message: document.getElementById('b-msg').value,
    tour: document.title
  }};
  try {{
    const res = await fetch('{rel_prefix}handlers/send-booking.php', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(payload) }});
    const data = await res.json();
    if(data.success) {{ msg.classList.add('ok'); msg.innerText = 'Thank you! Your inquiry was sent successfully. We will email you shortly.'; document.getElementById('booking-form').reset(); }}
    else {{ msg.classList.add('er'); msg.innerText = data.error || 'Something went wrong. Please try again.'; }}
  }} catch(err) {{ msg.classList.add('er'); msg.innerText = 'Unable to send booking at this time. Please email us directly!'; }}
}}
</script>
</body></html>
"""

HERO_IMAGES = {
    "3-day-wildlife-quest-machu-wasi": "wp-content/uploads/2022/10/Hero-wildlife-cuest-3-dyas-machuwasi.jpg",
    "4-day-wildlife-quest-machu-wasi": "wp-content/uploads/2022/10/Hero-wildlife-cuest-4-days-machuwasi.jpg",
    "4-day-wildlife-quest-nuevo-eden": "wp-content/uploads/2022/10/Wildlife-quest-3days-machuwasi.jpg",
    "5-day-wildlife-quest-nuevo-eden": "wp-content/uploads/2022/10/Wildlife-quest-3days-machuwasi.jpg",
    "6-day-wildlife-quest-blanquillo": "wp-content/uploads/2022/10/Wildlife-quest-6days-Reserved-Zone_1.jpg",
    "6-day-wildlife-quest-reserved-zone": "wp-content/uploads/2022/10/reserved-zone.jpg",
    "8-day-wildlife-photography-tour": "wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Jaguar.jpg",
    "2-day-rainforest-road-trip": "wp-content/uploads/2022/10/Rainforest-Road-Trip-1.jpg",
    "4-day-rainforest-road-trip": "wp-content/uploads/2022/10/Hero-Road-trip-4-days.jpg",
    "5-day-rainforest-road-trip": "wp-content/uploads/2022/10/Hero-Road-trip-5-days.jpg",
    "5-day-amazon-expedition": "wp-content/uploads/2022/10/Hero-Road-trip-4-days.jpg",
    "6-day-amazon-expedition": "wp-content/uploads/2022/10/Hero-Road-trip-5-days.jpg",
    "live-like-a-local-4d-3n": "wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg",
    "live-like-a-local-5d-4n": "wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg",
    "wildlife-tours-from-cusco": "wp-content/uploads/2022/10/Hero-wildlife-cuest-6-dyas-reserved-zone.jpg",
    "rainforest-road-trip-from-cusco": "wp-content/uploads/2022/10/Hero-wildlife-cuest-3-dyas-machuwasi.jpg",
    "amazon-expedition-from-cusco": "wp-content/uploads/2022/10/Hero-Road-trip-4-days.jpg",
    "cusco-to-machu-wasi": "wp-content/uploads/2022/10/Hero-wildlife-cuest-3-dyas-machuwasi.jpg",
    "cusco-to-nuevo-eden": "wp-content/uploads/2022/10/Wildlife-quest-3days-machuwasi.jpg"
}

ITINERARY_LOCAL_STYLE = """
.in-hero { position: relative; padding: 220px 0 140px; background-size: cover; background-position: center; background-repeat: no-repeat; text-align: center; }
.in-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(5,13,8,.7) 0%, var(--k) 100%); z-index: 1; }
.in-hero .cx { position: relative; z-index: 2; }
.itinerary-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 48px; margin-top: 48px; }
.itinerary-list { display: flex; flex-direction: column; gap: 20px; }
.itinerary-card { background: var(--f); border: 1px solid rgba(255,255,255,.05); border-radius: 16px; overflow: hidden; transition: var(--t); }
.itinerary-card:hover { border-color: rgba(201,168,76,.3); box-shadow: 0 12px 32px rgba(0,0,0,.3); }
.itinerary-toggle { width: 100%; padding: 24px 32px; display: flex; align-items: center; justify-content: space-between; text-align: left; font-weight: 700; background: rgba(255,255,255,.01); transition: var(--t); }
.itinerary-toggle:hover { background: rgba(255,255,255,.03); }
.day-badge { background: rgba(201,168,76,.15); border: 1px solid rgba(201,168,76,.4); color: var(--a); font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; padding: 6px 14px; border-radius: 20px; margin-right: 18px; flex-shrink: 0; }
.day-title { font-family: 'Syne', sans-serif; font-size: 1.15rem; color: var(--w); flex: 1; }
.itinerary-toggle i { color: rgba(255,255,255,.4); transition: transform var(--t); margin-left: 12px; }
.itinerary-card.open .itinerary-toggle i { transform: rotate(180deg); color: var(--a); }
.itinerary-content { max-height: 0; overflow: hidden; transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1); padding: 0 32px; }
.itinerary-card.open .itinerary-content { max-height: 2000px; padding-bottom: 28px; }
.itinerary-content p { color: rgba(255,255,255,.65); font-size: .95rem; line-height: 1.8; margin-bottom: 12px; }
.spec-card { background: var(--d); border: 1px solid rgba(255,255,255,.08); border-radius: 24px; padding: 44px 36px; position: sticky; top: 100px; height: fit-content; }
.spec-item { display: flex; align-items: center; gap: 16px; padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
.spec-item:last-child { border-bottom: none; }
.spec-icon { width: 44px; height: 44px; border-radius: 50%; background: rgba(201,168,76,.1); display: flex; align-items: center; justify-content: center; color: var(--a); font-size: 1.1rem; }
.spec-label { font-size: .75rem; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .06em; }
.spec-val { font-size: .92rem; font-weight: 600; color: var(--w); }
.inc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 48px; }
.inc-card { background: var(--f); border: 1px solid rgba(255,255,255,.05); border-radius: 20px; padding: 44px; }
.inc-title { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; margin-bottom: 24px; display: flex; align-items: center; gap: 12px; }
.inc-list { display: flex; flex-direction: column; gap: 14px; }
.inc-item { display: flex; align-items: flex-start; gap: 12px; font-size: .92rem; color: rgba(255,255,255,.65); line-height: 1.6; }
.inc-item i { color: var(--v); margin-top: 4px; }
.exc-list .inc-item i { color: var(--a); }
.tour-rich-text h2, .tour-rich-text h3, .tour-rich-text h4, .tour-rich-text h5 { color: var(--w); font-family: 'Syne', sans-serif; margin: 32px 0 16px; font-size: 1.4rem; }
.tour-rich-text p { color: rgba(255,255,255,0.7); font-size: 1.05rem; line-height: 1.8; margin-bottom: 20px; }
.tour-rich-text ul { color: rgba(255,255,255,0.7); margin-left: 20px; margin-bottom: 24px; }
.tour-rich-text li { margin-bottom: 8px; }
@media(max-width:900px) { .itinerary-grid, .inc-grid { grid-template-columns: 1fr; } }
"""

ARTICLE_LOCAL_STYLE = """
.in-hero { position: relative; padding: 220px 0 120px; background-size: cover; background-position: center; background-repeat: no-repeat; text-align: center; }
.in-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(5,13,8,.7) 0%, var(--k) 100%); z-index: 1; }
.in-hero .cx { position: relative; z-index: 2; }
.article-w { max-width: 820px; margin: 0 auto; padding: 60px 24px 100px; }
.article-meta { display: flex; align-items: center; gap: 16px; font-size: .85rem; color: var(--v); font-weight: 600; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 24px; }
.article-content { font-size: 1.05rem; color: rgba(255,255,255,.75); line-height: 1.9; }
.article-content p { margin-bottom: 28px; }
.article-content h2, .article-content h3, .article-content h4 { font-family: 'Syne', sans-serif; font-weight: 800; margin: 48px 0 20px; color: var(--w); line-height: 1.3; }
.article-content h2 { font-size: 2rem; }
.article-content h3 { font-size: 1.6rem; }
.article-content ul, .article-content ol { margin-left: 20px; margin-bottom: 28px; }
.article-content li { margin-bottom: 12px; }
.article-content img { border-radius: 16px; margin: 36px 0; border: 1px solid rgba(255,255,255,.05); max-width: 100%; height: auto; }
"""

def extract_metadata(soup):
    meta = {}
    title_tag = soup.find('title')
    meta['title'] = title_tag.text if title_tag else "Hidden Jungle Cusco"
    
    desc_tag = soup.find('meta', {'name': 'description'})
    meta['description'] = desc_tag['content'] if desc_tag else ""
    
    og_title = soup.find('meta', {'property': 'og:title'})
    meta['og_title'] = og_title['content'] if og_title else meta['title']
    
    og_desc = soup.find('meta', {'property': 'og:description'})
    meta['og_description'] = og_desc['content'] if og_desc else meta['description']
    return meta

def restore_itinerary(folder):
    url = f"https://www.hiddenjunglecusco.com/{folder}/"
    print(f"Fetching {url} ...")
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    meta = extract_metadata(soup)
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else folder.replace('-', ' ').title()

    # Extract all rich text blocks that are not accordions/inclusions/gallery
    rich_html = ""
    # Usually the first 3-5 text-editors contain the overview, highlights, and how to book
    # But some might be in other widgets. Let's get ALL text-editors that aren't footer
    editors = soup.select(".elementor-widget-text-editor .elementor-widget-container")
    for e in editors:
        # Ignore empty or copyright text
        text = e.text.lower()
        if "copyright" in text or "consulting" in text: continue
        rich_html += e.decode_contents() + "\n"

    # Also check if there are standalone Headings outside of accordions
    headings = soup.select(".elementor-widget-heading .elementor-heading-title")
    # We will just rely on the text editors which usually include the bold tags, or we can manually insert headings.
    # To be extremely thorough, let's grab the raw HTML of the inner sections, but it's full of elementor divs.
    # Instead, we will clean the rich_html
    
    itinerary_html = ""
    accordions = soup.select(".elementor-accordion-item")
    for idx, acc in enumerate(accordions):
        title_el = acc.select_one(".elementor-accordion-title")
        content_el = acc.select_one(".elementor-tab-content")
        if title_el and content_el:
            active_class = " open" if idx == 0 else ""
            itinerary_html += f'''
            <div class="itinerary-card{active_class}">
              <button class="itinerary-toggle" onclick="toggleAccordion(this)">
                <span class="day-badge">Day {idx+1}</span>
                <span class="day-title">{title_el.text.strip()}</span>
                <i class="fas fa-chevron-down"></i>
              </button>
              <div class="itinerary-content">
                {content_el.decode_contents()}
              </div>
            </div>
            '''

    inclusions = []
    exclusions = []
    # Identify lists
    icon_lists = soup.select(".elementor-icon-list-item")
    for item in icon_lists:
        text = item.text.strip()
        if not text: continue
        # Simple heuristic to split inc/exc
        if "not included" in text.lower() or "not" in text.lower() or "tips" in text.lower() or "final dinner" in text.lower():
            exclusions.append(text)
        else:
            inclusions.append(text)

    # Deduplicate
    inclusions = list(dict.fromkeys(inclusions))
    exclusions = list(dict.fromkeys(exclusions))

    inc_html = "".join([f'<div class="inc-item"><i class="fas fa-check-circle"></i><span>{i}</span></div>' for i in inclusions])
    exc_html = "".join([f'<div class="inc-item"><i class="fas fa-times-circle"></i><span>{e}</span></div>' for e in exclusions])

    hero_bg = HERO_IMAGES.get(folder, "wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg")
    hero_bg_path = "../" + hero_bg
    
    og_image = hero_bg_path

    header = HEADER_TEMPLATE.format(
        title=meta['title'], description=meta['description'], og_title=meta['og_title'], 
        og_description=meta['og_description'], og_image=og_image, canonical="index.html", 
        rel_prefix="../", local_style=ITINERARY_LOCAL_STYLE
    )
    header = header.replace('background-size: cover;', f'background-image: url("{hero_bg_path}"); background-size: cover;')

    body = f"""
<main id="main">
<section class="in-hero">
  <div class="cx">
    <span class="ey">Wilderness Expedition</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">{h1_text}</h1>
    <p class="hs" style="margin:0 auto">An authentic journey designed to explore Peru's untouched Amazonian biodiversity.</p>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    
    <div class="tour-rich-text">
      {rich_html}
    </div>

    <div class="itinerary-grid">
      <div>
        <span class="ey">The Journey Plan</span>
        <h2 class="h2">Day-by-Day Itinerary</h2>
        <div class="itinerary-list" style="margin-top:24px">
          {itinerary_html}
        </div>
      </div>
      <div>
        <div class="spec-card">
          <h3 class="h2" style="font-size:1.6rem; margin-bottom:20px">Quick Specs</h3>
          <div class="spec-item"><div class="spec-icon"><i class="fas fa-clock"></i></div><div><div class="spec-label">Duration</div><div class="spec-val">{folder.split('-')[0].upper()} Days</div></div></div>
          <div class="spec-item"><div class="spec-icon"><i class="fas fa-map-marker-alt"></i></div><div><div class="spec-label">Starting Point</div><div class="spec-val">Cusco, Peru</div></div></div>
          <div class="spec-item"><div class="spec-icon"><i class="fas fa-compass"></i></div><div><div class="spec-label">Destination</div><div class="spec-val">Manu National Park</div></div></div>
          <div class="spec-item"><div class="spec-icon"><i class="fas fa-user-shield"></i></div><div><div class="spec-label">Group Size</div><div class="spec-val">Small Groups / Private</div></div></div>
          <button class="btn ba" onclick="openModal()" style="width:100%; margin-top:32px; justify-content:center"><i class="fas fa-calendar-check"></i> Book This Tour</button>
        </div>
      </div>
    </div>
    
    <div class="inc-grid">
      <div class="inc-card"><h3 class="inc-title"><i class="fas fa-plus-circle" style="color:var(--v)"></i> What's Included</h3><div class="inc-list">{inc_html if inc_html else "All standard inclusions apply."}</div></div>
      <div class="inc-card"><h3 class="inc-title" style="color:var(--a)"><i class="fas fa-minus-circle" style="color:var(--a)"></i> What's Not Included</h3><div class="inc-list exc-list">{exc_html if exc_html else "Personal items not included."}</div></div>
    </div>
  </div>
</section>
</main>
<script>
function toggleAccordion(btn) {{
  const card = btn.parentElement;
  const content = card.querySelector('.itinerary-content');
  const isOpen = card.classList.contains('open');
  document.querySelectorAll('.itinerary-card').forEach(c => {{
    c.classList.remove('open'); c.querySelector('.itinerary-content').style.maxHeight = null;
  }});
  if (!isOpen) {{ card.classList.add('open'); content.style.maxHeight = content.scrollHeight + "px"; }}
}}
document.addEventListener('DOMContentLoaded', () => {{
  const first = document.querySelector('.itinerary-card.open .itinerary-content');
  if (first) first.style.maxHeight = first.scrollHeight + "px";
}});
</script>
"""
    footer = FOOTER_TEMPLATE.format(rel_prefix="../")
    
    path = f"www.hiddenjunglecusco.com/{folder}/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header + body + footer)

def restore_article(folder):
    url = f"https://www.hiddenjunglecusco.com/{folder}/"
    print(f"Fetching Article {url} ...")
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    meta = extract_metadata(soup)
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else folder.replace('-', ' ').title()

    # Extract article content perfectly
    content_block = soup.select_one(".elementor-widget-theme-post-content")
    if content_block:
        rich_html = content_block.decode_contents()
    else:
        # Fallback to general text editors if not found
        editors = soup.select(".elementor-widget-text-editor .elementor-widget-container")
        rich_html = "".join([e.decode_contents() for e in editors])

    hero_bg_path = "../wp-content/uploads/2024/06/Cusco-Photo-scaled.jpg"
    
    header = HEADER_TEMPLATE.format(
        title=meta['title'], description=meta['description'], og_title=meta['og_title'], 
        og_description=meta['og_description'], og_image=hero_bg_path, canonical="index.html", 
        rel_prefix="../", local_style=ARTICLE_LOCAL_STYLE
    )
    header = header.replace('background-size: cover;', f'background-image: url("{hero_bg_path}"); background-size: cover;')

    body = f"""
<main id="main">
<section class="in-hero">
  <div class="cx">
    <span class="ey">Jungle Travel Guide</span>
    <h1 class="h1" style="font-size:clamp(2rem,5vw,3.8rem); line-height:1.1">{h1_text}</h1>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="article-w">
    <div class="article-meta">
      <span><i class="fas fa-calendar-alt"></i> Travel Insight</span>
      <span>&middot;</span>
      <span>By Local Amazon Family Guides</span>
    </div>
    
    <article class="article-content">
      {rich_html}
    </article>
    
    <div style="margin-top:60px; padding:44px; background:var(--f); border-radius:24px; border:1px solid rgba(255,255,255,.05); text-align:center">
      <h3 class="h2" style="font-size:1.8rem; margin-bottom:14px">Plan Your Custom Adventure Today</h3>
      <p style="color:rgba(255,255,255,.6); font-size:.95rem; margin-bottom:28px; line-height:1.7">Want to explore the Amazon with us? Connect directly with Cayetano and Moisés to plan a customized, off-the-beaten-path Peruvian safari.</p>
      <button class="btn ba" onclick="openModal()"><i class="fas fa-paper-plane"></i> Get Free Quote</button>
    </div>
  </div>
</section>
</main>
"""
    footer = FOOTER_TEMPLATE.format(rel_prefix="../")
    
    path = f"www.hiddenjunglecusco.com/{folder}/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header + body + footer)

if __name__ == "__main__":
    sub_tours = [
        "3-day-wildlife-quest-machu-wasi",
        "4-day-wildlife-quest-machu-wasi",
        "4-day-wildlife-quest-nuevo-eden",
        "5-day-wildlife-quest-nuevo-eden",
        "6-day-wildlife-quest-blanquillo",
        "6-day-wildlife-quest-reserved-zone",
        "8-day-wildlife-photography-tour",
        "2-day-rainforest-road-trip",
        "4-day-rainforest-road-trip",
        "5-day-rainforest-road-trip",
        "5-day-amazon-expedition",
        "6-day-amazon-expedition",
        "live-like-a-local-4d-3n",
        "live-like-a-local-5d-4n"
    ]
    
    articles = [
        "why-visit-the-manu-national-park",
        "five-reasons-to-visit-manu-national-park",
        "how-tourism-helps-the-manu-national-park",
        "off-the-beaten-path-places-to-visit-from-cusco",
        "packing-list-for-your-trip-to-the-peruvian-amazon",
        "peru-travel-tips",
        "ten-days-in-peru",
        "the-sacred-valley-of-the-incas-a-comprehensive-guide",
        "everything-you-need-to-know-before-visiting-machu-picchu"
    ]
    
    for t in sub_tours:
        restore_itinerary(t)
        
    for a in articles:
        restore_article(a)
        
    print("Restore and modernizations completed successfully!")
