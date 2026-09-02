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

  const shuffledAssets = shuffleArray([...r2GalleryAssets]).filter(url => !url.endsWith('.keep_folder'));
  
  // Contenedores del DOM
  const imageGrid = document.getElementById("r2-image-grid");
  const videoGrid = document.getElementById("r2-video-grid");

  if (!imageGrid || !videoGrid) return; // Salida segura

  // Función para determinar si es video o imagen
  const isVideo = (url) => url.toLowerCase().match(/\.(mp4|webm|mov)$/i);

  // Generador de elementos HTML
  const createElementHTML = (url) => {
    let mediaEl;
    if (isVideo(url)) {
      mediaEl = `<video autoplay loop muted playsinline class="w-full h-full object-cover" loading="lazy"><source src="${url}" type="video/mp4"></video>`;
    } else {
      mediaEl = `<img src="${url}" class="w-full h-full object-cover" loading="lazy" alt="Jungle Media">`;
    }

    // Bento Grid Card
    return `
      <div class="bg-white/[0.02] border border-emerald-500/15 rounded-2xl overflow-hidden relative group backdrop-blur-sm cursor-pointer shadow-lg h-full">
        <div class="w-full h-full transition-transform duration-700 group-hover:scale-105 flex">
          ${mediaEl}
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        ${isVideo(url) ? '<div class="absolute top-4 right-4 bg-black/50 text-white rounded-full p-2 backdrop-blur-md pointer-events-none"><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"></path></svg></div>' : ''}
      </div>
    `;
  };

  // Separar imágenes y videos
  const images = shuffledAssets.filter(url => !isVideo(url));
  const videos = shuffledAssets.filter(url => isVideo(url));

  // Llenar contenedores
  imageGrid.innerHTML = images.map(url => createElementHTML(url)).join('');
  videoGrid.innerHTML = videos.map(url => createElementHTML(url)).join('');
});
