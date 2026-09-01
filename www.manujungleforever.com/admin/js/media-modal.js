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
      #media-modal-body .media-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        gap: 12px;
        max-height: 480px;
        overflow-y: auto;
        padding: 4px;
      }
      #media-modal-body .m-item {
        position: relative;
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.75);
        border: 1.5px solid rgba(255, 255, 255, 0.09);
        overflow: hidden;
        cursor: pointer;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
      }
      #media-modal-body .m-item:hover {
        border-color: rgba(45, 212, 191, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
      }
      #media-modal-body .m-item.selected {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45, 212, 191, 0.4), 0 8px 20px rgba(0, 0, 0, 0.6) !important;
      }
      #media-modal-body .m-item.m-folder {
        background: linear-gradient(145deg, rgba(20, 36, 33, 0.85) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-color: rgba(45, 212, 191, 0.25);
        padding: 16px 10px;
        text-align: center;
        justify-content: center;
        align-items: center;
        min-height: 128px;
      }
      #media-modal-body .m-item.m-folder:hover {
        border-color: #2dd4bf;
        background: linear-gradient(145deg, rgba(28, 52, 48, 0.95) 0%, rgba(20, 30, 50, 0.95) 100%);
      }
      .m-folder-icon {
        font-size: 2.5rem;
        color: #2dd4bf;
        margin-bottom: 8px;
        line-height: 1;
      }
      .m-folder-name {
        font-size: 0.82rem;
        font-weight: 700;
        color: #f1f5f9;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width: 100%;
      }
      .m-folder-count {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 4px;
      }
      .m-thumb-wrap {
        position: relative;
        width: 100%;
        height: 96px;
        background: #090d16;
        overflow: hidden;
      }
      .m-thumb-wrap img,
      .m-thumb-wrap video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }
      .m-video-badge {
        position: absolute;
        top: 6px;
        right: 6px;
        background: rgba(0, 0, 0, 0.7);
        color: #2dd4bf;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
      }
      #media-modal-body .m-name {
        padding: 6px 8px;
        font-size: 0.7rem;
        color: #cbd5e1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        background: rgba(10, 15, 29, 0.95);
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
