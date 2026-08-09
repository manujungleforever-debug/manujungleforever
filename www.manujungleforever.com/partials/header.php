<?php
$rel = $rel ?? '';
$active_page = $active_page ?? '';
?>
<body>
<!-- GTM noscript -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5476BC9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>
<div id="preloader">
  <img src="../assets/img/logo.png" alt="Loading Manu Jungle Forever">
</div>
<script>
  (function(){
    var p = document.getElementById('preloader');
    // Mostrar solo una vez por sesion, o si hay un parametro "lang=" en la URL
    if(sessionStorage.getItem('mjf_loader_shown') === '1' && !window.location.search.includes('lang=')) {
      if(p) p.style.display = 'none';
    } else {
      sessionStorage.setItem('mjf_loader_shown', '1');
      window.addEventListener('load', function() {
        setTimeout(function() {
          if (p) {
            p.classList.add('loaded');
            setTimeout(function() { p.style.display = 'none'; }, 700);
          }
        }, 800); // Pequeña espera para que se vea la animacion
      });
    }
  })();
</script>

<header id="N"><div class="cx ni">
  <div class="nl"><a href="../index.html"><img src="../assets/img/logo.png" alt="<?php echo htmlspecialchars(SITE_NAME); ?>" loading="eager"></a></div>
  <nav class="nm" aria-label="Main navigation">
    <a href="../index.html" class="on">Home</a>
    <a href="../about-2/index.html">About Us</a>
    <a href="../departures/index.html">Departures</a>
    <a href="../news-and-gallery/index.html">Gallery</a>
    <a href="../blog/index.html">Blog</a>
    <div class="hd"><a href="../guided-tours/index.html">Guided Tours <i class="fas fa-caret-down"></i></a>
      <ul class="dm">
        <span class="dh"><i class="fas fa-binoculars"></i> WILDLIFE QUEST</span>
        <li><a href="../3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="../4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="../5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="../6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="../6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="../8-day-wildlife-photography-tour/index.html">Wildlife Photography &ndash; 8 Days</a></li>
        
        <span class="dh"><i class="fas fa-route"></i> RAINFOREST ROAD TRIP</span>
        <li><a href="../rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip Overview</a></li>
        <li><a href="../2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="../5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>

        <span class="dh"><i class="fas fa-campground"></i> AMAZON EXPEDITION</span>
        <li><a href="../5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="../6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
    <a href="../contact/index.html" class="nb">Book Now</a>
  </nav>
  <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false"><span class="bb"></span><span class="bb"></span><span class="bb"></span></button>
</div></header>

<div class="mo" id="mo" aria-hidden="true">
  <ul class="ml">
    <li><a href="<?= $rel ?>index.php">Home</a></li>
    <li>
      <button class="mb" id="mbt">Guided Tours <i class="fas fa-caret-down"></i></button>
      <ul class="md" id="mdd">
        <li><a href="<?= $rel ?>wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="<?= $rel ?>3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="<?= $rel ?>4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="<?= $rel ?>4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="<?= $rel ?>5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="<?= $rel ?>6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="<?= $rel ?>6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="<?= $rel ?>8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="<?= $rel ?>2-day-rainforest-road-trip/index.html">2-Day Road Trip</a></li>
        <li><a href="<?= $rel ?>5-day-rainforest-road-trip/index.html">5-Day Road Trip</a></li>
        <li><a href="<?= $rel ?>5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="<?= $rel ?>6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </li>
    <li><a href="<?= $rel ?>about-2/index.html">About Us</a></li>
    <li><a href="<?= $rel ?>departures/index.html">Departures</a></li>
    <li><a href="<?= $rel ?>news-and-gallery/index.html">Gallery</a></li>
    <li><a href="<?= $rel ?>blog/index.html">Blog</a></li>
    <li><a href="<?= $rel ?>contact/index.html">Contact</a></li>
  </ul>
</div>
