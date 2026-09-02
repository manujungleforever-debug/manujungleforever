(async function initMassiveGallery() {
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

  // Genera elementos con una densidad visual masiva (estilo muro interactivo)
  const createMediaHTML = (item, index) => {
    // Da variaciones orgánicas de tamaño simulando un bento avanzado si hay muchos elementos
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
            <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 backdrop-blur-[2px]">
              <div class="w-12 h-12 rounded-full bg-emerald-500/90 text-black flex items-center justify-center shadow-lg transform scale-75 group-hover:scale-100 transition-transform duration-300">
                <i class="fas fa-play text-sm ml-0.5"></i>
              </div>
            </div>
          </div>
        </a>
      `;
    } else {
      return `
        <a href="${item.url}" class="glightbox relative group block overflow-hidden rounded-xl bg-white/[0.02] border border-emerald-500/20 shadow-lg transition-all duration-500 hover:scale-[1.02] hover:border-emerald-400 hover:z-20 ${spanClasses}" data-gallery="r2-gallery" style="break-inside: avoid;">
          <div class="relative w-full h-full min-h-[160px] max-h-[350px]">
            <img src="${item.url}" class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-110 opacity-90 group-hover:opacity-100" loading="lazy" alt="Manu Jungle Gallery Item">
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
  };

  try {
    dynamicGallery.innerHTML = '<div class="w-full text-center text-emerald-500 py-32"><i class="fas fa-spinner fa-spin text-5xl drop-shadow-[0_0_15px_rgba(45,212,191,0.5)]"></i><p class="text-white/50 text-sm mt-4">Loading massive multimedia matrix...</p></div>';

    const res = await fetch('/api/public-gallery');
    if (!res.ok) throw new Error('Failed to fetch media');
    const data = await res.json();
    const files = data.files || [];

    // Captura estricta con prefijos raiz/ o rutas directas
    const images = files.filter(f => (f.key.startsWith('raiz/medios/gallery/imagenes/') || f.key.startsWith('medios/gallery/imagenes/')) && !f.key.endsWith('.keep_folder') && !isVideo(f.key)).map(f => f.url);
    const videos = files.filter(f => (f.key.startsWith('raiz/medios/gallery/videos/') || f.key.startsWith('medios/gallery/videos/')) && !f.key.endsWith('.keep_folder') && isVideo(f.key)).map(f => f.url);

    let allMedia = [
      ...images.map(url => ({ type: 'image', url })),
      ...videos.map(url => ({ type: 'video', url }))
    ];

    // Mezcla orgánica de elementos
    for (let i = allMedia.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [allMedia[i], allMedia[j]] = [allMedia[j], allMedia[i]];
    }

    if (allMedia.length === 0) {
      dynamicGallery.innerHTML = getEmptyStateHTML();
    } else {
      // Muro masivo con columnas densas (hasta 5 columnas en pantallas grandes para lograr el efecto de muro lleno de contenido)
      dynamicGallery.innerHTML = `
        <div class="w-full px-2 md:px-0 mt-4 mb-24 mx-auto max-w-[95rem]">
          <div class="flex items-center justify-between mb-6 px-2">
            <span class="text-xs uppercase tracking-widest text-emerald-400 font-semibold"><i class="fas fa-th mr-2"></i>Interactive Amazon Matrix (${allMedia.length} items loaded)</span>
            <span class="text-xs text-white/40">Click any asset to expand</span>
          </div>
          <div class="columns-2 sm:columns-3 md:columns-4 lg:columns-5 gap-4 space-y-4 w-full">
            ${allMedia.map((item, idx) => createMediaHTML(item, idx)).join('')}
          </div>
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
    console.error("Gallery Hydrator Error:", error);

    // Fallback con múltiples elementos simulados para que no se vea vacío ni triste ante un fallo de red
    const fallbackAssets = Array(12).fill(0).map(() => ({ type: 'image', url: '/assets/media_to_upload/photos/placeholder.jpg' }));

    dynamicGallery.innerHTML = `
      <div class="w-full mb-8 text-center"><p class="text-white/50 text-sm bg-red-500/10 inline-block px-4 py-2 rounded-full border border-red-500/20"><i class="fas fa-exclamation-triangle mr-2 text-red-400"></i>Live connection to Cloudflare R2 is down. Showing offline matrix backup.</p></div>
      <div class="columns-2 sm:columns-3 md:columns-4 lg:columns-5 gap-4 space-y-4 w-full px-2 max-w-[95rem] mx-auto mb-24">
        ${fallbackAssets.map((item, idx) => createMediaHTML(item, idx)).join('')}
      </div>
    `;

    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
    }
  }
})();