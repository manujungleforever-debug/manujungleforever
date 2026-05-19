<?php
$rel = $rel ?? '';
?>
<footer class="ft">
  <div class="cx">
    <div class="fg">
      <div>
        <a href="<?= $rel ?>index.php">
          <img src="<?= $rel ?>wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png" alt="Hidden Jungle Cusco" class="fl" loading="lazy">
        </a>
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
      
      <div>
        <p class="fh">Explore</p>
        <ul class="fli">
          <li><a href="<?= $rel ?>index.php">Home</a></li>
          <li><a href="<?= $rel ?>about-2/index.html">About Us</a></li>
          <li><a href="<?= $rel ?>guided-tours/index.html">Guided Jungle Tours</a></li>
          <li><a href="<?= $rel ?>departures/index.html">Departures</a></li>
          <li><a href="<?= $rel ?>news-and-gallery/index.html">Gallery</a></li>
          <li><a href="<?= $rel ?>blog/index.html">Blog</a></li>
          <li><a href="<?= $rel ?>contact/index.html">Contact</a></li>
        </ul>
      </div>
      
      <div>
        <p class="fh">Wildlife Tours</p>
        <ul class="fli">
          <li><a href="<?= $rel ?>3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife Tour</a></li>
          <li><a href="<?= $rel ?>4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
          <li><a href="<?= $rel ?>4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
          <li><a href="<?= $rel ?>5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
          <li><a href="<?= $rel ?>6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
          <li><a href="<?= $rel ?>6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
          <li><a href="<?= $rel ?>8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        </ul>
      </div>
      
      <div>
        <p class="fh">Expeditions</p>
        <ul class="fli">
          <li><a href="<?= $rel ?>5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
          <li><a href="<?= $rel ?>6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
          <li><a href="<?= $rel ?>2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
          <li><a href="<?= $rel ?>5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>
          <li><a href="<?= $rel ?>live-like-a-local-4d-3n/index.html">Live Like a Local – 4D/3N</a></li>
          <li><a href="<?= $rel ?>live-like-a-local-5d-4n/index.html">Live Like a Local – 5D/4N</a></li>
        </ul>
      </div>
    </div>
    
    <div class="fb">
      <div class="fbi">
        <span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span>
        <span>Site design: Meyer Consulting and Management</span>
      </div>
    </div>
  </div>
</footer>

<a href="https://api.whatsapp.com/send?phone=51923289231&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips" class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" id="whats-flotante">
  <i class="fab fa-whatsapp"></i>
</a>

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
