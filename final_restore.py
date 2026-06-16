import os
import requests
import re
from bs4 import BeautifulSoup

def update_about_page():
    path = "www.hiddenjunglecusco.com/about-2/index.html"
    if not os.path.exists(path):
        print("about-2/index.html not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Create the new bio grid with images
    bio_html = """    <div class="bio-grid r" style="grid-template-columns: 1fr; gap: 48px;">
      
      <div class="bio-card" style="text-align: left; padding: 40px; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
        <img src="../wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily.jpg" alt="Moises Llaqui" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; border: 4px solid rgba(201,168,76,.3);">
        <div style="flex: 1; min-width: 250px;">
          <h3 style="font-size:1.8rem; margin-bottom:8px">Moises Llaqui</h3>
          <p class="bio-role" style="color:var(--a); margin-bottom: 20px;">Founder &amp; Local Guide</p>
          <p>I am a tour guide in the Manu National Park in Peru. When I was just a little boy, my parents set up our home in the jungle, I grew up with a special connection to the natural world around me. My parents taught me about medicinal plants, native food, and how we could survive and thrive in the jungle.</p>
          <p>Over time, my father established a school, and the town started to grow, family by family. My family also grew — I have 5 younger sisters, all of whom were raised in the jungle. When I outgrew the local school, my father organized for me to study at a school in Shintyua that was for kids from Native Communities in the area.</p>
          <p>As I got older, my father’s main gift to me was sending me to Cusco, to study Jungle Tourism. I’ve been working as a tour guide now for many years, and love to share the jungle with people from all over the world. If you travel with me, I will share with you the secrets and intricacies about this impressive place.</p>
        </div>
      </div>

      <div class="bio-card" style="text-align: left; padding: 40px; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
        <img src="../wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily_Anna.jpg" alt="Anna" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; border: 4px solid rgba(201,168,76,.3);">
        <div style="flex: 1; min-width: 250px;">
          <h3 style="font-size:1.8rem; margin-bottom:8px">Anna</h3>
          <p class="bio-role" style="color:var(--a); margin-bottom: 20px;">Co-Founder &amp; Logistics</p>
          <p>Anna caught the travel bug from a young age, intrigued by different cultures and languages. She visited Peru for the first time while traveling for work, and decided to stay a while to really know the culture.</p>
          <p>As a traveler, she’s visited over 30 countries and always seeks out unique, local experiences. She’s created Hidden Jungle Cusco for travelers like her, who want to have a fun, relaxed genuine experience in a different country.</p>
        </div>
      </div>

      <div class="bio-card" style="text-align: left; padding: 40px; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
        <img src="../wp-content/uploads/2020/12/jordi-llaqui-chusi.jpg" alt="Jordy Llaqui" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; border: 4px solid rgba(201,168,76,.3);">
        <div style="flex: 1; min-width: 250px;">
          <h3 style="font-size:1.8rem; margin-bottom:8px">Jordy Llaqui</h3>
          <p class="bio-role" style="color:var(--a); margin-bottom: 20px;">Jungle Specialist &amp; Guide</p>
          <p>He was born on August 1994 and grew up in the Manu National Park. He and his family used the abundant resources around them to live and prosper in the jungle, embracing the nature around them, and learning how to navigate the challenges as well.</p>
          <p>He went to primary school in the area, then moved to Cusco where he studied Tourism at the Instituto Americana de Turismo. As a jungle specialist, Jordy is very knowledgeable about the many species of birds in Peru, animals, plants, insects, and all wildlife. His goal is help to conserve and preserve the jungle and is passionate about sharing and teaching people about nature and the world in Manu National Park.</p>
        </div>
      </div>
      
      <div class="bio-card" style="text-align: left; padding: 40px; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
        <img src="../wp-content/uploads/2020/11/hidden-jungle-cusco-cayetano.jpg" alt="Cayetano Llaqui" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; border: 4px solid rgba(201,168,76,.3);">
        <div style="flex: 1; min-width: 250px;">
          <h3 style="font-size:1.8rem; margin-bottom:8px">Cayetano Llaqui</h3>
          <p class="bio-role" style="color:var(--a); margin-bottom: 20px;">Pioneer &amp; Boat Builder</p>
          <p>To say Cayetano has had a remarkable life would be an understatement. In a time of political unrest in Peru, and after serving in the army, he found his way to the jungle when he was a young man. Learning every useful skill along the way, he became a boat maker and started a family, living a nomadic life as work required.</p>
          <p>When it was time to find a permanent home for his family, Cayetano found a perfect spot that’s now Nuevo Eden. A pristine stream and perfect location made this the perfect place to settle down. Little by little other families joined them and the town began to grow.</p>
          <p>Fast forward to today. Thanks to Cayetano’s persistence, the town now has schools, shops, access via road to Cusco, and more. He now spends his days running a small shop, raising fish, and tinkering as a mechanic. He will love to share stories of his life in the jungle with you.</p>
        </div>
      </div>
      
      <div class="bio-card" style="text-align: left; padding: 40px; display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
        <img src="../wp-content/uploads/2020/12/Webp.net-resizeimage-13.jpg" alt="Mama Placida" style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; border: 4px solid rgba(201,168,76,.3);">
        <div style="flex: 1; min-width: 250px;">
          <h3 style="font-size:1.8rem; margin-bottom:8px">Mama Placida</h3>
          <p class="bio-role" style="color:var(--a); margin-bottom: 20px;">Family Heart &amp; Chief Cook</p>
          <p>Generous, hospitable, and big-hearted, Mama Placida is a force of energy in Nuevo Eden. She raised 6 children in the jungle, working hard to ensure that everyone always had what they needed.</p>
          <p>She is energetic and always smiling and laughing, a lover of life. If you’re interested, she’ll take you to her field of crops one day, and you’ll want to try any of the yummy dishes that she expertly cooks for her family.</p>
        </div>
      </div>
      
    </div>"""

    new_html = re.sub(r'<div class="bio-grid r".*?</div>\s*</div>\s*</section>', bio_html + '\n  </div>\n</section>', html, flags=re.DOTALL)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Updated about-2 with images")

def get_all_articles():
    articles = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    for p in range(1, 4):
        url = "https://www.hiddenjunglecusco.com/blog/" if p == 1 else f"https://www.hiddenjunglecusco.com/blog/page/{p}/"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        links = [a.get('href') for a in soup.select('.elementor-post__title a')]
        for l in links:
            slug = l.rstrip('/').split('/')[-1]
            articles.add(slug)
    return list(articles)

# Template constants
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

def restore_article_full(slug):
    url = f"https://www.hiddenjunglecusco.com/{slug}/"
    print(f"Fetching full article: {slug}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    meta = extract_metadata(soup)
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else slug.replace('-', ' ').title()

    # Extract article content perfectly, preserving images
    content_block = soup.select_one(".elementor-widget-theme-post-content")
    if content_block:
        rich_html = content_block.decode_contents()
    else:
        editors = soup.select(".elementor-widget-text-editor .elementor-widget-container")
        rich_html = "".join([e.decode_contents() for e in editors])
        
    # Replace absolute internal image paths with relative paths
    rich_html = rich_html.replace('https://www.hiddenjunglecusco.com/wp-content', '../wp-content')
    
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
    
    path = f"www.hiddenjunglecusco.com/{slug}/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header + body + footer)
    print(f"Created {slug}/index.html")

if __name__ == "__main__":
    update_about_page()
    articles = get_all_articles()
    print(f"Found {len(articles)} articles!")
    for a in articles:
        restore_article_full(a)
    print("All tasks completed.")
