<?php
$rel = $rel ?? '';
$active_page = $active_page ?? '';
?>
<body>
<!-- GTM noscript -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5476BC9" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>

<header id="N">
  <div class="cx ni">
    <div class="nl">
      <a href="<?= $rel ?>index.php">
        <img src="<?= $rel ?>wp-content/uploads/2018/01/cropped-HiddenJungleCusco_Logo-1.png" alt="Hidden Jungle Cusco" width="190" height="54" loading="eager">
      </a>
    </div>
    
    <nav class="nm" aria-label="Main navigation">
      <a href="<?= $rel ?>index.php" class="<?= $active_page === 'home' ? 'on' : '' ?>">Home</a>
      
      <div class="hd">
        <a href="<?= $rel ?>guided-tours/index.html" class="<?= $active_page === 'tours' ? 'on' : '' ?>">Guided Tours <i class="fas fa-caret-down"></i></a>
        <ul class="dm">
          <li><a href="<?= $rel ?>wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
          <li><a href="<?= $rel ?>3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
          <li><a href="<?= $rel ?>4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
          <li><a href="<?= $rel ?>4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
          <li><a href="<?= $rel ?>5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
          <li><a href="<?= $rel ?>6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
          <li><a href="<?= $rel ?>6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
          <li><a href="<?= $rel ?>8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
          <li><a href="<?= $rel ?>rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
          <li><a href="<?= $rel ?>5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
          <li><a href="<?= $rel ?>6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
        </ul>
      </div>
      
      <a href="<?= $rel ?>about-2/index.html" class="<?= $active_page === 'about' ? 'on' : '' ?>">About Us</a>
      <a href="<?= $rel ?>departures/index.html" class="<?= $active_page === 'departures' ? 'on' : '' ?>">Departures</a>
      <a href="<?= $rel ?>news-and-gallery/index.html" class="<?= $active_page === 'gallery' ? 'on' : '' ?>">Gallery</a>
      <a href="<?= $rel ?>blog/index.html" class="<?= $active_page === 'blog' ? 'on' : '' ?>">Blog</a>
      <a href="<?= $rel ?>contact/index.html" class="nb">Book Now</a>
    </nav>
    
    <button class="bg" id="bg" aria-label="Toggle menu" aria-expanded="false">
      <span class="bb"></span>
      <span class="bb"></span>
      <span class="bb"></span>
    </button>
  </div>
</header>

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
