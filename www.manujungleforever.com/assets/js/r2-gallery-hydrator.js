(async function initBentoMatrix() {
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
      <p class="text-white/60 text-lg max-w-xl mx-auto">Upload media from the admin panel to populate this interactive wall.</p>
    </div>
  `;

  // ── Determine bento span classes based on index ──
  const getSpanClasses = (index) => {
    if (index % 7 === 0) return 'col-span-2 row-span-2';   // Giant
    if (index % 9 === 0) return 'col-span-1 row-span-2';   // Vertical
    if (index % 5 === 0) return 'col-span-2 row-span-1';   // Landscape
    return 'col-span-1 row-span-1';                         // Normal
  };

  // ── Build a single image card ──
  const renderImageCard = (url, spanClasses) => `
    <div class="${spanClasses} relative overflow-hidden rounded-xl bg-neutral-900 border border-emerald-500/20 group hover:border-emerald-500/60 transition-all duration-300">
      <a href="${url}" class="glightbox block w-full h-full" data-gallery="bento-matrix">
        <img src="${url}" class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-110" loading="lazy" alt="Manu Jungle">
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-400"></div>
        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/30 backdrop-blur-[2px]">
          <div class="w-12 h-12 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
            <i class="fas fa-search-plus text-sm"></i>
          </div>
        </div>
      </a>
    </div>
  `;

  // ── Build a video card ──
  const renderVideoCard = (url, spanClasses) => `
    <div class="${spanClasses} relative overflow-hidden rounded-xl bg-neutral-900 border border-emerald-500/20 group hover:border-emerald-500/60 transition-all duration-300">
      <a href="${url}" class="glightbox block w-full h-full" data-gallery="bento-matrix">
        <video autoplay loop muted playsinline class="w-full h-full object-cover">
          <source src="${url}" type="video/mp4">
        </video>
        <div class="absolute top-3 left-3 flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-full border border-emerald-500/40 z-10">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-white text-[10px] font-black tracking-wider uppercase">Live Stream</span>
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/10 to-transparent opacity-60 group-hover:opacity-30 transition-opacity duration-400"></div>
        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/30 backdrop-blur-[2px]">
          <div class="w-14 h-14 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-xl">
            <i class="fas fa-play text-base ml-0.5"></i>
          </div>
        </div>
      </a>
    </div>
  `;

  // ── Build a crossfade slider card (giant cell) ──
  const renderSliderCard = (imageUrls, sliderId) => `
    <div class="col-span-2 row-span-2 relative overflow-hidden rounded-xl bg-neutral-900 border-2 border-emerald-500/30 group hover:border-emerald-500/60 transition-all duration-300">
      <div class="absolute inset-0 w-full h-full" id="${sliderId}">
        ${imageUrls.map((url, i) => `
          <div class="absolute inset-0 transition-opacity duration-1000 ease-in-out ${i === 0 ? 'opacity-100 z-10' : 'opacity-0 z-0'} slide-${sliderId}">
            <a href="${url}" class="glightbox block w-full h-full" data-gallery="bento-slider-${sliderId}">
              <img src="${url}" class="w-full h-full object-cover" loading="lazy" alt="Manu Jungle Slider">
              <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-50"></div>
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/30 backdrop-blur-[2px]">
                <div class="w-12 h-12 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
                  <i class="fas fa-search-plus text-sm"></i>
                </div>
              </div>
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

    // Separate images and videos
    const images = files.filter(f => !isVideo(f.key));
    const videos = files.filter(f => isVideo(f.key));

    // Build slider chunks from images (groups of 3)
    const sliderChunks = [];
    const sliderImageCount = Math.min(images.length, 9); // Use up to 9 images for sliders
    for (let i = 0; i < sliderImageCount; i += 3) {
      const chunk = images.slice(i, i + 3);
      if (chunk.length >= 2) sliderChunks.push(chunk);
    }
    const remainingImages = images.slice(sliderImageCount);

    // ── Assemble the grid ──
    let gridCells = '';
    let globalIndex = 0;

    // 1. Inject slider cells (each takes a giant 2x2 slot)
    sliderChunks.forEach((chunk, sIdx) => {
      gridCells += renderSliderCard(chunk.map(f => f.url), `slider-${sIdx}`);
      globalIndex++;
    });

    // 2. Inject video cells
    videos.forEach((vid) => {
      const span = getSpanClasses(globalIndex);
      // Videos get at minimum a 2-col span for impact
      const videoSpan = globalIndex % 7 === 0 ? 'col-span-2 row-span-2' : 'col-span-2 row-span-1';
      gridCells += renderVideoCard(vid.url, videoSpan);
      globalIndex++;
    });

    // 3. Inject remaining image cells with bento pattern
    remainingImages.forEach((img) => {
      const span = getSpanClasses(globalIndex);
      gridCells += renderImageCard(img.url, span);
      globalIndex++;
    });

    // ── Wrap everything ──
    const html = `
      <div class="w-full max-w-[120rem] mx-auto px-4 md:px-8 mt-6 mb-32">
        <div class="flex items-center justify-between mb-8 px-2 border-b border-emerald-500/20 pb-4">
          <div class="flex items-center gap-3">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span class="text-sm uppercase tracking-widest text-emerald-400 font-bold">Amazon Live Matrix &bull; ${files.length} Assets Active</span>
          </div>
          <span class="text-xs text-white/50 tracking-wider hidden sm:inline">Click any asset to expand</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 auto-rows-[220px] md:auto-rows-[260px] w-full">
          ${gridCells}
        </div>
      </div>
    `;

    dynamicGallery.innerHTML = html;
    console.log('[Gallery] Matrix rendered:', globalIndex, 'cells');

    // ── Initialize GLightbox ──
    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
      console.log('[Gallery] GLightbox initialized');
    }

    // ── Activate crossfade sliders ──
    sliderChunks.forEach((chunk, sIdx) => {
      const sliderId = `slider-${sIdx}`;
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