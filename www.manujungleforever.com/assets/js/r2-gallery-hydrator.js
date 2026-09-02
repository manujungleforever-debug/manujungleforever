(async function initMasonryMuseumWall() {
  const dynamicGallery = document.getElementById('dynamic-r2-gallery');
  if (!dynamicGallery) return;

  const isVideo = (key) => /\.(mp4|webm|mov)$/i.test(key);

  const renderEmptyState = () => `
    <div class="w-full flex flex-col items-center justify-center p-20 text-center border border-emerald-500/20 rounded-3xl bg-black/40 my-12 backdrop-blur-md">
      <div class="w-24 h-24 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6 border border-emerald-500/30">
        <svg class="w-12 h-12 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>
        </svg>
      </div>
      <h3 class="text-white text-3xl font-bold mb-3 tracking-wide">Gallery Matrix is Empty</h3>
      <p class="text-white/60 text-lg max-w-xl mx-auto">Upload media from the admin panel to populate this interactive museum wall.</p>
    </div>
  `;

  // ── Organic aspect ratio assignment ──
  const getAspectClass = (index) => {
    if (index % 7 === 0) return 'aspect-[4/5]';
    if (index % 5 === 0) return 'aspect-[3/4]';
    if (index % 4 === 0) return 'aspect-square';
    if (index % 3 === 0) return 'aspect-[16/9]';
    if (index % 2 === 0) return 'aspect-[16/10]';
    return 'aspect-[4/3]';
  };

  const cardBase = 'break-inside-avoid mb-3 inline-block w-full relative overflow-hidden rounded-xl bg-neutral-900 border border-emerald-500/20 group hover:border-emerald-500/60 transition-all duration-300';

  // ── Zoom overlay (shared by all card types) ──
  const zoomOverlay = (icon) => `
    <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-400 pointer-events-none"></div>
    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/30 backdrop-blur-[2px] pointer-events-none">
      <div class="w-12 h-12 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
        <i class="fas fa-${icon} text-sm"></i>
      </div>
    </div>
  `;

  // ── Single image card ──
  const renderImageCard = (url, index) => `
    <div class="${cardBase}">
      <a href="${url}" class="glightbox block w-full ${getAspectClass(index)}" data-gallery="museum-wall">
        <img src="${url}" class="w-full h-full object-cover transform transition-transform duration-500 group-hover:scale-105" loading="lazy" alt="Manu Jungle">
        ${zoomOverlay('search-plus')}
      </a>
    </div>
  `;

  // ── Video card ──
  const renderVideoCard = (url, index) => {
    const aspect = index % 2 === 0 ? 'aspect-[16/9]' : 'aspect-[3/4]';
    return `
      <div class="${cardBase} border-emerald-500/30">
        <a href="${url}" class="glightbox block w-full ${aspect}" data-gallery="museum-wall">
          <video autoplay loop muted playsinline class="w-full h-full object-cover"><source src="${url}" type="video/mp4"></video>
          <div class="absolute top-3 left-3 flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-full border border-emerald-500/40 z-10">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="text-white text-[10px] font-black tracking-wider uppercase">Live Stream</span>
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/10 to-transparent opacity-60 group-hover:opacity-30 transition-opacity duration-400"></div>
          ${zoomOverlay('play')}
        </a>
      </div>
    `;
  };

  // ── Crossfade slider card ──
  const renderSliderCard = (imageUrls, sliderId) => `
    <div class="${cardBase} border-emerald-500/30 aspect-[3/4]">
      <div class="absolute inset-0 w-full h-full">
        ${imageUrls.map((url, i) => `
          <div class="absolute inset-0 transition-opacity duration-1000 ease-in-out ${i === 0 ? 'opacity-100 z-10' : 'opacity-0 z-0'} slide-${sliderId}">
            <a href="${url}" class="glightbox block w-full h-full" data-gallery="slider-${sliderId}">
              <img src="${url}" class="w-full h-full object-cover" loading="lazy" alt="Manu Jungle Slider">
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-40"></div>
            </a>
          </div>
        `).join('')}
      </div>
      <div class="absolute top-3 left-3 flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-full border border-emerald-500/40 z-20">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-white text-[10px] font-black tracking-wider uppercase">Live Slider</span>
      </div>
      <div class="absolute bottom-3 right-3 z-20">
        <span class="bg-black/60 backdrop-blur-sm text-white/70 text-[10px] font-semibold px-2.5 py-1 rounded-full border border-white/10">${imageUrls.length} photos</span>
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

    // Separate media types
    const images = files.filter(f => !isVideo(f.key));
    const videos = files.filter(f => isVideo(f.key));

    // Build slider chunks from first images (groups of 3)
    const sliderChunks = [];
    const sliderPool = Math.min(images.length, 9);
    for (let i = 0; i < sliderPool; i += 3) {
      const chunk = images.slice(i, i + 3);
      if (chunk.length >= 2) sliderChunks.push(chunk);
    }
    const soloImages = images.slice(sliderPool);

    // ── Interleave all items into a single stream for organic mixing ──
    const allItems = [];

    // Sliders go first as anchor pieces
    sliderChunks.forEach((chunk, i) => {
      allItems.push({ type: 'slider', chunk, id: `sl-${i}` });
    });

    // Interleave solo images and videos organically
    let vIdx = 0;
    soloImages.forEach((img, i) => {
      allItems.push({ type: 'image', url: img.url });
      // Drop a video after every 2-3 images for organic dispersal
      if ((i + 1) % 3 === 0 && vIdx < videos.length) {
        allItems.push({ type: 'video', url: videos[vIdx].url });
        vIdx++;
      }
    });
    // Append any remaining videos
    while (vIdx < videos.length) {
      allItems.push({ type: 'video', url: videos[vIdx].url });
      vIdx++;
    }

    // ── Render the masonry stream ──
    let cards = '';
    allItems.forEach((item, index) => {
      if (item.type === 'slider') {
        cards += renderSliderCard(item.chunk.map(f => f.url), item.id);
      } else if (item.type === 'video') {
        cards += renderVideoCard(item.url, index);
      } else {
        cards += renderImageCard(item.url, index);
      }
    });

    const html = `
      <div class="w-full max-w-[120rem] mx-auto px-2 sm:px-4 mt-6 mb-32">
        <div class="flex items-center justify-between mb-8 px-2 border-b border-emerald-500/20 pb-4">
          <div class="flex items-center gap-3">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span class="text-sm uppercase tracking-widest text-emerald-400 font-bold">Amazon Museum Wall &bull; ${files.length} Assets</span>
          </div>
          <span class="text-xs text-white/50 tracking-wider hidden sm:inline">Click any piece to expand</span>
        </div>

        <div class="columns-2 sm:columns-3 md:columns-4 lg:columns-5 xl:columns-6 gap-3 space-y-3">
          ${cards}
        </div>
      </div>
    `;

    dynamicGallery.innerHTML = html;
    console.log('[Gallery] Museum wall rendered:', allItems.length, 'pieces');

    // ── Initialize GLightbox ──
    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
      console.log('[Gallery] GLightbox initialized');
    }

    // ── Activate crossfade sliders (3.5s interval) ──
    sliderChunks.forEach((chunk, i) => {
      const sliderId = `sl-${i}`;
      const slides = document.querySelectorAll(`.slide-${sliderId}`);
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