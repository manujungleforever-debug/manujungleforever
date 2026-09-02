(async function initMassiveSliderMatrix() {
  const dynamicGallery = document.getElementById('dynamic-r2-gallery');
  if (!dynamicGallery) return;

  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  const renderEmptyState = () => `
    <div class="w-full flex flex-col items-center justify-center p-20 text-center border border-emerald-500/20 rounded-3xl bg-black/40 my-12 backdrop-blur-md">
      <div class="w-24 h-24 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6 border border-emerald-500/30">
        <svg class="w-12 h-12 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>
        </svg>
      </div>
      <h3 class="text-white text-3xl font-bold mb-3 tracking-wide">Gallery Matrix is Empty</h3>
      <p class="text-white/60 text-lg max-w-xl mx-auto">Upload media items from your admin panel to instantly populate this massive interactive wall.</p>
    </div>
  `;

  try {
    dynamicGallery.innerHTML = '<div class="w-full text-center text-emerald-400 py-36"><i class="fas fa-circle-notch fa-spin text-6xl"></i><p class="text-white/60 text-base mt-4 tracking-wider uppercase font-semibold">Synchronizing Massive R2 Matrix...</p></div>';

    const res = await fetch('/api/media/gallery');
    if (!res.ok) throw new Error('API request failed');

    const data = await res.json();
    const files = data.files || [];
    console.log('[Gallery] Files received from API:', files.length);

    if (files.length === 0) {
      dynamicGallery.innerHTML = renderEmptyState();
      return;
    }

    // Separamos imágenes y videos para armar tanto sliders dinámicos como celdas colosales
    const images = files.filter(f => !isVideo(f.key));
    const videos = files.filter(f => isVideo(f.key));

    // Dividimos las imágenes en bloques de 3 o 4 para crear los Sliders Automáticos Interactivos
    const sliderChunks = [];
    for (let i = 0; i < images.length; i += 3) {
      sliderChunks.push(images.slice(i, i + 3));
    }

    let htmlContent = `
      <div class="w-full px-4 md:px-8 mt-6 mb-32 mx-auto">
        <div class="flex items-center justify-between mb-8 px-4 border-b border-emerald-500/20 pb-4">
          <div class="flex items-center gap-3">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span class="text-sm uppercase tracking-widest text-emerald-400 font-bold">Amazon Live Matrix &bull; ${files.length} Assets Active</span>
          </div>
          <span class="text-xs text-white/50 tracking-wider">Dynamic Sliders & Expanded Bento Grid Enabled</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 w-full">
    `;

    // 1. Inyectamos Sliders Automáticos si hay suficientes imágenes
    sliderChunks.forEach((chunk, sIndex) => {
      const sliderId = `auto-slider-${sIndex}`;
      htmlContent += `
        <div class="col-span-1 sm:col-span-2 row-span-2 relative group overflow-hidden rounded-2xl bg-black border-2 border-emerald-500/30 shadow-2xl min-h-[320px] md:min-h-[420px]">
          <div class="absolute inset-0 w-full h-full" id="${sliderId}">
            ${chunk.map((img, imgIdx) => `
              <div class="absolute inset-0 transition-opacity duration-1000 ease-in-out ${imgIdx === 0 ? 'opacity-100 z-10' : 'opacity-0 z-0'} slider-slide-${sIndex}">
                <a href="${img.url}" class="glightbox block w-full h-full relative group/item" data-gallery="matrix-slider-${sIndex}">
                  <img src="${img.url}" class="w-full h-full object-cover transform transition-transform duration-700 group-hover/item:scale-105" loading="lazy" alt="Manu Jungle Slider">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60"></div>
                  <div class="absolute bottom-4 left-4 right-4 flex items-center justify-between">
                    <span class="bg-emerald-500/90 text-black text-xs font-black px-3 py-1 rounded-full uppercase tracking-widest shadow-lg">Live Slider [${imgIdx + 1}/${chunk.length}]</span>
                    <div class="w-10 h-10 rounded-full bg-black/60 backdrop-blur-md text-emerald-400 border border-emerald-500/40 flex items-center justify-center opacity-0 group-hover/item:opacity-100 transition-opacity">
                      <i class="fas fa-search-plus text-sm"></i>
                    </div>
                  </div>
                </a>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    });

    // 2. Inyectamos el resto de imágenes sueltas en formato colosal
    images.slice(sliderChunks.length * 3).forEach((img, idx) => {
      const isLarge = (idx % 3 === 0);
      const spanClasses = isLarge ? 'sm:col-span-2 sm:row-span-2 min-h-[320px] md:min-h-[420px]' : 'min-h-[240px] md:min-h-[300px]';

      htmlContent += `
        <div class="${spanClasses} relative group overflow-hidden rounded-2xl bg-black border border-emerald-500/20 shadow-xl transition-all duration-500 hover:scale-[1.02] hover:border-emerald-400 hover:z-30">
          <a href="${img.url}" class="glightbox block w-full h-full relative" data-gallery="r2-grid">
            <img src="${img.url}" class="w-full h-full object-cover transform transition-transform duration-700 group-hover:scale-110 opacity-90 group-hover:opacity-100" loading="lazy" alt="Manu Jungle Gallery">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 backdrop-blur-[3px]">
              <div class="w-14 h-14 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-2xl transform scale-75 group-hover:scale-100 transition-transform duration-300">
                <i class="fas fa-search-plus text-lg font-bold"></i>
              </div>
            </div>
          </a>
        </div>
      `;
    });

    // 3. Inyectamos los Videos en tarjetas masivas con reproducción en bucle
    videos.forEach((vid) => {
      htmlContent += `
        <div class="col-span-1 sm:col-span-2 row-span-2 relative group overflow-hidden rounded-2xl bg-black border-2 border-emerald-500/40 shadow-2xl min-h-[320px] md:min-h-[420px]">
          <a href="${vid.url}" class="glightbox block w-full h-full relative" data-gallery="r2-grid">
            <video autoplay loop muted playsinline class="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity duration-500">
              <source src="${vid.url}" type="video/mp4">
            </video>
            <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-70 group-hover:opacity-40 transition-opacity"></div>
            <div class="absolute top-4 left-4 flex items-center gap-2 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-full border border-emerald-500/40">
              <span class="flex h-3 w-3 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
              <span class="text-white text-xs font-black tracking-wider uppercase">Live Stream</span>
            </div>
            <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40 backdrop-blur-[2px]">
              <div class="w-14 h-14 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-2xl">
                <i class="fas fa-play text-lg font-bold ml-1"></i>
              </div>
            </div>
          </a>
        </div>
      `;
    });

    htmlContent += `
        </div>
      </div>
    `;

    dynamicGallery.innerHTML = htmlContent;

    // Inicializamos GLightbox para el zoom en pantalla completa
    if (typeof GLightbox !== 'undefined') {
      GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
    }

    // Activamos los motores de cambio automático (Sliders Automáticos cada 4 segundos)
    sliderChunks.forEach((chunk, sIndex) => {
      let currentIndex = 0;
      const slides = document.querySelectorAll(`.slider-slide-${sIndex}`);
      if (slides.length > 1) {
        setInterval(() => {
          slides[currentIndex].classList.remove('opacity-100', 'z-10');
          slides[currentIndex].classList.add('opacity-0', 'z-0');

          currentIndex = (currentIndex + 1) % slides.length;

          slides[currentIndex].classList.remove('opacity-0', 'z-0');
          slides[currentIndex].classList.add('opacity-100', 'z-10');
        }, 4000); // Rota cada 4 segundos de forma suave
      }
    });

  } catch (err) {
    console.error("[Gallery] Initialization error:", err);
    dynamicGallery.innerHTML = renderEmptyState();
  }
})();