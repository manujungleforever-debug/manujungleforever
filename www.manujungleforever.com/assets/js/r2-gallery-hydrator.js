(async function initDynamicR2Matrix() {
  const dynamicGallery = document.getElementById('dynamic-r2-gallery');
  if (!dynamicGallery) return;

  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  const renderEmptyState = () => `
    <div class="w-full flex flex-col items-center justify-center p-16 text-center border border-emerald-500/10 rounded-2xl bg-white/[0.01] my-8">
      <div class="w-20 h-20 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6">
        <svg class="w-10 h-10 text-emerald-500/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>
        </svg>
      </div>
      <h3 class="text-white text-2xl font-semibold mb-3">Gallery is currently empty</h3>
      <p class="text-white/60 text-base max-w-md mx-auto">Upload images or videos through the admin panel, and they will automatically appear in this massive matrix.</p>
    </div>
  `;

  const renderGrid = (items) => {
    return `
      <div class="w-full px-2 md:px-0 mt-4 mb-24 mx-auto max-w-[95rem]">
        <div class="flex items-center justify-between mb-6 px-2">
          <span class="text-xs uppercase tracking-widest text-emerald-400 font-semibold"><i class="fas fa-th mr-2"></i>Amazon Live Matrix (${items.length} items loaded)</span>
          <span class="text-xs text-white/40">Click any asset to expand</span>
        </div>
        <div class="columns-2 sm:columns-3 md:columns-4 lg:columns-5 gap-4 space-y-4 w-full">
          ${items.map((item, index) => {
      const spanClasses = (index % 7 === 0) ? 'sm:col-span-2 sm:row-span-2' : '';
      if (item.type === 'video') {
        return `
                <a href="${item.url}" class="glightbox relative group block overflow-hidden rounded-xl bg-black border border-emerald-500/30 shadow-2xl transition-all duration-500 hover:scale-[1.02] hover:border-emerald-400 hover:z-20 ${spanClasses}" data-gallery="r2-gallery" style="break-inside: avoid;">
                  <div class="relative w-full h-full min-h-[180px] max-h-[350px]">
                    <video autoplay loop muted playsinline class="w-full h-full object-cover opacity-85 group-hover:opacity-100 transition-opacity duration-500">
                      <source src="${item.url}" type="video/mp4">
                    </video>
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 group-hover:opacity-30 transition-opacity duration-500"></div>
                    <div class="absolute bottom-3 left-3 flex items-center gap-2 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-full border border-emerald-500/20">
                      <span class="flex h-2.5 w-2.5 relative">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                      </span>
                      <span class="text-white text-xs font-bold tracking-wider uppercase">Live</span>
                    </div>
                  </div>
                </a>
              `;
      } else {
        return `
                <a href="${item.url}" class="glightbox relative group block overflow-hidden rounded-xl bg-white/[0.02] border border-emerald-500/20 shadow-lg transition-all duration-500 hover:scale-[1.02] hover:border-emerald-400 hover:z-20 ${spanClasses}" data-gallery="r2-gallery" style="break-inside: avoid;">
                  <div class="relative w-full h-full min-h-[160px] max-h-[350px]">
                    <img src="${item.url}" class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-110 opacity-90 group-hover:opacity-100" loading="lazy" alt="Manu Jungle Gallery">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 backdrop-blur-[2px]">
                      <div class="w-12 h-12 rounded-full bg-emerald-500/90 text-black flex items-center justify-center shadow-lg transform scale-75 group-hover:scale-100 transition-transform duration-300">
                        <i class="fas fa-search-plus text-sm"></i>
                      </div>
                    </div>
                  </div>
                </a>
              `;
      }
    }).join('')}
        </div>
      </div>
    `;
  };

  try {
    dynamicGallery.innerHTML = '<div class="w-full text-center text-emerald-500 py-32"><i class="fas fa-spinner fa-spin text-5xl"></i><p class="text-white/50 text-sm mt-4">Connecting to R2 Bucket...</p></div>';

    const res = await fetch('/api/media/gallery');
    console.log('[Gallery] API status:', res.status);
    if (!res.ok) throw new Error('API response ' + res.status);

    const data = await res.json();
    const files = data.files || [];
    console.log('[Gallery] Files received from API:', files.length, files);

    // Backend already filters .keep_folder and empty objects — map directly
    const mappedItems = files.map(f => ({
      type: isVideo(f.key) ? 'video' : 'image',
      url: f.url
    }));

    console.log('[Gallery] Mapped items:', mappedItems.length);

    if (mappedItems.length === 0) {
      dynamicGallery.innerHTML = renderEmptyState();
    } else {
      dynamicGallery.innerHTML = renderGrid(mappedItems);
      if (typeof GLightbox !== 'undefined') {
        GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
      }
    }
  } catch (err) {
    console.error('[Gallery] FATAL fetch error:', err);
    dynamicGallery.innerHTML = renderEmptyState();
  }
})();