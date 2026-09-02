document.addEventListener('DOMContentLoaded', async () => {
  const imageGrid = document.getElementById('r2-image-grid');
  const videoSliderWrapper = document.getElementById('r2-video-slider');

  if (!imageGrid || !videoSliderWrapper) return;

  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  const getEmptyStateHTML = (type) => `
    <div class="col-span-full w-full flex flex-col items-center justify-center p-16 text-center border border-emerald-500/10 rounded-2xl bg-white/[0.01] my-8" style="break-inside: avoid;">
      <div class="w-20 h-20 rounded-full bg-emerald-500/10 flex items-center justify-center mb-6">
        <svg class="w-10 h-10 text-emerald-500/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
          ${type === 'video' 
            ? '<path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>' 
            : '<path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path>'}
        </svg>
      </div>
      <h3 class="text-white text-2xl font-semibold mb-3">Discovering New Captures</h3>
      <p class="text-white/60 text-base max-w-md mx-auto">Our team in the jungle is preparing amazing content. Check back soon!</p>
    </div>
  `;

  const createImageHTML = (url) => `
    <a href="${url}" class="glightbox relative group block mb-6 overflow-hidden rounded-2xl bg-white/[0.02] border border-emerald-500/10 shadow-lg" data-gallery="r2-gallery" style="break-inside: avoid;">
      <img src="${url}" class="w-full h-auto object-cover transform transition-transform duration-700 group-hover:scale-105" loading="lazy" alt="Amazon Wildlife">
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
      <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
         <svg class="w-12 h-12 text-white drop-shadow-md scale-75 group-hover:scale-100 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path></svg>
      </div>
    </a>
  `;

  const createVideoHTML = (url) => `
    <div class="swiper-slide relative flex items-center justify-center bg-black rounded-2xl overflow-hidden shadow-lg border border-emerald-500/10" style="aspect-ratio: 16/9;">
      <video autoplay loop muted playsinline class="w-full h-full object-cover">
        <source src="${url}" type="video/mp4">
      </video>
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none"></div>
      <div class="absolute bottom-5 left-5 flex items-center gap-3">
        <span class="flex h-3 w-3 relative">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
        <span class="text-white text-xs font-semibold tracking-wider uppercase">Live Loop</span>
      </div>
    </div>
  `;

  try {
    imageGrid.innerHTML = '<div class="col-span-full text-center text-emerald-500 py-20"><i class="fas fa-spinner fa-spin text-4xl"></i></div>';
    
    const res = await fetch('/api/media');
    if (!res.ok) throw new Error('Failed to fetch media');
    const data = await res.json();
    const files = data.files || [];

    // Extract photos strictly from 'medios/imagenes' and videos strictly from 'medios/videos'
    const images = files.filter(f => f.key.startsWith('medios/imagenes/') && !f.key.endsWith('.keep_folder') && !isVideo(f.key)).map(f => f.url);
    const videos = files.filter(f => f.key.startsWith('medios/videos/') && !f.key.endsWith('.keep_folder') && isVideo(f.key)).map(f => f.url);

    // Shuffle both arrays to make it organic
    const shuffleArray = (arr) => arr.sort(() => Math.random() - 0.5);
    shuffleArray(images);
    shuffleArray(videos);

    // 1. Render Images (Masonry)
    if (images.length === 0) {
      imageGrid.innerHTML = getEmptyStateHTML('image');
      imageGrid.className = 'w-full';
    } else {
      imageGrid.className = 'columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6 mb-16'; // Masonry layout
      imageGrid.innerHTML = images.map(url => createImageHTML(url)).join('');
      if (typeof GLightbox !== 'undefined') {
        GLightbox({ selector: '.glightbox', touchNavigation: true, loop: true });
      }
    }

    // 2. Render Videos (Swiper Fluid)
    if (videos.length === 0) {
      const swiperContainer = document.querySelector('.video-swiper-container');
      if (swiperContainer) swiperContainer.outerHTML = getEmptyStateHTML('video');
    } else {
      videoSliderWrapper.innerHTML = videos.map(url => createVideoHTML(url)).join('');
      if (typeof Swiper !== 'undefined') {
        new Swiper('.video-swiper-container', {
          effect: 'slide',
          loop: videos.length > 1,
          slidesPerView: 1.1,
          centeredSlides: true,
          spaceBetween: 20,
          autoplay: { delay: 4000, disableOnInteraction: false },
          breakpoints: {
            768: { slidesPerView: 1.5, spaceBetween: 30 },
            1024: { slidesPerView: 2.2, spaceBetween: 40 }
          }
        });
      }
    }
  } catch (error) {
    console.error("Gallery Hydrator Error:", error);
    imageGrid.innerHTML = `<div class="col-span-full text-center text-red-400 py-12">Failed to load media from Cloudflare R2.</div>`;
  }
});
