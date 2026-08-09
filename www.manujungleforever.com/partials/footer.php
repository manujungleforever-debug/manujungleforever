<?php
$rel = $rel ?? '';
?>
<footer class="ft"><div class="cx">
  <div class="fg">
    <div>
      <a href="../index.html"><img src="../assets/img/logo.png" alt="<?php echo htmlspecialchars(SITE_NAME); ?>" class="fl" loading="lazy"></a>
      <p class="fa"><span style="display: block; margin-top: 15px; font-size: 0.95rem; line-height: 1.6; color: rgba(255,255,255,0.65); font-weight: 300;">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local, wild, and authentic.</span></p>
      <address class="fc">
        <p><i class="fas fa-map-marker-alt"></i><a href="https://goo.gl/maps/B8NjhLZizA6YKwKD6" target="_blank" rel="noopener"><?php echo htmlspecialchars(SITE_ADDRESS); ?></a></p>
        <p><i class="fas fa-phone"></i><a href="tel:+51901525679"><?php echo htmlspecialchars(SITE_PHONE); ?></a></p>
        <p><i class="fas fa-envelope"></i><a href="mailto:<?php echo htmlspecialchars(SITE_EMAIL); ?>"><?php echo htmlspecialchars(SITE_EMAIL); ?></a></p>
      </address>
      <div class="so">
        <a href="<?php echo htmlspecialchars(SOCIAL_FACEBOOK); ?>" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
        <a href="<?php echo htmlspecialchars(SOCIAL_INSTAGRAM); ?>" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        <a href="<?php echo htmlspecialchars(SOCIAL_TRIPADVISOR); ?>" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="custom-tripadvisor-icon"></i></a>
        <a href="<?php echo htmlspecialchars(SOCIAL_AIRBNB); ?>" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fa-brands fa-airbnb"></i></a>
        <a href="<?php echo htmlspecialchars(SOCIAL_WHATSAPP); ?>" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
        <a href="<?php echo htmlspecialchars(SOCIAL_TIKTOK); ?>" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fa-brands fa-tiktok"></i></a>
      </div>
    </div>
    <div><p class="fh">Explore</p><ul class="fli"><li><a href="../index.html">Home</a></li><li><a href="../about-2/index.html">About Us</a></li><li><a href="../departures/index.html">Departures</a></li><li><a href="../news-and-gallery/index.html">Gallery</a></li><li><a href="../blog/index.html">Blog</a></li><li><a href="../guided-tours/index.html">Guided Jungle Tours</a></li><li><a href="../contact/index.html">Contact</a></li></ul></div>
    <div><p class="fh">Wildlife Tours</p><ul class="fli"><li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife Tour</a></li><li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li><li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li><li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li><li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li><li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li><li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li></ul></div>
    <div><p class="fh">Expeditions</p><ul class="fli"><li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li><li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li><li><a href="../2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li><li><a href="../5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li><li><a href="../live-like-a-local-4d-3n/index.html">Live Like a Local – 4D/3N</a></li><li><a href="../live-like-a-local-5d-4n/index.html">Live Like a Local – 5D/4N</a></li></ul></div>
  </div>
  <div class="fb"><div class="fbi"><span>Copyright &copy; <?php echo date('Y'); ?> <?php echo htmlspecialchars(SITE_NAME); ?>. All rights reserved.</span><span>Site design: Meyer Consulting and Management</span></div></div>
</div></footer>

<div class="wa-wrap">
    <div class="wa-tooltip">How can I help you?</div>
    <span class="wa-ring"></span>
    <span class="wa-ring"></span>
    <span class="wa-ring"></span>
    <a href="https://api.whatsapp.com/send?phone=51901525679&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
</div>

<script>
(function(){
  // Header scroll
  const N = document.getElementById('N');
  if (N) {
    window.addEventListener('scroll', () => N.classList.toggle('s', window.scrollY > 60), {passive: true});
  }
  // Burger
  const bg = document.getElementById('bg'), mo = document.getElementById('mo');
  if (bg && mo) {
    bg.addEventListener('click', () => {
      const o = mo.classList.toggle('o');
      bg.classList.toggle('o', o);
      bg.setAttribute('aria-expanded', o);
      mo.setAttribute('aria-hidden', !o);
      document.body.style.overflow = o ? 'hidden' : '';
    });
  }
  // Mobile dropdown
  const mbt = document.getElementById('mbt'), mdd = document.getElementById('mdd');
  if (mbt && mdd) {
    mbt.addEventListener('click', () => mdd.classList.toggle('o'));
  }
  // Reveal on scroll
  const obs = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('v');
      obs.unobserve(e.target);
    }
  }), {threshold: 0.1});
  document.querySelectorAll('.r,.rl,.rr').forEach(el => obs.observe(el));
})();
</script>
</body>
</html>
