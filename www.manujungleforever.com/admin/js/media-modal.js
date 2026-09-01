/**
 * media-modal.js — Hierarchical Media Gallery Modal for Admin CMS
 * Implements strict media filtering, Windows-style folder navigation,
 * breadcrumbs bar, visual folder cards, and media selection.
 */

(function() {
  let modalCallback = null;
  let allMediaFiles = [];
  let modalCurrentPath = '';
  let selectedMediaUrl = null;

  const ALLOWED_EXTS = /\.(jpe?g|png|gif|webp|mp4|webm|mov|svg|avif)$/i;

  function isMediaFile(key) {
    if (!key || typeof key !== 'string') return false;
    const clean = key.trim();
    if (!clean || clean.startsWith('.') || clean.endsWith('.keep_folder') || clean.includes('/.keep_folder') || clean.includes('.keep_folder')) return false;
    return ALLOWED_EXTS.test(clean);
  }

  function normalizePath(p) {
    if (!p) return '';
    return p.replace(/^\/+|\/+$/g, '').trim();
  }

  function injectModalStyles() {
    if (document.getElementById('media-modal-modern-styles')) return;
    const style = document.createElement('style');
    style.id = 'media-modal-modern-styles';
    style.textContent = `
      .modal-nav-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(45, 212, 191, 0.2);
        border-radius: 12px;
        margin-bottom: 16px;
        flex-wrap: wrap;
      }
      .modal-nav-back {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(45, 212, 191, 0.15);
        border: 1px solid rgba(45, 212, 191, 0.35);
        color: #2dd4bf;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
      }
      .modal-nav-back:hover {
        background: rgba(45, 212, 191, 0.25);
        border-color: #2dd4bf;
        transform: translateX(-2px);
      }
      .modal-breadcrumbs {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85rem;
        color: #94a3b8;
        overflow-x: auto;
        white-space: nowrap;
        flex: 1;
      }
      .modal-bc-item {
        color: #94a3b8;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 6px;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }
      .modal-bc-item:hover {
        color: #2dd4bf;
        background: rgba(255, 255, 255, 0.05);
      }
      .modal-bc-item.active {
        color: #fff;
        font-weight: 600;
        cursor: default;
        background: rgba(45, 212, 191, 0.15);
        border: 1px solid rgba(45, 212, 191, 0.3);
      }
      .modal-bc-sep {
        color: #64748b;
        font-size: 0.75rem;
      }
      #media-modal-body {
        display: block !important;
        overflow: visible !important;
        min-height: 0 !important;
        padding: 16px 20px !important;
      }
      #media-modal-body .media-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fill, minmax(135px, 1fr)) !important;
        gap: 14px !important;
        max-height: 60vh !important;
        overflow-y: auto !important;
        padding: 4px !important;
        align-content: start !important;
      }
      #media-modal-body .m-item {
        position: relative !important;
        border-radius: 12px !important;
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
        overflow: hidden !important;
        cursor: pointer !important;
        display: flex !important;
        flex-direction: column !important;
        height: auto !important;
        min-height: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }
      #media-modal-body .m-item:hover {
        border-color: rgba(45, 212, 191, 0.55) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.55) !important;
      }
      #media-modal-body .m-item.selected {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45, 212, 191, 0.45), 0 8px 22px rgba(0, 0, 0, 0.65) !important;
      }
      #media-modal-body .m-item.m-folder {
        background: linear-gradient(145deg, rgba(20, 36, 33, 0.85) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border-color: rgba(45, 212, 191, 0.25) !important;
        padding: 20px 10px !important;
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
        min-height: 135px !important;
      }
      #media-modal-body .m-item.m-folder:hover {
        border-color: #2dd4bf !important;
        background: linear-gradient(145deg, rgba(28, 52, 48, 0.95) 0%, rgba(20, 30, 50, 0.95) 100%) !important;
      }
      .m-folder-icon {
        font-size: 2.5rem !important;
        color: #2dd4bf !important;
        margin-bottom: 8px !important;
        line-height: 1 !important;
      }
      .m-folder-name {
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        width: 100% !important;
        box-sizing: border-box !important;
        text-align: center !important;
      }
      .m-folder-count {
        font-size: 0.7rem !important;
        color: #94a3b8 !important;
        margin-top: 4px !important;
      }
      #media-modal-body .m-thumb-wrap {
        position: relative !important;
        width: 100% !important;
        aspect-ratio: 16 / 11 !important;
        height: auto !important;
        background: #090d16 !important;
        overflow: hidden !important;
        flex-shrink: 0 !important;
      }
      #media-modal-body .m-thumb-wrap img,
      #media-modal-body .m-thumb-wrap video {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        display: block !important;
        border-radius: 0 !important;
      }
      .m-video-badge {
        position: absolute !important;
        top: 6px !important;
        right: 6px !important;
        background: rgba(0, 0, 0, 0.7) !important;
        color: #2dd4bf !important;
        width: 22px !important;
        height: 22px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.75rem !important;
      }
      #media-modal-body .m-name {
        padding: 7px 8px !important;
        font-size: 0.72rem !important;
        font-weight: 500 !important;
        color: #cbd5e1 !important;
        text-align: center !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        background: rgba(10, 15, 29, 0.95) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
        width: 100% !important;
        box-sizing: border-box !important;
        display: block !important;
      }
    `;
    document.head.appendChild(style);
  }

  window.openMediaModal = async function(callback) {
    injectModalStyles();
    modalCallback = callback;
    selectedMediaUrl = null;
    modalCurrentPath = '';

    const confirmBtn = document.getElementById('media-confirm');
    if (confirmBtn) confirmBtn.disabled = true;

    if (typeof window.openModal === 'function') {
      window.openModal('media-modal');
    } else {
      const m = document.getElementById('media-modal');
      if (m) m.classList.add('open');
    }

    const body = document.getElementById('media-modal-body');
    if (!body) return;

    body.innerHTML = `<div class="loading" style="padding: 40px 0; text-align: center; color: #94a3b8;"><div class="spinner" style="margin: 0 auto 12px;"></div> Cargando galería de medios...</div>`;

    try {
      let rawList = [];
      if (typeof window.r2GetList === 'function') {
        rawList = await window.r2GetList();
      } else {
        const token = sessionStorage.getItem('cms_token');
        const mediaApi = window.MEDIA_API || '/api/media';
        const res = await fetch(mediaApi, { headers: { Authorization: `Bearer ${token}` } });
        if (res.status === 401) { sessionStorage.clear(); location.reload(); return; }
        const d = await res.json();
        rawList = d.files || [];
      }

      // Requirement 1: Strict Media Filtering
      allMediaFiles = (rawList || []).filter(f => isMediaFile(f.key));
      renderExplorer();
    } catch(err) {
      body.innerHTML = `<div class="err-msg" style="display:block; padding: 20px; color: #ef4444; background: rgba(239,68,68,0.1); border-radius: 8px;">❌ ${err.message || 'Error cargando archivos'}</div>`;
    }
  };

  window.navigateModalPath = function(path) {
    modalCurrentPath = normalizePath(path);
    renderExplorer();
  };

  window.selectModalMediaItem = function(url, el) {
    selectedMediaUrl = url;
    const body = document.getElementById('media-modal-body');
    if (body) {
      body.querySelectorAll('.m-item.m-file').forEach(item => item.classList.remove('selected'));
    }
    if (el) el.classList.add('selected');

    const confirmBtn = document.getElementById('media-confirm');
    if (confirmBtn) confirmBtn.disabled = false;
  };

  window.confirmMediaSelect = function() {
    if (selectedMediaUrl && typeof modalCallback === 'function') {
      try {
        modalCallback(selectedMediaUrl);
      } catch(e) {
        console.error('Error executing media callback:', e);
      }
    }
    if (typeof window.closeModal === 'function') {
      window.closeModal('media-modal');
    } else {
      const m = document.getElementById('media-modal');
      if (m) m.classList.remove('open');
    }
  };

  function renderExplorer() {
    const body = document.getElementById('media-modal-body');
    if (!body) return;

    const curr = normalizePath(modalCurrentPath);

    // Requirement 2: Parse folders & files in current directory level
    const folderCounts = {};
    const filesInDir = [];

    allMediaFiles.forEach(f => {
      const key = f.key.replace(/^\/+/, '');
      if (curr === '') {
        if (key.includes('/')) {
          const folderName = key.split('/')[0];
          folderCounts[folderName] = (folderCounts[folderName] || 0) + 1;
        } else {
          filesInDir.push(f);
        }
      } else {
        if (key.startsWith(curr + '/')) {
          const sub = key.slice(curr.length + 1);
          if (sub.includes('/')) {
            const folderName = sub.split('/')[0];
            folderCounts[folderName] = (folderCounts[folderName] || 0) + 1;
          } else {
            filesInDir.push(f);
          }
        }
      }
    });

    const folderNames = Object.keys(folderCounts).sort((a, b) => a.localeCompare(b));
    filesInDir.sort((a, b) => (a.key || '').localeCompare(b.key || ''));

    // Requirement 3: Breadcrumbs Navigation Bar
    const pathParts = curr ? curr.split('/') : [];
    let breadcrumbHtml = `
      <div class="modal-nav-bar">
        ${curr !== '' ? `
          <button type="button" class="modal-nav-back" onclick="navigateModalPath('${pathParts.slice(0, -1).join('/')}')">
            <i class="ph ph-arrow-left"></i> Volver
          </button>
        ` : ''}
        <div class="modal-breadcrumbs">
          <span class="modal-bc-item ${curr === '' ? 'active' : ''}" onclick="navigateModalPath('')">
            <i class="ph ph-house"></i> Raíz
          </span>
    `;

    pathParts.forEach((part, idx) => {
      const full = pathParts.slice(0, idx + 1).join('/');
      const isLast = idx === pathParts.length - 1;
      breadcrumbHtml += `
        <span class="modal-bc-sep">/</span>
        <span class="modal-bc-item ${isLast ? 'active' : ''}" ${!isLast ? `onclick="navigateModalPath('${full}')"` : ''}>
          ${part}
        </span>
      `;
    });

    breadcrumbHtml += `
        </div>
      </div>
    `;

    // Grid rendering (Folders first, then files)
    let gridContent = '';
    if (folderNames.length === 0 && filesInDir.length === 0) {
      gridContent = `
        <div class="empty" style="grid-column: 1 / -1; padding: 48px 0; text-align: center; color: #64748b;">
          <i class="ph ph-folder-dashed" style="font-size: 2.8rem; display: block; margin-bottom: 12px; color: #475569;"></i>
          Esta carpeta está vacía
        </div>
      `;
    } else {
      // 1. Folders
      folderNames.forEach(name => {
        const folderFullPath = curr ? `${curr}/${name}` : name;
        const count = folderCounts[name];
        gridContent += `
          <div class="m-item m-folder" onclick="navigateModalPath('${folderFullPath}')" title="Carpeta: ${name}">
            <div class="m-folder-icon">
              <i class="ph ph-folder"></i>
            </div>
            <div class="m-folder-info">
              <div class="m-folder-name">${name}</div>
              <div class="m-folder-count">${count} archivo${count !== 1 ? 's' : ''}</div>
            </div>
          </div>
        `;
      });

      // 2. Files
      filesInDir.forEach(f => {
        const isVideo = /\.(mp4|webm|mov)$/i.test(f.key);
        const fileName = f.key.split('/').pop() || f.key;
        const isSelected = selectedMediaUrl === f.url;

        gridContent += `
          <div class="m-item m-file ${isSelected ? 'selected' : ''}" onclick="selectModalMediaItem('${f.url}', this)" title="${fileName}">
            <div class="m-thumb-wrap">
              ${isVideo ? `
                <video src="${f.url}" preload="metadata"></video>
                <div class="m-video-badge"><i class="ph ph-play"></i></div>
              ` : `
                <img src="${f.url}" loading="lazy" alt="${fileName}">
              `}
            </div>
            <div class="m-name">${fileName}</div>
          </div>
        `;
      });
    }

    body.innerHTML = `
      ${breadcrumbHtml}
      <div class="media-grid">
        ${gridContent}
      </div>
    `;
  }

  // Hook upload handlers so they reload the hierarchical explorer after upload
  document.addEventListener('DOMContentLoaded', () => {
    const mediaUploadInput = document.getElementById('media-upload');
    const folderUploadInput = document.getElementById('media-upload-folder');
    const confirmBtn = document.getElementById('media-confirm');

    if (confirmBtn) {
      confirmBtn.onclick = () => window.confirmMediaSelect();
    }

    async function handleUpload(e) {
      const files = Array.from(e.target.files || []);
      if (!files.length) return;
      e.target.value = '';

      const inModal = document.getElementById('media-modal')?.classList.contains('open') || 
                      document.getElementById('media-modal')?.classList.contains('active');
      const progEl = document.getElementById(inModal ? 'media-upload-prog' : 'main-upload-prog');

      let successCount = 0, errorCount = 0, lastError = '';

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) continue;
        try {
          if (progEl) progEl.textContent = `Subiendo ${i+1}/${files.length}... (${file.name})`;
          if (typeof window.r2Upload === 'function') {
            await window.r2Upload(file, null);
          } else {
            const token = sessionStorage.getItem('cms_token');
            const mediaApi = window.MEDIA_API || '/api/media';
            await fetch(mediaApi, {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
                'X-File-Name': encodeURIComponent(file.name),
                'Content-Type': file.type || 'application/octet-stream'
              },
              body: file
            });
          }
          successCount++;
        } catch(err) {
          console.error(err);
          errorCount++;
          lastError = err.message;
        }
      }

      if (progEl) {
        progEl.textContent = `✓ Subidos: ${successCount}` + (errorCount ? `, ✗ Errores: ${errorCount}` : '');
        setTimeout(() => { if (progEl) progEl.textContent = ''; }, 5000);
      }

      if (inModal) {
        try {
          let rawList = [];
          if (typeof window.r2GetList === 'function') {
            rawList = await window.r2GetList();
          } else {
            const token = sessionStorage.getItem('cms_token');
            const mediaApi = window.MEDIA_API || '/api/media';
            const res = await fetch(mediaApi, { headers: { Authorization: `Bearer ${token}` } });
            const d = await res.json();
            rawList = d.files || [];
          }
          allMediaFiles = (rawList || []).filter(f => isMediaFile(f.key));
          renderExplorer();
        } catch(e) {}
      }
    }

    if (mediaUploadInput) mediaUploadInput.addEventListener('change', handleUpload);
    if (folderUploadInput) folderUploadInput.addEventListener('change', handleUpload);
  });
})();
