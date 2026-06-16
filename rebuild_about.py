import os

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

html_content = """<!doctype html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>All About Us – Hidden Jungle Cusco</title>
<meta name="description" content="Learn about our family, local tour guides, safe ground and river transport, clean lodges, and conservation efforts in the Manu National Park.">
<meta property="og:title" content="All About Us – Hidden Jungle Cusco">
<meta property="og:description" content="Discover the passionate locals, family guides, safe transport and local lodges that make your Peruvian Amazon tour unforgettable.">
<meta property="og:image" content="../wp-content/uploads/2025/08/Hidden_Jungle_Drone__optimized.jpg">
<meta property="og:type" content="website"><meta property="og:url" content="https://www.hiddenjunglecusco.com/about-2/">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://www.hiddenjunglecusco.com/about-2/">
<link rel="icon" href="../wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="../assets/css/new.css">
<style>
  .intro-text p { font-size: 1.15rem; line-height: 1.85; color: rgba(255,255,255,.8); margin-bottom: 24px; text-align: left; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; margin-bottom: 60px; }
  .grid-2:nth-child(even) { direction: rtl; }
  .grid-2:nth-child(even) .col-text { direction: ltr; }
  .grid-2 img { width: 100%; border-radius: 16px; box-shadow: 0 16px 40px rgba(0,0,0,.3); border: 1px solid rgba(255,255,255,.05); object-fit: cover; height: 380px; }
  .col-text span.ey { display: block; color: var(--a); font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; font-size: .85rem; }
  .col-text h3 { font-family: 'Syne', sans-serif; font-size: 2.2rem; color: var(--w); margin-bottom: 16px; font-weight: 800; }
  .col-text p { font-size: 1.05rem; line-height: 1.75; color: rgba(255,255,255,.75); margin-bottom: 16px; }
  
  .lodge-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; margin-top: 40px; }
  .lodge-card { background: rgba(255,255,255,.02); border: 1px solid rgba(255,255,255,.05); border-radius: 20px; padding: 24px; display: flex; flex-direction: column; gap: 16px; backdrop-filter: blur(10px); }
  .lodge-card img { width: 100%; height: 200px; object-fit: cover; border-radius: 12px; }
  .lodge-card h4 { font-family: 'Syne', sans-serif; font-size: 1.4rem; color: var(--w); font-weight: 700; }
  .lodge-card p { font-size: .95rem; line-height: 1.65; color: rgba(255,255,255,.65); }

  .bio-row { display: flex; gap: 40px; background: rgba(255,255,255,.01); border: 1px solid rgba(255,255,255,.03); border-radius: 24px; padding: 40px; align-items: flex-start; margin-bottom: 40px; }
  .bio-row img { width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 4px solid var(--a); flex-shrink: 0; box-shadow: 0 12px 30px rgba(0,0,0,.4); }
  .bio-desc h3 { font-family: 'Syne', sans-serif; font-size: 1.8rem; color: var(--w); margin-bottom: 4px; font-weight: 800; }
  .bio-desc span.role { display: block; color: var(--a); font-weight: 600; font-size: .9rem; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
  .bio-desc p { font-size: 1.05rem; line-height: 1.8; color: rgba(255,255,255,.75); margin-bottom: 16px; }

  .destination-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 48px; }
  .destination-card { background: rgba(255,255,255,.02); border: 1px solid rgba(255,255,255,.05); border-radius: 24px; overflow: hidden; }
  .destination-card img { width: 100%; height: 260px; object-fit: cover; }
  .destination-info { padding: 32px; }
  .destination-info h3 { font-family: 'Syne', sans-serif; font-size: 1.6rem; color: var(--w); margin-bottom: 16px; font-weight: 700; }
  .destination-info p { font-size: 1rem; line-height: 1.7; color: rgba(255,255,255,.7); margin-bottom: 12px; }

  @media(max-width:991px) {
    .grid-2 { grid-template-columns: 1fr; gap: 32px; }
    .grid-2:nth-child(even) { direction: ltr; }
    .grid-2 img { height: 280px; }
    .bio-row { flex-direction: column; align-items: center; text-align: center; }
    .destination-grid { grid-template-columns: 1fr; }
  }
</style>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-5476BC9');</script>
</head><body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5476BC9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>

<header id="N"><div class="cx ni">
  <div class="nl"><a href="../index.html"><img src="../wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1.png" alt="Hidden Jungle Cusco" width="190" height="54" loading="eager"></a></div>
  <nav class="nm" aria-label="Main navigation">
    <a href="../index.html">Home</a>
    <div class="hd"><a href="../guided-tours/index.html" class="on">Guided Tours <i class="fas fa-caret-down"></i></a>
      <ul class="dm">
        <li><a href="../wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="../rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
    <a href="index.html" class="on">About Us</a>
    <a href="../departures/index.html">Departures</a>
    <a href="../news-and-gallery/index.html">Gallery</a>
    <a href="../blog/index.html">Blog</a>
    <a href="../contact/index.html" class="nb">Book Now</a>
  </nav>
  <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false"><span class="bb"></span><span class="bb"></span><span class="bb"></span></button>
</div></header>

<div class="mo" id="mo" aria-hidden="true">
  <ul class="ml">
    <li><a href="../index.html">Home</a></li>
    <li><button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>
      <ul class="md" id="mdd">
        <li><a href="../wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="../2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="../5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>
        <li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </li>
    <li><a href="index.html">About Us</a></li>
    <li><a href="../departures/index.html">Departures</a></li>
    <li><a href="../news-and-gallery/index.html">Gallery</a></li>
    <li><a href="../blog/index.html">Blog</a></li>
    <li><a href="../contact/index.html">Contact</a></li>
  </ul>
</div>

<main id="main">
<!-- Hero Section -->
<section class="in-hero h-lg" style="background-image: url('../wp-content/uploads/2025/08/Hidden_Jungle_Drone__optimized.jpg'); background-size: cover; background-position: center; position: relative; padding: 220px 0 120px; text-align: center;">
  <div style="content: ''; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(5,13,8,.7) 0%, var(--k) 100%); z-index: 1;"></div>
  <div class="cx cr r" style="position: relative; z-index: 2;">
    <span class="ey">All About Us</span>
    <h1 class="h1" style="font-size:clamp(2.5rem,6vw,4.5rem)">Our Heritage &amp; Vision</h1>
    <p class="ld">Local, Professional Tour Operator in the Manu Biosphere</p>
  </div>
</section>

<!-- Introduction Section -->
<section class="sec" style="background:var(--k)">
  <div class="cx">
    <div style="max-width: 900px; margin: 0 auto; text-align: center; margin-bottom: 80px;">
      <span class="ey" style="display: block; color: var(--a); font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;">Local Travel Agency</span>
      <h2 class="h2" style="font-size: clamp(1.8rem, 4vw, 2.8rem); line-height: 1.3; margin-bottom: 32px;">Jungle Trips from Cusco with a Local Travel Agency, Peru</h2>
      <div class="intro-text">
        <p>If you’re planning a trip to South America, you probably want to visit the top destinations, but not get stuck in any tourist traps along the way. If the Amazon Rainforest is on your list, there are a lot of options to choose from, different countries to visit, and lots of information to sort through. Let’s talk about the adventure you can have with us to the Jungle.</p>
        <p>We’re based in Cusco, Peru, and operate trips to the jungle that neighbors the Andes Mountains in Madre de Dios. Our trips start in Cusco, and visit the Manu National Park. You can choose between a 3-day quick trip if that’s all the time you have, or we can take you on an 8-day journey deep into the jungle to search for all kinds of animals (or anything in between).</p>
        <p>Why visit the Manu National Park? Of the jungle trips from Cusco that you can take, Manu is less-touristic, more wild, is an area that needs tourism to help protect the neighboring rainforest. From native communities to banana farmers, coca plantations and virgin jungle, there is a lot to see and learn about in the area.</p>
        <p>Of course, the main reason to visit the Amazon is to see animals. On a trip with us, you will have the chance to see many kinds of monkeys, toucans, macaws, capybaras, caimans, frogs, snakes, the blue morpho butterfly, and the allusive jaguar. Each of our tour pages will give you an idea of what animals you may see on your trip to the Manu National Park.</p>
        <p>We are a small business with big ambitions to help use tourism as a force for positive change in our home of Nuevo Eden, a tiny village in Manu. Together with our family, local guides, drivers, and chefs, you will have a unique and adventurous tour to the Amazon Rainforest.</p>
        <p>For more information about our team and story, keep reading. Or, click <a href="../guided-tours/index.html" style="color:var(--a); font-weight:600; text-decoration:underline;">here</a> for more information about our tours.</p>
      </div>
    </div>
  </div>
</section>

<!-- Columns Section: Logistics and Transport -->
<section class="sec" style="background:var(--f); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div style="text-align: center; margin-bottom: 64px;">
      <span class="ey" style="display: block; color: var(--a); font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">Pillars of our Operations</span>
      <h2 class="h2">Professional, Safe &amp; Caring Operations</h2>
    </div>

    <div>
      <!-- Block 1 -->
      <div class="grid-2">
        <img src="../wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Guided-Tour-Hiking.jpg" alt="Tour guide Moises Llaqui teaches travelers about the jungle" loading="lazy">
        <div class="col-text">
          <span class="ey">Eco-Friendly Operations</span>
          <h3>Local, Professional Tour Operator</h3>
          <span class="ey" style="color:rgba(255,255,255,.6); font-size:1.15rem; text-transform:none; letter-spacing:0; margin-bottom:16px;">Caring for our rainforest &amp; visitors</span>
          <p>The rainforest is an exciting, beautiful, exotic destination. Our leaders and travel team have years of experience transporting, guiding, and feeding international travelers to the Manu National Park for more than a decade.</p>
          <p>We have two priorities: taking care of you, the traveler, and taking care of our home, the jungle. Working with professionals who are local to the area, limiting our footprint, and supporting reforestation efforts all help us run eco-friendly jungle trips.</p>
        </div>
      </div>

      <!-- Block 2 -->
      <div class="grid-2">
        <img src="../wp-content/uploads/2022/10/1P7A3487_Original.jpg" alt="A van on the ready for a Manu National Park Tour" loading="lazy">
        <div class="col-text">
          <span class="ey">Safety on the Road</span>
          <h3>Ground Transport</h3>
          <span class="ey" style="color:rgba(255,255,255,.6); font-size:1.15rem; text-transform:none; letter-spacing:0; margin-bottom:16px;">Professional Drivers and Safe Vans</span>
          <p>The road from Cusco to Manu is winding and bumpy, and our drivers know the road like the back of their hands. All vehicles are inspected and drivers have all documentation in order, and lots of experience driving travelers on these roads.</p>
        </div>
      </div>

      <!-- Block 3 -->
      <div class="grid-2">
        <img src="../wp-content/uploads/2022/10/Wildlife-Quest-4dyas-eden.jpg" alt="A boat on the Madre de Dios River" loading="lazy">
        <div class="col-text">
          <span class="ey">Madre de Dios Navigation</span>
          <h3>River Transport</h3>
          <span class="ey" style="color:rgba(255,255,255,.6); font-size:1.15rem; text-transform:none; letter-spacing:0; margin-bottom:16px;">Boat travel on the river</span>
          <p>You can’t miss the opportunity to travel by boat to the jungle. From the boat you get fresh air, beautiful views, and a chance to see Amazon wildlife on the river banks. Our boats are made of metal, about 20 meters (65 feet) long, and have space for all travelers, crew, and gear to make the journey.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Section: Accommodation & Food -->
<section class="sec" style="background:var(--k); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div style="text-align: center; max-width:700px; margin: 0 auto 60px;">
      <span class="ey">Our Accommodations &amp; Cuisine</span>
      <h2 class="h2">Where You Will Stay &amp; What You Will Eat</h2>
      <p style="color:rgba(255,255,255,.6); margin-top:16px;">We operate private, fully equipped eco-lodges and offer freshly prepared, highly customizable local cuisine.</p>
    </div>

    <div class="lodge-grid">
      <!-- Lodge 1 -->
      <div class="lodge-card">
        <img src="../wp-content/uploads/elementor/thumbs/Bambu_Outside_optimized-1-ra7adzsznigk4xhm06ydxr2t609v22ybrw3tzcm8og.jpg" alt="Bambu Lodge" loading="lazy">
        <h4>Lodging: Bambu Lodge</h4>
        <p>The first night of each of our trips is spent at Bambu Lodge, just outside of Patria.</p>
        <p>Here you will sleep in a mosquito net, with a private bathroom with a shower with “room temperature” water. A small towel is provided, but you will want to have your own shampoo and soap. This is a rented lodge, where multiple groups might stay.</p>
      </div>

      <!-- Lodge 2 -->
      <div class="lodge-card">
        <img src="../wp-content/uploads/2025/08/Eden_Little_Houses_optimized.jpg" alt="Nuevo Eden Lodge" loading="lazy">
        <h4>Lodging: Nuevo Eden Lodge</h4>
        <p>We have 3 properties in Nuevo Eden: 2 private rooms/bathrooms for couples or a small family, and 2 bedrooms with a shared bathroom for larger groups. This is our unique property located near the village where Hidden Jungle Founder Moises grew up.</p>
      </div>

      <!-- Lodge 3 -->
      <div class="lodge-card">
        <img src="../wp-content/uploads/2025/08/Nuevo_Eden_Clay_Lick_Platform_optimized.jpg" alt="Camouflage House" loading="lazy">
        <h4>Lodging: Camouflage House</h4>
        <p>Located on the Llaqui family land, this platform is the perfect place to enjoy a night in the open-air jungle. You will be provided with mosquito nets and mattresses. Sleeping bags are available to rent, and you’ll want to bring something to use as a pillow. You’ll enjoy the sounds of the jungle while watching for nocturnal animal activity.</p>
      </div>

      <!-- Food -->
      <div class="lodge-card">
        <img src="../wp-content/uploads/2025/08/Hidden_Jungle_Food_optimized.jpg" alt="Amazon Cuisine" loading="lazy">
        <h4>Delicious Amazonian Food</h4>
        <p>You will enjoy freshly prepared, full meals on each day of the trip. Our team of chefs can tailor the menu of a group or individual traveler to any dietary requirement from vegan to celiac, or any allergy.</p>
        <p>We only use clean bottled water at every step of the food preparation process. Plus, every meal will be absolutely delicious!</p>
      </div>
    </div>
  </div>
</section>

<!-- Section: Conservation & Geography -->
<section class="sec" style="background:var(--f); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div class="grid-2">
      <div class="col-text">
        <span class="ey">Our Project</span>
        <h3>Community &amp; Conservation</h3>
        <p>We are certain that tourism is the healthiest, most positive industry in the rainforest. The Llaqui family owns a piece of land that we use for trails, lodges, and the camouflage house. It is the only piece of land in the area being used for conservation, and we can feel the benefits of our protection of this land by the flora and fauna.</p>
        <p>Each traveler who visits Nuevo Eden is helping us with this small conservation project, and as we grow, we are dedicated to helping the community and nature in more ways as well.</p>
      </div>
      <img src="../wp-content/uploads/2021/01/Copia-de-Copia-de-Copia-de-Sin-titulo-min.jpg" alt="A traveler enjoys a reforestation workshop in Nuevo Eden" loading="lazy">
    </div>

    <div class="grid-2">
      <img src="../wp-content/uploads/2025/08/Hidden_Jungle_Drone__optimized.jpg" alt="A photo from above of the Madre de Dios River in the Manu National Park" loading="lazy">
      <div class="col-text">
        <span class="ey">The Ecosystem</span>
        <h3>Manu National Park, Peru</h3>
        <p>The Manu National Park is an enormous place that spans 4 distinct regions: the high mountains (Acjanaco), the Cloud Forest, the High Jungle (Patria &amp; Machu Wasi), and the Low Jungle (Nuevo Eden, the Reserved Zone, and Blanquillo).</p>
        <p>Based on your budget, trip length, and interests, we can’t wait to share the biodiversity, natural wonders, flavors, and local culture of the Manu National Park with you.</p>
        <p style="font-weight: 700; color: var(--a);">Vamos a la selva!</p>
      </div>
    </div>
  </div>
</section>

<!-- Section: Our Story & Team -->
<section class="sec" style="background:var(--k); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div style="max-width: 800px; margin: 0 auto 64px; text-align: center;">
      <span class="ey">Our Story</span>
      <h2 class="h2">The Llaqui Family &amp; Friends</h2>
      <div style="font-size:1.15rem; line-height:1.8; color:rgba(255,255,255,.7); margin-top:24px;">
        <p style="margin-bottom: 20px; font-weight:700; color:var(--w);">Dear Curious Traveler,</p>
        <p style="margin-bottom: 20px;">Our team at Hidden Jungle Cusco is excited to share your jungle travel with you. We are a family business, working with local professionals to create an unforgettable experience.</p>
        <p style="margin-bottom: 20px;">The Llaqui family will welcome you and be your guides. Moises has been a professional tour guide in the Amazon jungle for many years, and with Anna’s enthusiasm for travel, they started this project together. They have created these tours and jungle adventures to provide a unique experience in the Manu National Park.</p>
        <p style="margin-bottom: 20px;">When Anna first visited Nuevo Eden, she had already traveled to Manu as a tourist. The Llaqui family were welcoming and generous with their time and hospitality. They organized fishing trips, ate fresh local food, swam in the river, and more. Whereas her trip as a tourist was strictly nature-focused, this trip was a complete immersion into a totally different life. Yet, she was in the same little slice of jungle for both.</p>
        <p>Hidden Jungle Cusco celebrates the whole jungle: the magnificent nature, and the local life. As a traveler, you can choose your priority and focus. We offer 3 types of guided tours that range from very nature-based to very culture-based. Or, you can customize your own adventure using our beautiful jungle bungalow as your base.</p>
      </div>
    </div>

    <div style="max-width: 900px; margin: 60px auto 0;">
      <!-- Moises -->
      <div class="bio-row">
        <img src="../wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily.jpg" alt="Moises loves taking photos of birds and animals in the jungle">
        <div class="bio-desc">
          <h3>Moises Llaqui Llanca</h3>
          <span class="role">Founder &amp; Local Guide</span>
          <p>I am a tour guide in the Manu National Park in Peru. When I was just a little boy, my parents set up our home in the jungle, I grew up with a special connection to the natural world around me. My parents taught me about medicinal plants, native food, and how we could survive and thrive in the jungle.</p>
          <p>Over time, my father established a school, and the town started to grow, family by family. My family also grew – I have 5 younger sisters, all of whom were raised in the jungle. When I outgrew the local school, my father organized for me to study at a school in Shintyua that was for kids from Native Communities in the area. As I got older, my father’s main gift to me was sending me to Cusco, to study Jungle Tourism. I’ve been working as a tour guide now for many years, and love to share the jungle with people from all over the world. If you travel with me, I will share with you the secrets and intricacies about this impressive place.</p>
        </div>
      </div>

      <!-- Anna -->
      <div class="bio-row">
        <img src="../wp-content/uploads/2018/02/HiddenJungleCusco_JungleFamily_Anna.jpg" alt="Anna, co-founder, on the way to the jungle">
        <div class="bio-desc">
          <h3>Anna Ashley</h3>
          <span class="role">Co-Founder &amp; Logistics</span>
          <p>Anna caught the travel bug from a young age, intrigued by different cultures and languages. She visited Peru for the first time while traveling for work, and decided to stay a while to really know the culture. As a traveler, she’s visited over 30 countries and always seeks out unique, local experiences. She’s created Hidden Jungle Cusco for travelers like her, who want to have a fun, relaxed genuine experience in a different country.</p>
        </div>
      </div>

      <!-- Jordy -->
      <div class="bio-row">
        <img src="../wp-content/uploads/2020/12/jordi-llaqui-chusi.jpg" alt="Tour Guide Jordy teaches travelers about the jungle">
        <div class="bio-desc">
          <h3>Jordy Leonidas LLaqui</h3>
          <span class="role">Jungle Specialist &amp; Guide</span>
          <p>He was born on August 1994 and grew up in the Manu National Park. He and his family used the abundant resources around them to live and prosper in the jungle, embracing the nature around them, and learning how to navigate the challenges as well. He went to primary school in the area, then moved to Cusco where he studied Tourism at the Instituto Americana de Turismo. As a jungle specialist, Jordy is very knowledgeable about the many species of birds in Peru, animals, plants, insects, and all wildlife. His goal is help to conserve and preserve the jungle and is passionate about sharing and teaching people about nature and the world in Manu National Park.</p>
        </div>
      </div>

      <!-- Cayetano -->
      <div class="bio-row">
        <img src="../wp-content/uploads/2020/11/hidden-jungle-cusco-cayetano.jpg" alt="Family member Cayetano Llaqui holding a Paco fish">
        <div class="bio-desc">
          <h3>Cayetano LLaqui</h3>
          <span class="role">Pioneer &amp; Boat Builder</span>
          <p>To say Cayetano has had a remarkable life would be an understatement. In a time of political unrest in Peru, and after serving in the army, he found his way to the jungle when he was a young man. Learning every useful skill along the way, he became a boat maker and started a family, living a nomadic life as work required.</p>
          <p>When it was time to find a permanent home for his family, Cayetano found a perfect spot that’s now Nuevo Eden. A pristine stream and perfect location made this the perfect place to settle down. Little by little other families joined them and the town began to grow.</p>
          <p>Fast forward to today. Thanks to Cayetano’s persistence, the town now has schools, shops, access via road to Cusco, and more. He now spends his days running a small shop, raising fish, and tinkering as a mechanic. He will love to share stories of his life in the jungle with you.</p>
        </div>
      </div>

      <!-- Placida -->
      <div class="bio-row">
        <img src="../wp-content/uploads/2020/12/Webp.net-resizeimage-13.jpg" alt="Family member, Mama Placida, sitting in the Tigre Mayo River in Nuevo Eden">
        <div class="bio-desc">
          <h3>Placida Yanca</h3>
          <span class="role">Family Heart &amp; Chief Cook</span>
          <p>Generous, hospitable, and big-hearted, Mama Placida is a force of energy in Nuevo Eden. She raised 6 children in the jungle, working hard to ensure that everyone always had what they needed. She is energetic and always smiling and laughing, a lover of life. If you’re interested, she’ll take you to her field of crops one day, and you’ll want to try any of the yummy dishes that she expertly cooks for her family.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Section: Insights & Location -->
<section class="sec" style="background:var(--f); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div class="grid-2">
      <div class="col-text">
        <span class="ey">The Experience</span>
        <h3>Why Visit Manu National Park?</h3>
        <p>The Manu Biosphere Reserve is hands down, the best jungle to visit in Peru. It may be off the beaten path compared to other options, but it boasts lush, rich rainforest and a vast range of biodiversity. Manu is mostly untouched by humans, so the animals we see are living their best lives in their natural habitat.</p>
        <p>Manu is deep in the Amazon jungle, where monkeys, macaws, and toucans are regular residents. There are no city lights to interfere with the Milky Way’s dominance of the night sky. River water is clean and pure, and you’ll find critters around every corner.</p>
        <p>Another reason to visit Manu is the incredible journey along the way. Our trips depart from Cusco, the famous Inca city that’s about 3600 meters above sea level. On our journey deep into the rainforest, we will travel through the mountains, through the cloud forest, and descend to the jungle. In just one day of travel, you will enjoy three distinct biomes.</p>
        <p>Hidden Jungle Cusco operates in the Manu Biosphere which contains the Manu National Park and Buffer Zone. The National Park is highly protected, and the buffer zone is where humans are more present and mingle with the neighboring creatures. Our carefully planned jungle tours are a perfect addition to your Cusco trip when visiting Machu Picchu.</p>
      </div>
      <div class="col-text">
        <span class="ey">Our Philosophy</span>
        <h3>Why travel with us?</h3>
        <p>Our tours and trips offer a unique experience for every traveler: a glimpse of daily life in our hometown. We value supporting the local economy and involving our family in our work with tourists. We also want international travelers to taste local flavors and see a slice of a different way of life.</p>
        <p>Our planet is one global community, now more than ever. There is so much division: race, borders, class, and more. We believe that the more we share our lives and realities with people who are different than us, the smaller the world feels, and the more we can understand each other.</p>
        <p>The jungle is also in danger. It’s a prime resource for mining, logging, and cattle farming. Our region is tiny on the map, but we want to do our part to support a sustainable way of life. We want the Amazon jungle to live forever. That means making small, deliberate steps in the right direction. There’s never been a better time to visit the Amazon rainforest.</p>
      </div>
    </div>
  </div>
</section>

<!-- Section: Our Destinations -->
<section class="sec" style="background:var(--k); border-top: 1px solid rgba(255,255,255,.05)">
  <div class="cx">
    <div style="text-align: center; max-width:700px; margin: 0 auto 48px;">
      <span class="ey">Explore Locations</span>
      <h2 class="h2">Our Destinations &amp; Campsites</h2>
      <p style="color:rgba(255,255,255,.6); margin-top:16px;">We guide you through carefully preserved campsites and local settlements deep within the reserve.</p>
    </div>

    <div class="destination-grid">
      <!-- Destination 1 -->
      <div class="destination-card">
        <img src="../wp-content/uploads/2025/08/Nuevo_Eden_Lodges_optimized.jpg" alt="Nuevo Eden Town">
        <div class="destination-info">
          <h3>Nuevo Eden</h3>
          <p>Welcome to our hometown. Founded on a small river, Nuevo Eden is where Moises and his 5 sisters all grew up. During his childhood, the town was only accessible by boat via the Madre de Dios river, and only if one knew where to look. The Llaqui family lived off the land, growing crops, raising animals, and foraging.</p>
          <p>The road from Cusco arrived about 15 years ago. Since then, the population has grown, groceries and goodies are more accessible, and life is a bit easier. There are a few small shops and 2 schools for local children. People work as farmers or run small businesses.</p>
        </div>
      </div>

      <!-- Destination 2 -->
      <div class="destination-card">
        <img src="../wp-content/uploads/2018/06/HiddenJungleCusco_JungleBungalow7.jpg" alt="Casa Matsigenka Lodge">
        <div class="destination-info">
          <h3>Casa Matsigenka – Reserved Zone</h3>
          <p>Deep in the Manu National Park, there are still some groups of Native People living in the rainforest. The Matsigenkas are one of the largest groups living in the Park. They run a comfy but rustic lodge that’s a great base for exploring the surrounding area.</p>
          <p>You’ll have a private room, and there are large communal bathrooms. You’ll find an artisan shop on the property to check out some unique handmade crafts.</p>
          <p style="font-size: .9rem; color: var(--a); margin-top: 16px;"><strong>Accommodation:</strong> Private room in shared bungalow &nbsp;|&nbsp; <strong>Bathroom:</strong> Shared &nbsp;|&nbsp; <strong>Tour:</strong> Manu Wildlife Tour 6 Days</p>
        </div>
      </div>

      <!-- Destination 3 -->
      <div class="destination-card">
        <img src="../wp-content/uploads/2025/08/Quebrada_Negra_optimized.jpg" alt="Quebrada Negra Campsite">
        <div class="destination-info">
          <h3>Quebrada Negra Campsite</h3>
          <p>Adventure lovers will enjoy camping deep in the jungle beside a pristine river. From the campsite, you’ll explore the surrounding jungle, search for wildlife in its natural habitat, and swim and fish in the river.</p>
          <p>Our Travel Team will help set up camp and carry supplies as needed. Tents are provided and sleeping bags are available for rent.</p>
          <p style="font-size: .9rem; color: var(--a); margin-top: 16px;"><strong>Accommodation:</strong> Private tent &nbsp;|&nbsp; <strong>Bathroom:</strong> Bush toilet &nbsp;|&nbsp; <strong>Tour:</strong> Eden Expedition 6 Days</p>
        </div>
      </div>

      <!-- Destination 4 -->
      <div class="destination-card">
        <img src="../wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Machu-Wasi-1024x576.jpg" alt="Machu Wasi Campsite">
        <div class="destination-info">
          <h3>Machu Wasi Campsite</h3>
          <p>On the banks of the Madre de Dios River, a small Oxbow lake is tucked away, teeming with birds. Beside this lake is an ideal spot to camp, with beautiful views of the river, an open clear sky, and a nice place to pitch tents. We will explore the lake while the travel team sets up camp and prepares for a rustic riverside dinner.</p>
          <p><em>Please note: if the weather doesn’t allow for camping, we will stay at a hostel in Salvación.</em></p>
          <p style="font-size: .9rem; color: var(--a); margin-top: 16px;"><strong>Accommodation:</strong> Private tent &nbsp;|&nbsp; <strong>Bathroom:</strong> Bush toilet &nbsp;|&nbsp; <strong>Tour:</strong> Manu Wildlife Tour 5 Days</p>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
"""

# Write out to www.hiddenjunglecusco.com/about-2/index.html
with open("www.hiddenjunglecusco.com/about-2/index.html", "w", encoding="utf-8") as f:
    f.write(html_content + FOOTER_TEMPLATE.format(rel_prefix="../"))

print("SUCCESS: fully self-contained about-2 rebuilt.")
