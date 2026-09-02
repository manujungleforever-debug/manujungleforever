document.addEventListener("DOMContentLoaded", () => {
  // Configuración de la galería R2 (Simulación de JSON endpoint para Cloudflare Pages)
  const r2GalleryAssets = [
    // Simular que el endpoint devuelve elementos (Para probar la galería, descomentar. Para probar empty state, dejar vacío o con .keep_folder)
    // "../assets/media_to_upload/videos/video_1.mp4",
    // "../assets/media_to_upload/photos/placeholder.jpg",
  ];

  // Algoritmo Fisher-Yates (Aleatoriedad Estricta solicitada)
  function shuffleArray(array) {
    let currentIndex = array.length, randomIndex;
    while (currentIndex !== 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
  }

  const shuffledAssets = shuffleArray([...r2GalleryAssets]).filter(url => !url.endsWith('.keep_folder'));
  
  // Contenedores del DOM
  const imageGrid = document.getElementById("r2-image-grid");
  const videoSliderWrapper = document.getElementById("r2-video-slider");

  if (!imageGrid || !videoSliderWrapper) return; // Salida segura

  // Función para determinar si es video o imagen
  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  // Template para Empty State (Placeholder Profesional)
  const getEmptyStateHTML = (type) => {
    return `
      <div class="col-span-full w-full flex flex-col items-center justify-center p-12 text-center border border-emerald-500/10 rounded-2xl bg-white/[0.01] my-8">
        <div class="w-16 h-16 rounded-full bg-emerald-500/10 flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-emerald-500/60" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
            ${type === 'video' 
              ? '<path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>' 
              : '<path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"></path>'}
          </svg>
        </div>
        <h3 class="text-white text-xl font-semibold mb-2">Descubriendo nuevas capturas</h3>
        <p class="text-white/60 text-sm max-w-md mx-auto">Nuestro equipo en la selva está preparando contenido increíble. Vuelve pronto para explorar la colección.</p>
      </div>
    `;
  };

  // Generador de elemento de Imagen (GLightbox Bento)
  const createImageHTML = (url) => {
    return `
      <a href="${url}" class="glightbox bg-white/[0.02] border border-emerald-500/15 rounded-2xl overflow-hidden relative group backdrop-blur-sm cursor-pointer shadow-lg h-full block" data-gallery="r2-gallery">
        <div class="w-full h-full transition-transform duration-700 group-hover:scale-105 flex">
          <img src="${url}" class="w-full h-full object-cover" loading="lazy" alt="Jungle Media">
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
           <svg class="w-10 h-10 text-white drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path></svg>
        </div>
      </a>
    `;
  };

  // Generador de elemento de Video (Swiper Slide)
  const createVideoHTML = (url) => {
    return `
      <div class="swiper-slide relative flex items-center justify-center bg-black w-full h-full">
        <video autoplay loop muted playsinline class="w-full h-full object-cover"><source src="${url}" type="video/mp4"></video>
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none"></div>
      </div>
    `;
  };

  // Separar imágenes y videos
  const images = shuffledAssets.filter(url => !isVideo(url));
  const videos = shuffledAssets.filter(url => isVideo(url));

  // 1. Renderizar Imágenes (con Empty State)
  if (images.length === 0) {
    imageGrid.innerHTML = getEmptyStateHTML('image');
    imageGrid.classList.remove('grid', 'grid-cols-1', 'md:grid-cols-3', 'lg:grid-cols-4');
  } else {
    imageGrid.innerHTML = images.map(url => createImageHTML(url)).join('');
    if (typeof GLightbox !== 'undefined') {
      GLightbox({
        selector: '.glightbox',
        touchNavigation: true,
        loop: true,
      });
    }
  }

  // 2. Renderizar Videos (con Empty State)
  if (videos.length === 0) {
    // Si no hay videos, reemplazamos todo el contenedor del swiper por el empty state
    const swiperContainer = document.querySelector('.video-swiper-container');
    if (swiperContainer) {
      swiperContainer.outerHTML = getEmptyStateHTML('video');
    }
  } else {
    videoSliderWrapper.innerHTML = videos.map(url => createVideoHTML(url)).join('');
    
    // Inicializar Swiper.js para Videos
    if (typeof Swiper !== 'undefined') {
      new Swiper('.video-swiper-container', {
        effect: 'slide',
        loop: true,
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
      });
    }
  }
});
