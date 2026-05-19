<?php
$rel = $rel ?? '';
$page_title = $page_title ?? 'Cusco Jungle &amp; Manu National Park Tours | Hidden Jungle Cusco';
$page_desc  = $page_desc  ?? 'Explore Cusco Jungle &amp; Manu National Park Tours with Hidden Jungle Cusco. Immerse yourself in wildlife, book your adventure now!';
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="<?= htmlspecialchars($page_desc) ?>">
<meta name="robots" content="index,follow,max-image-preview:large">
<title><?= htmlspecialchars($page_title) ?></title>

<!-- Open Graph -->
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="Hidden Jungle Cusco">
<meta property="og:title"       content="<?= htmlspecialchars($page_title) ?>">
<meta property="og:description" content="<?= htmlspecialchars($page_desc) ?>">
<meta property="og:url"         content="https://www.hiddenjunglecusco.com/">
<meta property="og:image"       content="https://www.hiddenjunglecusco.com/wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Visit-Manu-National-Park.jpg">
<meta name="twitter:card"       content="summary_large_image">

<!-- Canonical -->
<link rel="canonical" href="https://www.hiddenjunglecusco.com/">

<!-- Favicons -->
<link rel="icon"             href="<?= $rel ?>wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-32x32.png"   sizes="32x32">
<link rel="icon"             href="<?= $rel ?>wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="<?= $rel ?>wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-180x180.png">

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">

<!-- Site CSS (New Premium Dark-Mode) -->
<link rel="stylesheet" href="<?= $rel ?>assets/css/new.css">

<!-- Schema.org -->
<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
  {"@type":"TouristAttraction","name":"Hidden Jungle Cusco",
   "url":"https://www.hiddenjunglecusco.com/",
   "description":"Guided tours from Cusco to the Manu National Park in the Peruvian Amazon.",
   "image":"https://www.hiddenjunglecusco.com/wp-content/uploads/2020/10/Hidden-Jungle-Cusco-Visit-Manu-National-Park.jpg",
   "telephone":"+51979808013","email":"discover@hiddenjunglecusco.com",
   "address":{"@type":"PostalAddress","addressLocality":"Nuevo Eden","addressCountry":"PE"},
   "sameAs":["https://www.facebook.com/hiddenjunglecusco","https://www.instagram.com/hiddenjunglecusco/","https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html"]
  },
  {"@type":"WebSite","name":"Hidden Jungle Cusco","url":"https://www.hiddenjunglecusco.com/",
   "description":"What will you discover?",
   "potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https://www.hiddenjunglecusco.com/?s={search_term_string}"},"query-input":"required name=search_term_string"}
  }
]}
</script>

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-5476BC9');</script>
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GT-NS9ZNKJP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','GT-NS9ZNKJP');</script>
</head>
