
const MEDIA_API = '/api/media';
let token = sessionStorage.getItem('cms_token');

let allR2Files = [];
let currentPath = ''; // '' = root
let currentViewMode = localStorage.getItem('r2_view_mode') || 'grid';
let searchQuery = '';
let selectedLbFile = null;

// Formateadores
function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function formatDate(iso) {
  if (!iso) return '-';
  try {
    const d = new Date(iso);
    return d.toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch(e) { return iso; }
}

function esc(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function showToast(text) {
  const t = document.getElementById('toast-msg');
  const txt = document.getElementById('toast-text');
  txt.textContent = text;
  t.style.display = 'flex';
  setTimeout(() => { t.style.display = 'none'; }, 3000);
}

// ── CARGAR LISTA R2 ──
async function loadMedia() {
  const content = document.getElementById('explorer-content');
  content.innerHTML = '<div class="loading" style="padding:40px 0;text-align:center;"><div class="spinner"></div> Cargando explorador R2...</div>';
  
  try {
    const r = await fetch(MEDIA_API, { headers: { Authorization: `Bearer ${token}` } });
    if (r.status === 401) { sessionStorage.clear(); location.reload(); }
    const d = await r.json();
    if (!r.ok) throw new Error(d.error || 'Error al obtener medios');

    allR2Files = d.files || [];
    updateGlobalStats();
    renderCurrentView();
  } catch(e) {
    content.innerHTML = `<div style="color:var(--danger);padding:30px;text-align:center;">❌ Error al conectar con R2: ${e.message}</div>`;
  }
}

function updateGlobalStats() {
  const totalFiles = allR2Files.length;
  const totalSize = allR2Files.reduce((acc, f) => acc + (f.size || 0), 0);
  document.getElementById('stats-label').textContent = `${totalFiles} archivos almacenados (${formatBytes(totalSize)} en total)`;
}

// ── PARSEO DE CARPETAS Y ARCHIVOS ──
function getFolderContents(path) {
  const cleanPath = path.replace(/^\/+|\/+$/g, '');
  const folderMap = new Map();
  const files = [];

  allR2Files.forEach(f => {
    const key = f.key || '';
    if (!cleanPath) {
      // Nivel raíz
      if (key.includes('/')) {
        const topFolder = key.split('/')[0];
        if (!folderMap.has(topFolder)) {
          folderMap.set(topFolder, { name: topFolder, fullPath: topFolder, count: 0, size: 0 });
        }
        const item = folderMap.get(topFolder);
        item.count++;
        item.size += (f.size || 0);
      } else {
        files.push(f);
      }
    } else {
      // Dentro de una subcarpeta
      if (key.startsWith(cleanPath + '/')) {
        const rel = key.slice(cleanPath.length + 1);
        if (rel.includes('/')) {
          const nextFolder = rel.split('/')[0];
          const fullFolderPath = `${cleanPath}/${nextFolder}`;
          if (!folderMap.has(nextFolder)) {
            folderMap.set(nextFolder, { name: nextFolder, fullPath: fullFolderPath, count: 0, size: 0 });
          }
          const item = folderMap.get(nextFolder);
          item.count++;
          item.size += (f.size || 0);
        } else {
          files.push(f);
        }
      }
    }
  });

  return {
    folders: Array.from(folderMap.values()).sort((a, b) => a.name.localeCompare(b.name)),
    files: files
  };
}

// ── FILTROS Y ORDENACIÓN ──
function filterAndSortFiles(files) {
  let list = [...files];

  // Búsqueda
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase().trim();
    list = list.filter(f => f.key.toLowerCase().includes(q));
  }

  // Tipo
  const typeFilter = document.getElementById('filter-type')?.value || 'all';
  if (typeFilter === 'images') {
    list = list.filter(f => /\.(jpe?g|png|webp|gif|svg)$/i.test(f.key));
  } else if (typeFilter === 'videos') {
    list = list.filter(f => /\.(mp4|webm|mov)$/i.test(f.key));
  } else if (typeFilter === 'docs') {
    list = list.filter(f => /\.(pdf|docx?|xlsx?)$/i.test(f.key));
  }

  // Ordenación
  const sortMode = document.getElementById('filter-sort')?.value || 'date-desc';
  list.sort((a, b) => {
    if (sortMode === 'date-desc') return new Date(b.uploaded || 0) - new Date(a.uploaded || 0);
    if (sortMode === 'date-asc') return new Date(a.uploaded || 0) - new Date(b.uploaded || 0);
    if (sortMode === 'name-asc') return (a.key || '').localeCompare(b.key || '');
    if (sortMode === 'name-desc') return (b.key || '').localeCompare(a.key || '');
    if (sortMode === 'size-desc') return (b.size || 0) - (a.size || 0);
    if (sortMode === 'size-asc') return (a.size || 0) - (b.size || 0);
    return 0;
  });

  return list;
}

// ── RENDER PRINCIPAL ──
function renderCurrentView() {
  updateBreadcrumbs();
  const { folders, files } = getFolderContents(currentPath);
  const filteredFiles = filterAndSortFiles(files);
  const container = document.getElementById('explorer-content');

  // Si estamos en búsqueda global
  if (searchQuery.trim()) {
    const allFiltered = filterAndSortFiles(allR2Files);
    renderSearchResults(container, allFiltered);
    return;
  }

  if (folders.length === 0 && filteredFiles.length === 0) {
    container.innerHTML = `
      <div style="text-align:center;padding:60px 20px;color:var(--muted);">
        <i class="ph ph-folder-open" style="font-size:3.5rem;color:rgba(45,212,191,0.3);margin-bottom:12px;display:block;"></i>
        <p style="font-size:1.1rem;font-weight:600;color:#fff;">Esta carpeta está vacía</p>
        <p style="font-size:0.85rem;margin-top:4px;">Sube archivos o crea una nueva subcarpeta para comenzar.</p>
      </div>`;
    return;
  }

  let html = '';

  // 1. Carpetas
  if (folders.length > 0) {
    html += `<div class="section-title"><i class="ph ph-folder"></i> Carpetas (${folders.length})</div>`;
    html += `<div class="folder-grid">`;
    folders.forEach(f => {
      html += `
        <div class="folder-card" onclick="navigateToFolder('${esc(f.fullPath)}')">
          <div class="folder-icon"><i class="ph ph-folder-notch-fill"></i></div>
          <div class="folder-info">
            <div class="folder-name" title="${esc(f.name)}">${esc(f.name)}</div>
            <div class="folder-count">${f.count} archivo(s) · ${formatBytes(f.size)}</div>
          </div>
        </div>`;
    });
    html += `</div>`;
  }

  // 2. Archivos
  if (filteredFiles.length > 0) {
    html += `<div class="section-title"><i class="ph ph-file"></i> Archivos (${filteredFiles.length})</div>`;
    
    if (currentViewMode === 'grid') {
      html += `<div class="file-grid-large">`;
      filteredFiles.forEach(f => { html += renderLargeCard(f); });
      html += `</div>`;
    } else if (currentViewMode === 'compact') {
      html += `<div class="file-grid-compact">`;
      filteredFiles.forEach(f => { html += renderCompactCard(f); });
      html += `</div>`;
    } else if (currentViewMode === 'table') {
      html += renderTable(filteredFiles);
    }
  }

  container.innerHTML = html;
}

function renderSearchResults(container, list) {
  if (list.length === 0) {
    container.innerHTML = `<div style="text-align:center;padding:60px 20px;color:var(--muted);">No se encontraron archivos que coincidan con "<strong>${esc(searchQuery)}</strong>".</div>`;
    return;
  }
  let html = `<div class="section-title"><i class="ph ph-magnifying-glass"></i> Resultados de búsqueda (${list.length})</div>`;
  if (currentViewMode === 'table') {
    html += renderTable(list);
  } else {
    html += `<div class="file-grid-large">`;
    list.forEach(f => { html += renderLargeCard(f); });
    html += `</div>`;
  }
  container.innerHTML = html;
}

// ── PLANTILLAS DE RENDER ──
function getFileExtension(key) {
  return key.includes('.') ? key.split('.').pop().toLowerCase() : 'file';
}

function isImage(ext) { return ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg'].includes(ext); }
function isVideo(ext) { return ['mp4', 'webm', 'mov'].includes(ext); }

function renderLargeCard(f) {
  const ext = getFileExtension(f.key);
  const fileName = f.key.split('/').pop();
  let mediaThumb = '';

  if (isImage(ext)) {
    mediaThumb = `<img src="${esc(f.url)}" alt="${esc(fileName)}" loading="lazy">`;
  } else if (isVideo(ext)) {
    mediaThumb = `<video src="${esc(f.url)}" muted preload="metadata"></video>`;
  } else {
    mediaThumb = `<div class="file-doc-icon"><i class="ph ph-file-text"></i></div>`;
  }

  return `
    <div class="file-card-large">
      <div class="file-thumb-wrap" onclick="openLightbox('${esc(f.key)}')">
        ${mediaThumb}
        <span class="file-format-badge">${ext}</span>
      </div>
      <div class="file-card-body">
        <div class="file-name" title="${esc(fileName)}">${esc(fileName)}</div>
        <div class="file-meta">
          <span>${formatBytes(f.size)}</span>
          <span>${formatDate(f.uploaded).split(',')[0]}</span>
        </div>
        <div class="file-card-actions">
          <button class="btn-card-action" onclick="copyFileUrl('${esc(f.url)}')" title="Copiar URL"><i class="ph ph-link"></i> Copiar</button>
          <button class="btn-card-action" onclick="openLightbox('${esc(f.key)}')" title="Ver detalles"><i class="ph ph-eye"></i> Ver</button>
          <button class="btn-action-del" onclick="deleteFile('${esc(f.key)}')" title="Eliminar"><i class="ph ph-trash"></i></button>
        </div>
      </div>
    </div>`;
}

function renderCompactCard(f) {
  const ext = getFileExtension(f.key);
  const fileName = f.key.split('/').pop();
  let mediaThumb = isImage(ext) 
    ? `<img src="${esc(f.url)}" alt="${esc(fileName)}" loading="lazy">` 
    : `<div class="file-doc-icon" style="font-size:2rem;"><i class="ph ph-file"></i></div>`;

  return `
    <div class="file-card-compact" onclick="openLightbox('${esc(f.key)}')">
      <div class="file-thumb-wrap">
        ${mediaThumb}
        <span class="file-format-badge">${ext}</span>
      </div>
      <div class="file-name" title="${esc(fileName)}">${esc(fileName)}</div>
    </div>`;
}

function renderTable(files) {
  let rows = '';
  files.forEach(f => {
    const ext = getFileExtension(f.key);
    const fileName = f.key.split('/').pop();
    const folderPath = f.key.includes('/') ? f.key.slice(0, f.key.lastIndexOf('/')) : 'Raíz';
    const thumb = isImage(ext) 
      ? `<img src="${esc(f.url)}" class="table-thumb" onclick="openLightbox('${esc(f.key)}')" loading="lazy">` 
      : `<div class="table-doc-icon"><i class="ph ph-file"></i></div>`;

    rows += `
      <tr>
        <td style="width:50px;">${thumb}</td>
        <td>
          <div style="font-weight:600;color:#fff;cursor:pointer;" onclick="openLightbox('${esc(f.key)}')">${esc(fileName)}</div>
          <div style="font-size:0.72rem;color:var(--muted);">${esc(f.key)}</div>
        </td>
        <td><span style="font-size:0.8rem;color:var(--teal);">${esc(folderPath)}</span></td>
        <td><span class="file-format-badge" style="position:static;display:inline-block;">${ext}</span></td>
        <td style="font-family:monospace;font-size:0.82rem;">${formatBytes(f.size)}</td>
        <td style="font-size:0.8rem;color:var(--muted);">${formatDate(f.uploaded)}</td>
        <td style="text-align:right;">
          <div style="display:inline-flex;gap:6px;">
            <button class="btn-card-action" onclick="copyFileUrl('${esc(f.url)}')" title="Copiar URL"><i class="ph ph-link"></i></button>
            <button class="btn-card-action" onclick="openLightbox('${esc(f.key)}')" title="Ver"><i class="ph ph-eye"></i></button>
            <button class="btn-action-del" onclick="deleteFile('${esc(f.key)}')" title="Eliminar"><i class="ph ph-trash"></i></button>
          </div>
        </td>
      </tr>`;
  });

  return `
    <div class="file-table-wrap">
      <table class="file-table">
        <thead>
          <tr>
            <th>Vista</th>
            <th>Nombre</th>
            <th>Carpeta</th>
            <th>Tipo</th>
            <th>Tamaño</th>
            <th>Fecha</th>
            <th style="text-align:right;">Acciones</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

// ── NAVEGACIÓN Y BREADCRUMBS ──
function updateBreadcrumbs() {
  const container = document.getElementById('breadcrumbs-container');
  const btnUp = document.getElementById('btn-up-level');
  const clean = currentPath.replace(/^\/+|\/+$/g, '');

  if (!clean) {
    btnUp.style.display = 'none';
    container.innerHTML = `<span class="crumb-item active"><i class="ph ph-hard-drive"></i> Raíz (Almacenamiento R2)</span>`;
    return;
  }

  btnUp.style.display = 'inline-flex';
  const parts = clean.split('/');
  let html = `<span class="crumb-item" onclick="navigateToFolder('')"><i class="ph ph-hard-drive"></i> Raíz</span>`;

  let accumulated = '';
  parts.forEach((p, idx) => {
    accumulated = accumulated ? `${accumulated}/${p}` : p;
    const isLast = idx === parts.length - 1;
    html += `<span class="crumb-sep">/</span>`;
    if (isLast) {
      html += `<span class="crumb-item active"><i class="ph ph-folder-open"></i> ${esc(p)}</span>`;
    } else {
      const target = accumulated;
      html += `<span class="crumb-item" onclick="navigateToFolder('${esc(target)}')"><i class="ph ph-folder"></i> ${esc(p)}</span>`;
    }
  });

  container.innerHTML = html;
}

window.navigateToFolder = function(path) {
  currentPath = path;
  searchQuery = '';
  document.getElementById('search-input').value = '';
  document.getElementById('search-clear').style.display = 'none';
  renderCurrentView();
};

window.goUpOneLevel = function() {
  if (!currentPath) return;
  const parts = currentPath.replace(/^\/+|\/+$/g, '').split('/');
  parts.pop();
  currentPath = parts.join('/');
  renderCurrentView();
};

window.setViewMode = function(mode) {
  currentViewMode = mode;
  localStorage.setItem('r2_view_mode', mode);
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`btn-view-${mode}`)?.classList.add('active');
  renderCurrentView();
};

// ── BÚSQUEDA ──
window.handleSearch = function(val) {
  searchQuery = val;
  document.getElementById('search-clear').style.display = val ? 'block' : 'none';
  renderCurrentView();
};

window.clearSearch = function() {
  document.getElementById('search-input').value = '';
  searchQuery = '';
  document.getElementById('search-clear').style.display = 'none';
  renderCurrentView();
};

// ── SUBIDA DE ARCHIVOS Y CARPETAS ──
window.triggerFileUpload = function() {
  document.getElementById('input-upload-files').click();
};

window.triggerFolderUpload = function() {
  document.getElementById('input-upload-folder').click();
};

window.promptCreateFolder = function() {
  const name = prompt('Nombre de la nueva carpeta:');
  if (!name || !name.trim()) return;
  const cleanName = name.trim().replace(/[^a-z0-9_-]/gi, '-').toLowerCase();
  const newFolderPath = currentPath ? `${currentPath}/${cleanName}` : cleanName;
  navigateToFolder(newFolderPath);
  showToast(`Carpeta "${cleanName}" lista. Sube archivos dentro para crearla en R2.`);
};

window.handleFilesSelected = async function(input) {
  if (!input.files || input.files.length === 0) return;
  await uploadFileList(Array.from(input.files), currentPath);
  input.value = '';
};

window.handleFolderSelected = async function(input) {
  if (!input.files || input.files.length === 0) return;
  const files = Array.from(input.files);
  await uploadFileList(files, currentPath, true);
  input.value = '';
};

async function uploadFileList(files, targetFolder, isFolderUpload = false) {
  const statsLabel = document.getElementById('stats-label');
  const originalText = statsLabel.textContent;
  let successCount = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    statsLabel.textContent = `Subiendo (${i + 1}/${files.length}): ${file.name}...`;

    try {
      let relativePath = file.name;
      if (isFolderUpload && file.webkitRelativePath) {
        relativePath = file.webkitRelativePath;
      }
      
      const fullKey = targetFolder ? `${targetFolder}/${relativePath}` : relativePath;
      const renamedFile = new File([file], fullKey, { type: file.type || 'application/octet-stream' });

      const r = await fetch(MEDIA_API, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'X-File-Name': encodeURIComponent(renamedFile.name),
          'Content-Type': file.type || 'application/octet-stream'
        },
        body: renamedFile
      });

      if (r.ok) successCount++;
    } catch(e) {
      console.error('Error subiendo archivo:', e);
    }
  }

  statsLabel.textContent = originalText;
  showToast(`✓ ${successCount} de ${files.length} archivo(s) subido(s) con éxito.`);
  await loadMedia();
}

// ── DRAG & DROP ──
const dropZone = document.getElementById('explorer-container');
const dropOverlay = document.getElementById('drop-overlay');

['dragenter', 'dragover'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropOverlay.classList.add('active');
  }, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropOverlay.classList.remove('active');
  }, false);
});

dropZone.addEventListener('drop', async (e) => {
  const dt = e.dataTransfer;
  const files = dt.files;
  if (files && files.length > 0) {
    await uploadFileList(Array.from(files), currentPath);
  }
});

// ── COPIAR Y ELIMINAR ──
window.copyFileUrl = function(url) {
  const fullUrl = url.startsWith('http') ? url : window.location.origin + url;
  navigator.clipboard.writeText(fullUrl).then(() => {
    showToast('✓ Enlace copiado al portapapeles');
  }).catch(() => {
    prompt('Copia este enlace:', fullUrl);
  });
};

window.deleteFile = async function(key) {
  if (!confirm(`¿Estás seguro de eliminar permanentemente "${key}" de Cloudflare R2?`)) return;

  try {
    const r = await fetch(`${MEDIA_API}/${encodeURIComponent(key)}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error || 'Error al eliminar');

    showToast('✓ Archivo eliminado de R2');
    if (selectedLbFile && selectedLbFile.key === key) {
      closeLightbox();
    }
    await loadMedia();
  } catch(e) {
    alert('Error al eliminar archivo: ' + e.message);
  }
};

// ── LIGHTBOX / INSPECTOR ──
window.openLightbox = function(key) {
  const f = allR2Files.find(x => x.key === key);
  if (!f) return;
  selectedLbFile = f;

  const ext = getFileExtension(f.key);
  const fileName = f.key.split('/').pop();
  const fullUrl = f.url.startsWith('http') ? f.url : window.location.origin + f.url;

  document.getElementById('lb-title').textContent = fileName;
  document.getElementById('lb-filename').textContent = fileName;
  document.getElementById('lb-key').textContent = f.key;
  document.getElementById('lb-size').textContent = `${formatBytes(f.size)} (${(f.size || 0).toLocaleString()} bytes)`;
  document.getElementById('lb-date').textContent = formatDate(f.uploaded);
  document.getElementById('lb-url').value = fullUrl;
  document.getElementById('lb-btn-download').href = fullUrl;

  const previewCol = document.getElementById('lb-preview-col');
  if (isImage(ext)) {
    previewCol.innerHTML = `<img src="${esc(f.url)}" alt="${esc(fileName)}">`;
  } else if (isVideo(ext)) {
    previewCol.innerHTML = `<video src="${esc(f.url)}" controls autoplay style="max-height:420px;width:100%;"></video>`;
  } else {
    previewCol.innerHTML = `<div style="text-align:center;color:var(--teal);"><i class="ph ph-file-text" style="font-size:5rem;"></i><p style="margin-top:10px;font-weight:600;">Archivo ${ext.toUpperCase()}</p></div>`;
  }

  document.getElementById('lightbox-modal').classList.add('open');
};

window.closeLightbox = function() {
  document.getElementById('lightbox-modal').classList.remove('open');
  const previewCol = document.getElementById('lb-preview-col');
  previewCol.innerHTML = '';
  selectedLbFile = null;
};

window.copyLbUrl = function() {
  const inp = document.getElementById('lb-url');
  copyFileUrl(inp.value);
};

window.deleteCurrentLbFile = function() {
  if (selectedLbFile) {
    deleteFile(selectedLbFile.key);
  }
};

// ── INICIALIZACIÓN ──
document.addEventListener('DOMContentLoaded', () => {
  if (!token) return;
  if (typeof tsParticles !== 'undefined') {
    tsParticles.load('pg-particles', {
      fpsLimit: 60,
      particles: {
        number: { value: 24, density: { enable: true, area: 800 } },
        color: { value: ['#c9a84c', '#2dd4bf', '#ffffff'] },
        shape: { type: 'circle' },
        opacity: { value: 0.35, random: true, animation: { enable: true, speed: 0.4, minimumValue: 0.08, sync: false } },
        size: { value: 2.2, random: true, animation: { enable: true, speed: 0.6, minimumValue: 0.4, sync: false } },
        move: { enable: true, speed: 0.45, direction: 'top', random: true, straight: false, outModes: { default: 'out' } }
      },
      detectRetina: true
    });
  }

  // Activar modo guardado en vista
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`btn-view-${currentViewMode}`)?.classList.add('active');

  loadMedia();
});
