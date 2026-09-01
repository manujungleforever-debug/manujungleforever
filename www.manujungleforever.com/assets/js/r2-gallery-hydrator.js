document.addEventListener("DOMContentLoaded", () => {
  // Configuración de la galería R2 (Simulación de JSON endpoint para Cloudflare Pages)
  // En producción, esto podría venir de fetch('/api/gallery')
  const r2GalleryAssets = [
    // Videos (.mp4, .webm)
    "../assets/media_to_upload/videos/video_1.mp4",
    "../assets/media_to_upload/videos/video_2.mp4",
    "../assets/media_to_upload/videos/video_3.mp4",
    "../assets/media_to_upload/videos/video_4.mp4",
    "../assets/media_to_upload/videos/video_5.mp4",
    
    // Imágenes (.jpg, .webp, .png)
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg",
    "../assets/media_to_upload/photos/placeholder.jpg"
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

  const shuffledAssets = shuffleArray([...r2GalleryAssets]);
  
  // Contenedores del DOM
  const sliderWrapper = document.getElementById("r2-slider-wrapper");
  const bentoGrid = document.getElementById("r2-bento-grid");

  if (!sliderWrapper || !bentoGrid) return; // Salida segura

  // Función para determinar si es video o imagen
  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm)$/i);

  // Generador de elementos HTML
  const createElementHTML = (url, isSliderItem = false) => {
    let mediaEl;
    if (isVideo(url)) {
      mediaEl = `<video autoplay loop muted playsinline class="w-full h-full object-cover" ${!isSliderItem ? 'loading="lazy"' : ''}><source src="${url}" type="video/mp4"></video>`;
    } else {
      mediaEl = `<img src="${url}" class="w-full h-full object-cover" ${!isSliderItem ? 'loading="lazy"' : ''} alt="Jungle Media">`;
    }

    if (isSliderItem) {
      return `<div class="swiper-slide relative flex items-center justify-center bg-black">${mediaEl}<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div></div>`;
    } else {
      // Bento Grid Card
      return `
        <div class="bg-white/[0.02] border border-emerald-500/15 rounded-2xl overflow-hidden relative group backdrop-blur-sm cursor-pointer shadow-lg">
          <div class="w-full h-full transition-transform duration-700 group-hover:scale-105">
            ${mediaEl}
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60 group-hover:opacity-100 transition-opacity duration-500"></div>
          ${isVideo(url) ? '<div class="absolute top-4 right-4 bg-black/50 text-white rounded-full p-2 backdrop-blur-md"><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"></path></svg></div>' : ''}
        </div>
      `;
    }
  };

  // 1. Llenar el Hero Slider (3 primeros elementos)
  const sliderItems = shuffledAssets.slice(0, 3);
  sliderWrapper.innerHTML = sliderItems.map(url => createElementHTML(url, true)).join('');

  // 2. Llenar el Bento Grid (El resto de elementos)
  const bentoItems = shuffledAssets.slice(3);
  bentoGrid.innerHTML = bentoItems.map(url => createElementHTML(url, false)).join('');

  // 3. Inicializar Swiper.js (después de montar DOM)
  if (typeof Swiper !== 'undefined') {
    new Swiper('.top-hero-slider', {
      effect: 'fade', // Efecto premium fade o coverflow
      fadeEffect: { crossFade: true },
      loop: true,
      autoplay: {
        delay: 4000,
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
});
