(async function initCollectionWall() {
  const dynamicGallery = document.getElementById('dynamic-r2-gallery');
  if (!dynamicGallery) return;

  const isVideo = (key) => /\.(mp4|webm|mov)$/i.test(key);

  // ── 1. Fetch JSON attributions to match Home page exactly ──
  let attributionsMap = {};
  try {
    const res = await fetch('/data/attributions.json?t=' + Date.now(), { cache: 'no-store' });
    if (res.ok) {
      const list = await res.json();
      if (Array.isArray(list)) {
        list.forEach(item => {
          if (item && item.filename && item.attribution) {
            attributionsMap[item.filename.toLowerCase()] = item.attribution;
          }
        });
      }
    }
  } catch (e) {
    console.warn('Failed to load attributions.json', e);
  }

  // ── 2. Credit logic (combining API customMetadata + JSON) ──
  const getRawCredit = (file) => {
    // Check API metadata first
    if (file.credit || file.author || file.copyright) {
      return file.credit || file.author || file.copyright;
    }
    // Fallback to JSON attributions based on filename
    const filename = file.key.split('/').pop().toLowerCase();
    const jsonMeta = attributionsMap[filename];
    if (jsonMeta && jsonMeta.author) {
      return jsonMeta.author;
    }
    return '';
  };

  const formatCredit = (file) => {
    const raw = getRawCredit(file);
    if (!raw) return '';
    if (raw.includes('CC BY')) return raw;
    return `Photo: ${raw} · CC BY-SA 4.0`;
  };

  const glightboxAttrs = (file) => {
    const credit = formatCredit(file);
    if (!credit) return 'data-gallery="manu-collection"';
    const safe = credit.replace(/"/g, '&quot;');
    return `data-gallery="manu-collection" data-description="<div class='text-center text-xs text-neutral-300 font-sans py-1'><i class='fas fa-camera text-emerald-400 mr-1.5'></i> ${safe}</div>"`;
  };

  const creditBadge = (file) => {
    const credit = formatCredit(file);
    if (!credit) return '';
    return `<div class="absolute bottom-2 right-2 z-20 pointer-events-none inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-[10px] text-white/80 font-sans shadow-md"><span>${credit}</span></div>`;
  };

  const renderEmptyState = () => `
    <div class="w-full flex flex-col items-center justify-center p-20 text-center border border-emerald-500/20 rounded-3xl bg-black/40 my-12 backdrop-blur-md">
      <div class="w-24 h-24 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6 border border-emerald-500/30">
        <svg class="w-12 h-12 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>
        </svg>
      </div>
      <h3 class="text-white text-3xl font-bold mb-3">Gallery Matrix is Empty</h3>
      <p class="text-white/60 text-lg max-w-xl mx-auto">Upload media from the admin panel to populate this wall.</p>
    </div>
  `;

  // ── Organic size pattern: mix of horizontal, vertical, giant, and normal ──
  // H = horizontal wide (2col x 1row), V = vertical tall (1col x 2row),
  // G = giant (2col x 2row), N = normal square (1col x 1row)
  const sizePattern = ['G', 'N', 'H', 'V', 'N', 'N', 'H', 'N', 'V', 'N', 'H', 'N', 'G', 'N', 'V', 'H', 'N', 'N', 'N', 'V', 'H', 'N', 'N', 'G'];

  const getSpan = (index) => {
    const size = sizePattern[index % sizePattern.length];
    switch (size) {
      case 'G': return 'col-span-2 row-span-2';  // Giant square
      case 'H': return 'col-span-2 row-span-1';  // Horizontal landscape
      case 'V': return 'col-span-1 row-span-2';  // Vertical portrait
      default:  return 'col-span-1 row-span-1';  // Normal
    }
  };

  const cardBase = 'relative overflow-hidden rounded-xl bg-neutral-900 border border-emerald-500/20 group hover:border-emerald-500/60 hover:shadow-[0_0_25px_rgba(16,185,129,0.15)] transition-all duration-300';

  const zoomOverlay = (icon) => `
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
      <div class="w-11 h-11 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
        <i class="fas fa-${icon} text-xs"></i>
      </div>
    </div>
  `;

  // ── Card renderers (credits handled natively) ──
  const renderImageCard = (url, span, file) => `
    <div class="${span} ${cardBase}">
      <a href="${url}" class="glightbox block w-full h-full" ${glightboxAttrs(file)}>
        <img src="${url}" class="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-105" loading="lazy" alt="Manu Jungle">
        ${zoomOverlay('search-plus')}
      </a>
      ${creditBadge(file)}
    </div>
  `;

  const renderVideoCard = (url, span, file) => `
    <div class="${span} ${cardBase} border-emerald-500/30">
      <a href="${url}" class="glightbox block w-full h-full" ${glightboxAttrs(file)}>
        <video autoplay loop muted playsinline class="w-full h-full object-cover"><source src="${url}" type="video/mp4"></video>
        <div class="absolute top-3 left-3 flex items-center gap-2 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-full border border-emerald-500/40 z-10">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-white text-[10px] font-black tracking-wider uppercase">Live Stream</span>
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent opacity-50 group-hover:opacity-20 transition-opacity duration-300"></div>
        ${zoomOverlay('play')}
      </a>
      ${creditBadge(file)}
    </div>
  `;

  const renderSliderCard = (sliderFiles, sliderId, span) => `
    <div class="${span} ${cardBase} border-emerald-500/30">
      <div class="absolute inset-0 w-full h-full">
        ${sliderFiles.map((file, i) => `
          <div class="absolute inset-0 transition-opacity duration-1000 ease-in-out ${i === 0 ? 'opacity-100 z-10' : 'opacity-0 z-0'} slide-${sliderId}">
            <a href="${file.url}" class="glightbox block w-full h-full" ${glightboxAttrs(file)}>
              <img src="${file.url}" class="w-full h-full object-cover" loading="lazy" alt="Manu Jungle">
            </a>
          </div>
        `).join('')}
      </div>
      <div class="absolute top-3 left-3 flex items-center gap-2 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-full border border-emerald-500/40 z-20">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-white text-[10px] font-black tracking-wider uppercase">Live Slider</span>
      </div>
      <div class="absolute bottom-3 right-3 z-20">
        <span class="bg-black/50 backdrop-blur-sm text-white/70 text-[10px] font-semibold px-2 py-0.5 rounded-full">${sliderFiles.length} photos</span>
      </div>
      ${zoomOverlay('search-plus')}
    </div>
  `;

  try {
    dynamicGallery.innerHTML = '<div class="w-full text-center text-emerald-400 py-36"><i class="fas fa-circle-notch fa-spin text-6xl"></i><p class="text-white/60 text-base mt-4 tracking-wider uppercase font-semibold">Synchronizing R2 Matrix...</p></div>';

    const res = await fetch('/api/media/gallery');
    console.log('[Gallery] API status:', res.status);
    if (!res.ok) throw new Error('API response ' + res.status);

    const data = await res.json();
    const files = data.files || [];
    console.log('[Gallery] Files received:', files.length);

    if (files.length === 0) {
      dynamicGallery.innerHTML = renderEmptyState();
      return;
    }

    const images = files.filter(f => !isVideo(f.key));
    const videos = files.filter(f => isVideo(f.key));

    // ── Dynamic slider count: 1 slider per every 5 images (scales with content) ──
    const sliderCount = Math.max(1, Math.floor(images.length / 5));
    const imagesPerSlider = 3;
    const sliderPool = sliderCount * imagesPerSlider;
    const sliderChunks = [];
    for (let i = 0; i < sliderPool && i < images.length; i += imagesPerSlider) {
      const chunk = images.slice(i, i + imagesPerSlider);
      if (chunk.length >= 2) sliderChunks.push(chunk);
    }
    const soloImages = images.slice(sliderPool);
    console.log('[Gallery] Sliders:', sliderChunks.length, '| Solo images:', soloImages.length, '| Videos:', videos.length);

    // ── Build the organic interleaved stream ──
    const stream = [];
    let imgIdx = 0, vidIdx = 0, sliderIdx = 0;

    // Total items to place
    const totalItems = sliderChunks.length + soloImages.length + videos.length;

    for (let i = 0; i < totalItems; i++) {
      // Place sliders at positions that get Giant (G) or Vertical (V) spans for visual impact
      const currentSize = sizePattern[i % sizePattern.length];
      if ((currentSize === 'G') && sliderIdx < sliderChunks.length) {
        stream.push({ type: 'slider', idx: sliderIdx });
        sliderIdx++;
      } else if ((currentSize === 'H' || currentSize === 'G') && vidIdx < videos.length) {
        // Videos look best in horizontal or giant slots
        stream.push({ type: 'video', url: videos[vidIdx].url, file: videos[vidIdx] });
        vidIdx++;
      } else if (imgIdx < soloImages.length) {
        stream.push({ type: 'image', url: soloImages[imgIdx].url, file: soloImages[imgIdx] });
        imgIdx++;
      } else if (vidIdx < videos.length) {
        stream.push({ type: 'video', url: videos[vidIdx].url, file: videos[vidIdx] });
        vidIdx++;
      } else if (sliderIdx < sliderChunks.length) {
        stream.push({ type: 'slider', idx: sliderIdx });
        sliderIdx++;
      }
    }

    // ── Render all cards ──
    let cards = '';
    stream.forEach((item, index) => {
      const span = getSpan(index);
      if (item.type === 'slider') {
        cards += renderSliderCard(sliderChunks[item.idx], `sl-${item.idx}`, span);
      } else if (item.type === 'video') {
        cards += renderVideoCard(item.url, span, item.file);
      } else {
        cards += renderImageCard(item.url, span, item.file);
      }
    });

    dynamicGallery.innerHTML = `
      <div class="w-full max-w-[120rem] mx-auto px-2 sm:px-4 mt-6 mb-32">
        <div class="flex items-center justify-between mb-8 px-2 border-b border-emerald-500/20 pb-4">
          <div class="flex items-center gap-3">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span class="text-sm uppercase tracking-widest text-emerald-400 font-bold">Amazon Collection Wall &bull; ${files.length} Assets</span>
          </div>
          <span class="text-xs text-white/50 tracking-wider hidden sm:inline">Click any piece to expand</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 auto-rows-[160px] sm:auto-rows-[180px] md:auto-rows-[200px] gap-3" style="grid-auto-flow: dense;">
          ${cards}
        </div>
      </div>
    `;

    console.log('[Gallery] Collection wall rendered:', stream.length, 'pieces');

    // ── GLightbox ──
    if (typeof GLightbox !== 'undefined') {
      GLightbox({
        selector: '.glightbox',
        touchNavigation: true,
        loop: true,
        zoomable: true,
        draggable: true
      });
    }

    // ── Activate all crossfade sliders ──
    sliderChunks.forEach((chunk, i) => {
      const slides = document.querySelectorAll(`.slide-sl-${i}`);
      if (slides.length <= 1) return;
      let current = 0;
      setInterval(() => {
        slides[current].classList.remove('opacity-100', 'z-10');
        slides[current].classList.add('opacity-0', 'z-0');
        current = (current + 1) % slides.length;
        slides[current].classList.remove('opacity-0', 'z-0');
        slides[current].classList.add('opacity-100', 'z-10');
      }, 3500);
    });
    console.log('[Gallery] Sliders activated:', sliderChunks.length);

  } catch (err) {
    console.error('[Gallery] FATAL error:', err);
    dynamicGallery.innerHTML = renderEmptyState();
  }
})();