(async function initGallery() {
  const dynamicGallery = document.getElementById('dynamic-r2-gallery');
  if (!dynamicGallery) return;

  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  const getEmptyStateHTML = () => `
    <div class="w-full flex flex-col items-center justify-center p-16 text-center border border-emerald-500/10 rounded-2xl bg-white/[0.01] my-8">
      <div class="w-20 h-20 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6">
        <svg class="w-10 h-10 text-emerald-500/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>
        </svg>
      </div>
      <h3 class="text-white text-2xl font-semibold mb-3">No multimedia files found in R2 bucket</h3>
      <p class="text-white/60 text-base max-w-md mx-auto">Please upload images or videos to the raiz/medios/gallery/imagenes/ or raiz/medios/gallery/videos/ directories in the Admin Panel.</p>
    </div>
  `;

  const createMediaHTML = (item) => {
    if (item.type === 'video') {
      return `
        <a href="${item.url}" class="glightbox relative group block mb-6 overflow-hidden rounded-2xl bg-black border border-emerald-500/20 shadow-2xl" data-gallery="r2-gallery" style="break-inside: avoid;">
          <video autoplay loop muted playsinline class="w-full h-auto object-cover transform transition-transform duration-700 group-hover:scale-105 opacity-90 group-hover:opacity-100">
            <source src="${item.url}" type="video/mp4">
          </video>
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
          <div class="absolute bottom-5 left-5 flex items-center gap-3">
            <span class="flex h-3.5 w-3.5 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500"></span>
            </span>
            <span class="text-white text-sm font-bold tracking-widest uppercase drop-shadow-md">Live Loop</span>
          </div>
          <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
             <svg class="w-14 h-14 text-white drop-shadow-xl scale-75 group-hover:scale-100 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path></svg>
          </div>
        </a>
      `;
    } else {
      return `
        <a href="${item.url}" class="glightbox relative group block mb-6 overflow-hidden rounded-2xl bg-white/[0.02] border border-emerald-500/10 shadow-lg" data-gallery="r2-gallery" style="break-inside: avoid;">
          <img src="${item.url}" class="w-full h-auto object-cover transform transition-transform duration-700 group-hover:scale-105" loading="lazy" alt="Amazon Wildlife">
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
          <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
             <svg class="w-12 h-12 text-white drop-shadow-md scale-75 group-hover:scale-100 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path></svg>
          </div>
        </a>
      `;
    }
  };

  try {
    dynamicGallery.innerHTML = '<div class="w-full text-center text-emerald-500 py-20"><i class="fas fa-spinner fa-spin text-5xl drop-shadow-[0_0_15px_rgba(45,212,191,0.5)]"></i></div>';

    const res = await fetch('/api/public-gallery');
    if (!res.ok) throw new Error('Failed to fetch media');
    const data = await res.json();
    const files = data.files || [];

    // FIXED ROUTES WITH 'raiz/' PREFIX MATCHING BUCKET STRUCTURE
    const images = files.filter(f => (f.key.startsWith('raiz/medios/gallery/imagenes/') || f.key.startsWith('medios/gallery/imagenes/')) && !f.key.endsWith('.keep_folder') && !isVideo(f.key)).map(f => f.url);
    const videos = files.filter(f => (f.key.startsWith('raiz/medios/gallery/videos/') || f.key.startsWith('medios/gallery/videos/')) && !f.key.endsWith('.keep_folder') && isVideo(f.key)).map(f => f.url);

    let allMedia = [
      ...images.map(url => ({ type: 'image', url })),
      ...videos.map(url => ({ type: 'video', url }))
    ];

    // Organic shuffle (Fisher-Yates)
    for (let i = allMedia.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [allMedia[i], allMedia[j]] = [allMedia[j], allMedia[i]];
    }

    if (allMedia.length === 0) {
      dynamicGallery.innerHTML = getEmptyStateHTML();
    } else {
      dynamicGallery.innerHTML = `
        <div class="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6 w-full px-4 md:px-0 mt-8 mb-24 mx-auto max-w-7xl">
          ${allMedia.map(item => createMediaHTML(item)).join('')}
        </div>
      `;

      if (typeof GLightbox !== 'undefined') {
        GLightbox({
          selector: '.glightbox',
          touchNavigation: true,
          loop: true,
          plyr: {
            config: {
              autoplay: true,
              muted: false,
            }
          }
        });
      }
    }
  } catch (error) {
    console.error("Gallery Hydrator Error: Fetch from /api/public-gallery failed.", error);

    const fallbackAssets = [
      { type: 'image', url: '/assets/media_to_upload/photos/placeholder.jpg' }
    ];

    dynamicGallery.innerHTML = `
      <div class="w-full mb-8 text-center"><p class="text-white/50 text-sm bg-red-500/10 inline-block px-4 py-2 rounded-full border border-red-500/20"><i class="fas fa-exclamation-triangle mr-2 text-red-400"></i>Live connection to Cloudflare R2 is currently down. Showing offline gallery.</p></div>
      <div class="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6 w-full px-4 md:px-0 mb-24 mx-auto max-w-7xl">
        ${fallbackAssets.map(item => createMediaHTML(item)).join('')}
      </div>
    `;

    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
    }
  }
})();