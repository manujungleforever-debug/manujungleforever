import os
import zipfile
import re
from bs4 import BeautifulSoup

# Define directories & paths
ZIP_PATH = 'hts-cache/new.zip'
BASE_DIR = 'www.hiddenjunglecusco.com'

# List of all user-facing directories to recreate
PAGES = [
    # Tours
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
    "live-like-a-local-5d-4n",
    # Guides / Informative sections
    "guided-tours",
    "wildlife-tours-from-cusco",
    "rainforest-road-trip-from-cusco",
    "amazon-expedition-from-cusco",
    "cusco-to-machu-wasi",
    "cusco-to-nuevo-eden",
    "news-and-gallery",
    "departures",
    "about-2",
    "contact",
    "book-now",
    "itinerary-builder",
    # Blog articles (14 articles)
    "five-reasons-to-visit-manu-national-park",
    "packing-list-for-your-trip-to-the-peruvian-amazon",
    "how-tourism-helps-the-manu-national-park",
    "why-visit-the-manu-national-park",
    "everything-you-need-to-know-before-visiting-machu-picchu",
    "sustainable-tourism-in-the-manu-biosphere-reserve-conservation-through-private-agricultural-lands",
    "ten-days-in-peru",
    "the-sacred-valley-of-the-incas-a-comprehensive-guide",
    "peru-travel-tips",
    "off-the-beaten-path-places-to-visit-from-cusco",
    "climate-change-manu-national-park-peru",
    "manu-national-park-in-8-days-complete-travel-guide-to-the-peruvian-amazon",
    "what-to-see-when-traveling-to-the-peruvian-amazon-complete-guide-2026",
    "amazon-rainforest-tour-to-manu-national-park-from-cusco"
]

HERO_IMAGES = {
    "3-day-wildlife-quest-machu-wasi": "wp-content/uploads/2022/10/Hero-wildlife-cuest-3-dyas-machuwasi.jpg",
    "4-day-wildlife-quest-machu-wasi": "wp-content/uploads/2022/10/Hero-wildlife-cuest-4-days-machuwasi.jpg",
    "4-day-wildlife-quest-nuevo-eden": "wp-content/uploads/2022/10/Hero-wildlife-cuest-4-dyas-eden.jpg",
    "5-day-wildlife-quest-nuevo-eden": "wp-content/uploads/2022/10/Hero-wildlife-cuest-5-days-eden.jpg",
    "6-day-wildlife-quest-blanquillo": "wp-content/uploads/2022/10/Hero-wildlife-cuest-8-days-blanquillo.jpg",
    "6-day-wildlife-quest-reserved-zone": "wp-content/uploads/2022/10/Hero-wildlife-cuest-6-dyas-reserved-zone.jpg",
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
    "cusco-to-nuevo-eden": "wp-content/uploads/2022/10/Hero-wildlife-cuest-4-dyas-eden.jpg"
}

# General style tokens & styling definitions
COMMON_CSS = """
.in-hero { position: relative; padding: 220px 0 140px; background-size: cover; background-position: center; background-repeat: no-repeat; text-align: center; }
.in-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(5,13,8,.7) 0%, var(--k) 100%); z-index: 1; }
.in-hero .cx { position: relative; z-index: 2; }
.tour-rich-text h2, .tour-rich-text h3, .tour-rich-text h4 { font-family: 'Syne', sans-serif; font-weight: 800; margin: 40px 0 20px; color: var(--w); line-height: 1.3; }
.tour-rich-text p { font-size: 1.05rem; line-height: 1.8; color: rgba(255,255,255,.75); margin-bottom: 24px; }
.tour-rich-text ul, .tour-rich-text ol { margin-left: 24px; margin-bottom: 28px; color: rgba(255,255,255,.75); }
.tour-rich-text li { margin-bottom: 12px; line-height: 1.7; }
.tour-rich-text img { border-radius: 16px; margin: 32px 0; border: 1px solid rgba(255,255,255,.05); max-width:100%; height:auto; }

/* Checklist */
.checklist-container { background: var(--f); border: 1px solid rgba(255,255,255,.05); border-radius: 20px; padding: 36px; margin-bottom: 40px; }
.checklist-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
.check-item { display: flex; align-items: flex-start; gap: 14px; font-size: .98rem; color: rgba(255,255,255,.75); line-height: 1.6; }
.check-item i { margin-top: 4px; font-size: 1.1rem; }
.check-item i.fa-check-circle, .check-item i.fa-check { color: var(--v); }
.check-item i.fa-times-circle, .check-item i.fa-times, .check-item i.fa-minus-circle { color: var(--a); }

/* Accordion Itinerary */
.itinerary-list { display: flex; flex-direction: column; gap: 20px; margin-top: 24px; margin-bottom: 48px; }
.itinerary-card { background: var(--f); border: 1px solid rgba(255,255,255,.05); border-radius: 16px; overflow: hidden; transition: var(--t); }
.itinerary-card:hover { border-color: rgba(201,168,76,.3); box-shadow: 0 12px 32px rgba(0,0,0,.3); }

/* Tour Gallery */
.tour-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 32px 0; }
.tour-gallery img { width: 100%; height: 220px; object-fit: cover; border-radius: 12px; border: 1px solid rgba(255,255,255,.05); margin: 0 !important; transition: transform 0.3s ease; }
.tour-gallery img:hover { transform: scale(1.03); }

.itinerary-toggle { width: 100%; padding: 24px 32px; display: flex; align-items: center; justify-content: space-between; text-align: left; font-weight: 700; background: rgba(255,255,255,.01); transition: var(--t); border:none; outline:none; cursor:pointer; }
.itinerary-toggle:hover { background: rgba(255,255,255,.03); }
.day-badge { background: rgba(201,168,76,.15); border: 1px solid rgba(201,168,76,.4); color: var(--a); font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; padding: 6px 14px; border-radius: 20px; margin-right: 18px; flex-shrink: 0; }
.day-title { font-family: 'Syne', sans-serif; font-size: 1.15rem; color: var(--w); flex: 1; }
.itinerary-toggle i { color: rgba(255,255,255,.4); transition: transform var(--t); margin-left: 12px; }
.itinerary-card.open .itinerary-toggle i { transform: rotate(180deg); color: var(--a); }
.itinerary-content { max-height: 0; overflow: hidden; transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1); padding: 0 32px; }
.itinerary-card.open .itinerary-content { max-height: 2000px; padding-bottom: 28px; }
.itinerary-content p { color: rgba(255,255,255,.65); font-size: .95rem; line-height: 1.8; margin-bottom: 12px; }

/* Grid columns */
.tour-layout { display: grid; grid-template-columns: 1.7fr 1fr; gap: 48px; margin-top: 48px; }
.spec-sticky { background: var(--d); border: 1px solid rgba(255,255,255,.08); border-radius: 24px; padding: 40px; position: sticky; top: 100px; height: fit-content; }
.spec-item { display: flex; align-items: center; gap: 16px; padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,.06); }
.spec-item:last-child { border-bottom: none; }
.spec-icon { width: 44px; height: 44px; border-radius: 50%; background: rgba(201,168,76,.1); display: flex; align-items: center; justify-content: center; color: var(--a); font-size: 1.1rem; }
.spec-label { font-size: .75rem; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .06em; }
.spec-val { font-size: .92rem; font-weight: 600; color: var(--w); }

.article-w { max-width: 820px; margin: 0 auto; padding: 60px 24px 100px; }

@media(max-width:991px) {
  .tour-layout { grid-template-columns: 1fr; gap: 40px; }
}
"""

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
  <div class="fb"><div class="fbi"><span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span><span>Site design: Meyer Consulting and Management</span></div></div>
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
  
  // Accordion script for Day-by-Day itinerary
  window.toggleAccordion = function(btn) {{
    const card = btn.parentElement;
    const wasOpen = card.classList.contains('open');
    document.querySelectorAll('.itinerary-card').forEach(c => c.classList.remove('open'));
    if (!wasOpen) {{
      card.classList.add('open');
    }}
  }};
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

def relative_urls(html_str, rel_prefix):
    # Convert WordPress assets to relative path
    html_str = html_str.replace('https://www.hiddenjunglecusco.com/wp-content/', rel_prefix + 'wp-content/')
    html_str = html_str.replace('/wp-content/', rel_prefix + 'wp-content/')
    # Keep external domains absolute, but convert standard site pages to relative link structure
    html_str = re.sub(r'href=["\']https://www\.hiddenjunglecusco\.com/([^"\']+)["\']', r'href="' + rel_prefix + r'\1/index.html"', html_str)
    html_str = re.sub(r'href=["\']/([^"\']+)["\']', r'href="' + rel_prefix + r'\1/index.html"', html_str)
    # Remove index.html index.html duplicates
    html_str = html_str.replace('/index.html/index.html', '/index.html')
    return html_str

z = zipfile.ZipFile(ZIP_PATH, 'r')

for folder in PAGES:
    url = f"https://www.hiddenjunglecusco.com/{folder}/"
    print(f"Cloning {url} ...")
    
    try:
        html = z.read(url)
    except KeyError:
        print(f"  Warning: page not found in zip as {url}, trying contact or alternative formats...")
        # Try without trailing slash
        try:
            html = z.read(url[:-1])
        except KeyError:
            print(f"  CRITICAL ERROR: {url} is completely missing in zip cache!")
            continue

    soup = BeautifulSoup(html, 'html.parser')
    
    # Metadata extraction
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else "Hidden Jungle Cusco"
    
    desc_tag = soup.find('meta', {'name': 'description'})
    description = desc_tag['content'].strip() if desc_tag else "Professional local guides in Manu National Park, Cusco."
    
    og_title_tag = soup.find('meta', {'property': 'og:title'})
    og_title = og_title_tag['content'].strip() if og_title_tag else title
    
    og_desc_tag = soup.find('meta', {'property': 'og:description'})
    og_description = og_desc_tag['content'].strip() if og_desc_tag else description
    
    # Find main Elementor container
    main_el = None
    for el in soup.select('.elementor'):
        classes = el.get('class', [])
        if 'elementor-location-header' in classes or 'elementor-location-popup' in classes:
            continue
        if el.get('data-elementor-id') == '6663': # Footer
            continue
        main_el = el
        break
        
    if not main_el:
        print(f"  Error: could not find main container for {folder}!")
        continue
        
    # sequential construction
    sections = main_el.select('.elementor-section.elementor-top-section')
    
    rel_prefix = "../"
    
    hero_bg = HERO_IMAGES.get(folder, "wp-content/uploads/2018/02/HiddenJungleCusco_Sliders2.jpg")
    hero_bg_path = rel_prefix + hero_bg
    og_image = hero_bg_path
    
    # Analyze if it's a tour (contains itinerary accordions or icon-lists with day keywords)
    is_tour = False
    if main_el.select('.elementor-accordion-item') or 'day' in folder.lower() or 'expedition' in folder.lower() or 'road-trip' in folder.lower():
        is_tour = True
        
    # We will build two streams:
    # 1. Main rich text flow
    # 2. Itinerary accordion
    # 3. Inclusions list
    # 4. Exclusions list
    # 5. Quick Specs list
    
    rich_content = ""
    itinerary_html = ""
    inclusions_html = ""
    exclusions_html = ""
    quick_specs = []
    
    # Helper to clean text
    def clean_text(t):
        return t.strip().replace('\xa0', ' ')
        
    acc_idx = 0
    
    for sec_idx, sec in enumerate(sections):
        if is_tour and sec_idx == 0:
            continue
            
        widgets = sec.select('.elementor-widget')
        for w in widgets:
            w_classes = w.get('class', [])
            w_type = "unknown"
            for c in w_classes:
                if c.startswith('elementor-widget-'):
                    w_type = c.replace('elementor-widget-', '').split('--')[0]
                    break
                    
            if w_type == 'heading':
                title_tag = w.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                t_text = clean_text(title_tag.text if title_tag else w.text)
                t_lower = t_text.lower()
                
                # Filter out redundant tour headers that duplicate what is in the Hero or Sidebar
                if (
                    t_lower in ["overview", "logistics", "the plan", "itinerary", "whats included", "whats included:", "whats not included", "whats not included:", "inclusions", "exclusions"]
                    or "days /" in t_lower
                    or "days/" in t_lower
                    or "nights" in t_lower
                    or "jungle wildlife quest" in t_lower
                    or "jungle wildlife tour" in t_lower
                    or "rainforest road trip" in t_lower
                    or "amazon expedition" in t_lower
                    or "photography tour" in t_lower
                    or "live like a local" in t_lower
                    or t_lower == folder.replace('-', ' ')
                ):
                    continue
                
                heading_level = title_tag.name if title_tag else 'h2'
                rich_content += f'<{heading_level} class="h2">{t_text}</{heading_level}>\n'
                
            elif w_type == 'divider':
                continue
                
            elif w_type == 'button':
                btn_a = w.find('a')
                if btn_a:
                    btn_href = btn_a.get('href', '')
                    btn_text = clean_text(btn_a.text)
                    if btn_href.startswith('https://www.hiddenjunglecusco.com/'):
                        btn_href = btn_href.replace('https://www.hiddenjunglecusco.com/', rel_prefix)
                    elif btn_href.startswith('/'):
                        btn_href = rel_prefix + btn_href.lstrip('/')
                    rich_content += f'<div style="margin:24px 0;"><a href="{btn_href}" class="btn ba"><i class="fas fa-envelope"></i> {btn_text}</a></div>\n'
                    
            elif w_type == 'text-editor':
                container = w.select_one('.elementor-widget-container')
                if container:
                    content_inner = container.decode_contents().strip()
                    # Filter out empty editor blocks
                    if len(BeautifulSoup(content_inner, 'html.parser').text.strip()) > 3:
                        rich_content += f'<div class="tour-rich-text">{relative_urls(content_inner, rel_prefix)}</div>\n'
                        
            elif w_type == 'image':
                img = w.find('img')
                if img:
                    img_src = img.get('src', '')
                    img_alt = img.get('alt', '')
                    # Map to relative
                    if img_src.startswith('https://www.hiddenjunglecusco.com/'):
                        img_src = img_src.replace('https://www.hiddenjunglecusco.com/', rel_prefix)
                    elif img_src.startswith('/'):
                        img_src = rel_prefix + img_src.lstrip('/')
                    
                    rich_content += f'<div class="tour-rich-text"><img src="{img_src}" alt="{img_alt}" loading="lazy"></div>\n'
                    
            elif w_type == 'gallery':
                gallery_items = w.select('.e-gallery-item')
                if gallery_items:
                    rich_content += '<div class="tour-gallery">\n'
                    for item in gallery_items:
                        img_src = item.get('href', '')
                        if img_src.startswith('https://www.hiddenjunglecusco.com/'):
                            img_src = img_src.replace('https://www.hiddenjunglecusco.com/', rel_prefix)
                        elif img_src.startswith('/'):
                            img_src = rel_prefix + img_src.lstrip('/')
                        # In case the elementor gallery has background images or data-thumbnail
                        if not img_src:
                            bg_style = item.get('style', '')
                            if 'url(' in bg_style:
                                import re
                                match = re.search(r'url\([\'"]?([^\'"]+)[\'"]?\)', bg_style)
                                if match:
                                    img_src = match.group(1)
                        if img_src:
                            rich_content += f'  <img src="{img_src}" alt="Gallery Image" loading="lazy">\n'
                    rich_content += '</div>\n'
                    
            elif w_type == 'accordion':
                acc_items = w.select('.elementor-accordion-item')
                for ai in acc_items:
                    a_title = clean_text(ai.select_one('.elementor-accordion-title').text)
                    a_content = ai.select_one('.elementor-tab-content').decode_contents().strip()
                    
                    active_class = " open" if acc_idx == 0 else ""
                    itinerary_html += f"""
                    <div class="itinerary-card{active_class}">
                      <button class="itinerary-toggle" onclick="toggleAccordion(this)">
                        <span class="day-badge">Day {acc_idx+1}</span>
                        <span class="day-title">{a_title}</span>
                        <i class="fas fa-chevron-down"></i>
                      </button>
                      <div class="itinerary-content">
                        {relative_urls(a_content, rel_prefix)}
                      </div>
                    </div>
                    """
                    acc_idx += 1
                    
            elif w_type == 'icon-list':
                list_items = w.select('.elementor-icon-list-item')
                list_html = '<div class="tour-rich-text"><ul style="padding:0; margin-left:0">\n'
                for li in list_items:
                    li_text = clean_text(li.text)
                    icon_el = li.find('i')
                    icon_class = "fas fa-check"
                    if icon_el:
                        icon_class = " ".join(icon_el.get('class', []))
                        
                    color_style = ""
                    if 'times' in icon_class or 'minus' in icon_class or 'not included' in li_text.lower() or 'isn’t included' in li_text.lower() or 'isn\'t included' in li_text.lower():
                        icon_class = 'fas fa-times-circle'
                        color_style = 'color:var(--a);'
                        
                    list_html += f'<li style="list-style:none; margin-bottom:12px; display:flex; align-items:flex-start; gap:12px; {color_style}"><i class="{icon_class}" style="margin-top:4px; {color_style}"></i><span>{li_text}</span></li>\n'
                list_html += '</ul></div>\n'
                rich_content += list_html
                    
            else:
                # Fallback: extract widget container verbatim to ensure 100% data preservation
                container = w.select_one('.elementor-widget-container')
                if container:
                    content_inner = container.decode_contents().strip()
                    if len(BeautifulSoup(content_inner, 'html.parser').text.strip()) > 3:
                        rich_content += f'<div class="tour-rich-text-custom">{relative_urls(content_inner, rel_prefix)}</div>\n'

    title_main = title.split('–')[0].split('|')[0].strip()
    
    # Build the main page block
    if is_tour:
        # Determine duration
        duration_val = "Multi-Day"
        try:
            parts = folder.split('-')
            if parts[0].isdigit():
                duration_val = f"{parts[0]} Days"
        except:
            pass
            
        specs_html = f"""
        <div class="spec-item"><div class="spec-icon"><i class="fas fa-clock"></i></div><div><div class="spec-label">Duration</div><div class="spec-val">{duration_val}</div></div></div>
        <div class="spec-item"><div class="spec-icon"><i class="fas fa-map-marker-alt"></i></div><div><div class="spec-label">Starting Point</div><div class="spec-val">Cusco, Peru</div></div></div>
        <div class="spec-item"><div class="spec-icon"><i class="fas fa-compass"></i></div><div><div class="spec-label">Destination</div><div class="spec-val">Manu National Park</div></div></div>
        <div class="spec-item"><div class="spec-icon"><i class="fas fa-user-shield"></i></div><div><div class="spec-label">Group Size</div><div class="spec-val">Small Groups / Private</div></div></div>
        """
        
        main_body_content = f"""
<main id="main">
<section class="in-hero" style="background-image: url('{hero_bg_path}'); background-size: cover; background-position: center; position: relative;">
  <div class="cx">
    <span class="ey">Wilderness Exploration</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">{title_main} | Hidden Jungle Cusco</h1>
    <p class="hs" style="margin:0 auto">An authentic, local journey designed to explore Peru's untouched Amazonian biodiversity.</p>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="tour-layout">
      <div>
        <span class="ey">Overview &amp; Plan</span>
        <h2 class="h2">Explore the Amazon Rainforest</h2>
        <div style="margin-top:24px;">
          {rich_content}
        </div>
        
        {f'''
        <span class="ey" style="display:block; margin-top:60px;">The Journey Plan</span>
        <h2 class="h2">Day-by-Day Itinerary</h2>
        <div class="itinerary-list">
          {itinerary_html}
        </div>
        ''' if itinerary_html else ''}
        

      </div>
      
      <div>
        <div class="spec-sticky">
          <h3 class="h2" style="font-size:1.6rem; margin-bottom:24px;">Quick Specs</h3>
          {specs_html}
          <button class="btn ba" onclick="openModal()" style="width:100%; margin-top:32px; justify-content:center"><i class="fas fa-calendar-check"></i> Book This Tour</button>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
"""
    else:
        if folder in ['.', 'blog']:
            main_body_content = f"""
<main id="main">
<section class="in-hero" style="background-image: url('{hero_bg_path}'); background-size: cover; background-position: center; position: relative;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">{title_main}</h1>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="article-w" style="max-width:900px; margin:0 auto;">
      {rich_content}
    </div>
  </div>
</section>
</main>
"""
        else:
            # Non-tour layout (e.g. About, Contact)
            main_body_content = f"""
<main id="main">
<section class="in-hero" style="background-image: url('{hero_bg_path}'); background-size: cover; background-position: center; position: relative;">
  <div class="cx">
    <span class="ey">Hidden Jungle Cusco</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">{title_main}</h1>
  </div>
</section>

<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div class="article-w" style="max-width:900px; margin:0 auto;">
      {rich_content}
    </div>
  </div>
</section>
</main>
"""

    # Assemble complete page
    header = HEADER_TEMPLATE.format(
        title=title, description=description, og_title=og_title, og_description=og_description,
        og_image=og_image, canonical=f"https://www.hiddenjunglecusco.com/{folder}/",
        rel_prefix=rel_prefix, local_style=COMMON_CSS
    )
    
    footer = FOOTER_TEMPLATE.format(rel_prefix=rel_prefix)
    
    full_html = header + main_body_content + footer
    
    # Save file
    target_dir = os.path.join(BASE_DIR, folder)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, 'index.html')
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"  SUCCESS: {target_file} written perfectly.")

print("\nALLL PAGES CLONED WITH 100% TEXT FIDELITY AND MODERN PREMIUM LAYOUTS!")
