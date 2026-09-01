/**
 * attribution-hydrator.js — Automatic & Minimalist Media Attribution System
 * Injects ultra-discreet, glassmorphism micro-badges for Wikimedia/R2 images with licensing metadata.
 */

(function() {
  window.__mediaAttributionsCache = window.__mediaAttributionsCache || null;
  let isFetching = false;
  const pendingCallbacks = [];

  function injectAttributionStyles() {
    if (document.getElementById('media-attribution-styles')) return;
    const style = document.createElement('style');
    style.id = 'media-attribution-styles';
    style.textContent = `
      .media-attr-badge {
        position: absolute !important;
        bottom: 8px !important;
        right: 8px !important;
        z-index: 15 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        background: rgba(10, 15, 29, 0.45) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: rgba(255, 255, 255, 0.72) !important;
        font-size: 9.5px !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        line-height: 1.25 !important;
        font-weight: 500 !important;
        padding: 2px 7px !important;
        border-radius: 9999px !important;
        opacity: 0.65 !important;
        transition: opacity 0.3s ease, color 0.3s ease, background 0.3s ease !important;
        max-width: 82% !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        pointer-events: auto !important;
        user-select: none !important;
      }
      .media-attr-badge:hover {
        opacity: 1 !important;
        color: #ffffff !important;
        background: rgba(10, 15, 29, 0.85) !important;
        border-color: rgba(45, 212, 191, 0.45) !important;
      }
      .media-attr-badge a {
        color: inherit !important;
        text-decoration: underline !important;
        transition: color 0.2s ease !important;
      }
      .media-attr-badge a:hover {
        color: #2dd4bf !important;
      }
      @media (max-width: 640px) {
        .media-attr-badge {
          font-size: 8.5px !important;
          padding: 1.5px 6px !important;
          bottom: 6px !important;
          right: 6px !important;
        }
      }
    `;
    document.head.appendChild(style);
  }

  async function loadAttributions() {
    if (window.__mediaAttributionsCache) return window.__mediaAttributionsCache;
    if (isFetching) {
      return new Promise(resolve => pendingCallbacks.push(resolve));
    }

    isFetching = true;
    try {
      const res = await fetch('/data/attributions.json?t=' + Date.now(), { cache: 'no-store' }).catch(() => null);
      if (!res || !res.ok) {
        window.__mediaAttributionsCache = {};
        return window.__mediaAttributionsCache;
      }
      const list = await res.json();
      const map = {};
      if (Array.isArray(list)) {
        list.forEach(item => {
          if (!item) return;
          const attr = item.attribution || {};
          const meta = {
            author: attr.author || 'Wikimedia Commons',
            license: attr.license || 'CC',
            license_url: attr.license_url || '',
            description: attr.description || ''
          };

          if (item.filename) {
            map[item.filename.toLowerCase()] = meta;
            map[decodeURIComponent(item.filename).toLowerCase()] = meta;
          }
          if (item.r2_path) {
            map[item.r2_path.toLowerCase()] = meta;
            map[decodeURIComponent(item.r2_path).toLowerCase()] = meta;
          }
        });
      }
      window.__mediaAttributionsCache = map;
      pendingCallbacks.forEach(cb => cb(map));
      return map;
    } catch(e) {
      window.__mediaAttributionsCache = {};
      return window.__mediaAttributionsCache;
    } finally {
      isFetching = false;
    }
  }

  function getAttributionForUrl(url, map) {
    if (!url || !map) return null;
    try {
      const decoded = decodeURIComponent(url);
      const clean = decoded.split('?')[0].split('#')[0];
      const filename = clean.split('/').pop().toLowerCase();
      
      // Match by filename
      if (map[filename]) return map[filename];
      
      // Match by relative path
      const parts = clean.split('/media/');
      if (parts.length > 1) {
        const rel = parts[1].toLowerCase();
        if (map[rel]) return map[rel];
      }
      
      // Match by folder + file
      const segs = clean.split('/');
      if (segs.length >= 2) {
        const lastTwo = `${segs[segs.length - 2]}/${segs[segs.length - 1]}`.toLowerCase();
        if (map[lastTwo]) return map[lastTwo];
      }
    } catch(e) {}
    return null;
  }

  window.hydrateMediaAttributions = async function() {
    injectAttributionStyles();
    const map = await loadAttributions();
    if (!map || Object.keys(map).length === 0) return;

    const images = document.querySelectorAll('img');
    images.forEach(img => {
      const src = img.getAttribute('src') || img.currentSrc || '';
      if (!src) return;

      const meta = getAttributionForUrl(src, map);
      if (!meta) return;

      const parent = img.parentElement;
      if (!parent) return;

      // Check if badge already exists
      if (parent.querySelector('.media-attr-badge')) return;

      // Ensure parent container is positioned
      const computedPos = window.getComputedStyle(parent).position;
      if (computedPos === 'static') {
        parent.style.position = 'relative';
      }

      // Create micro-badge
      const badge = document.createElement('span');
      badge.className = 'media-attr-badge';
      badge.title = `${meta.author} · ${meta.license}`;

      const photoText = document.createElement('span');
      photoText.textContent = `📷 Photo: ${meta.author}`;
      badge.appendChild(photoText);

      const sep = document.createElement('span');
      sep.textContent = '·';
      badge.appendChild(sep);

      if (meta.license_url) {
        const link = document.createElement('a');
        link.href = meta.license_url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = meta.license;
        badge.appendChild(link);
      } else {
        const licText = document.createElement('span');
        licText.textContent = meta.license;
        badge.appendChild(licText);
      }

      parent.appendChild(badge);
    });
  };

  // Run on load and observe dynamic DOM changes
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      window.hydrateMediaAttributions();
    });
  } else {
    window.hydrateMediaAttributions();
  }

  // MutationObserver to auto-hydrate newly injected images
  if (typeof MutationObserver !== 'undefined') {
    let debounceTimer = null;
    const observer = new MutationObserver(mutations => {
      let hasNewImg = false;
      for (const m of mutations) {
        if (m.addedNodes && m.addedNodes.length > 0) {
          hasNewImg = true;
          break;
        }
      }
      if (hasNewImg) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          window.hydrateMediaAttributions();
        }, 150);
      }
    });

    observer.observe(document.body || document.documentElement, {
      childList: true,
      subtree: true
    });
  }
})();
