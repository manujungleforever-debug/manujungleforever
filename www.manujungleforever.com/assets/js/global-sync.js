(function() {
  async function syncSiteData() {
    try {
      const isContactPage = window.location.pathname.includes('/contact/') || window.location.pathname.endsWith('/contact');
      
      // Fetch both configs in parallel with API first and static fallback
      let [gRes, cRes] = await Promise.all([
        fetch('/api/content/global?v=' + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/content/contact?v=' + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null)
      ]);

      if (!gRes || (!gRes.site_name && !gRes.data)) {
        gRes = await fetch('/data/global.json?v=' + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null);
      }
      if (!cRes || (!cRes.contacto_principal && !cRes.data)) {
        cRes = await fetch('/data/contact.json?v=' + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null);
      }

      const gData = (gRes && gRes.data) ? gRes.data : (gRes || {});
      const cData = (cRes && cRes.data) ? cRes.data : (cRes || {});
      const cp = cData.contacto_principal || {};
      const dir = cData.direccion || {};
      const soc = gData.social || gData.redes_sociales || {};

      // Unified Contact Fields from contact.json (single source of truth)
      const phone1 = cp.telefono_1 || gData.phone_primary || '+51 901 525 679';
      const phone2 = cp.telefono_2 || gData.phone_secondary || '';
      const email = cp.email || gData.email || 'discover@manujungleforever.com';
      const waNum = (cp.whatsapp || gData.whatsapp_number || '51901525679').replace(/[^0-9]/g, '');
      const waTxt = encodeURIComponent(cp.whatsapp_texto || gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');
      const waLink = `https://api.whatsapp.com/send?phone=${waNum}&text=${waTxt}`;
      const waDirect = `https://wa.me/${waNum}`;

      // Address & Map
      const addrParts = [];
      if (dir.nombre) addrParts.push(dir.nombre);
      const subParts = [dir.calle, dir.localidad, dir.pais].filter(Boolean).join(', ');
      if (subParts) addrParts.push(subParts);
      const addressText = addrParts.join(', ') || gData.address || 'Manu Jungle Forever 17800, Nuevo Eden, Peru';
      const mapsUrl = dir.maps_url || gData.address_maps_url || 'https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc';

      // 5. Individual Tour Page dynamic hydration from D1
      await syncTourPage();

      // 6. Home Page Dynamic Hydration (e.g. Wildlife Section)
      await syncHomePage();
    } catch(err) {
      console.warn('Sync error:', err);
    }
  }

  function fixImgPath(p) {
    if (!p) return '';
    if (p.startsWith('http://') || p.startsWith('https://') || p.startsWith('data:')) return p;
    if (p.startsWith('/')) return p;
    return '/' + p;
  }

  async function syncTourPage() {
    const reservedPages = ['about', 'admin', 'contact', 'blog', 'guided-tours', 'departures', 'news-and-gallery', 'faq', 'libro-de-reclamaciones', 'privacy-policy', 'terms-and-conditions', 'cookies-policy', 'itinerary-builder', 'book-now', ''];
    const parts = window.location.pathname.replace(/^\/+|\/+$/g, '').split('/');
    const last = parts[parts.length - 1];
    const slug = (last === 'index.html' || last === '') ? (parts[parts.length - 2] || '') : last;

    if (!slug || reservedPages.includes(slug)) return;

    try {
      const res = await fetch(`/api/tours/${encodeURIComponent(slug)}?v=${Date.now()}`).catch(() => null);
      if (!res || !res.ok) return;
      const t = await res.json();
      if (!t || !t.nombre) return;

      // 1. Hero Title & Category
      const h1 = document.querySelector('.in-hero .h1');
      if (h1 && t.nombre) h1.textContent = t.nombre;

      const ey = document.querySelector('.in-hero .ey');
      if (ey && t.categoria) ey.textContent = t.categoria.toUpperCase();

      // 2. Hero Background Image
      if (t.imagen_hero) {
        const hero = document.querySelector('.in-hero');
        if (hero) {
          hero.style.backgroundImage = `url('${fixImgPath(t.imagen_hero)}')`;
        }
      }

      // 3. Badges in Hero
      const durText = `${t.duracion_dias || 1} Days / ${t.duracion_noches || 0} Nights`;
      const capText = `${t.capacidad_min || 1}–${t.capacidad_max || 8} Travelers`;
      const difText = t.dificultad || 'Fácil';

      const heroSpans = document.querySelectorAll('.in-hero .cx div span');
      if (heroSpans.length >= 3) {
        if (heroSpans[0]) heroSpans[0].innerHTML = `<i class="far fa-clock" style="color:var(--a, #2dd4bf);"></i> ${durText}`;
        if (heroSpans[1]) heroSpans[1].innerHTML = `<i class="fas fa-users" style="color:var(--a, #2dd4bf);"></i> ${capText}`;
        if (heroSpans[2]) heroSpans[2].innerHTML = `<i class="fas fa-mountain" style="color:var(--a, #2dd4bf);"></i> ${difText}`;
      }

      // 4. Sidebar Pricing & Features
      const priceVal = document.querySelector('.tour-page-grid div[style*="font-size:2.2rem"]');
      if (priceVal && t.precio_desde !== undefined) {
        priceVal.innerHTML = `$${t.precio_desde} <span style="font-size:0.9rem; font-weight:600; color:#fff;">USD</span>`;
      }

      const durSidebar = document.querySelector('.tour-page-grid span[style*="border-radius:8px"]');
      if (durSidebar) {
        durSidebar.textContent = durText;
      }

      // Features list in sidebar
      const featList = document.querySelector('.tour-page-grid ul[style*="list-style:none"]');
      if (featList) {
        const items = featList.querySelectorAll('li');
        if (items[0] && t.temporada) items[0].innerHTML = `<i class="fas fa-check-circle" style="color:var(--a, #2dd4bf);"></i> Season: ${t.temporada}`;
        if (items[1]) items[1].innerHTML = `<i class="fas fa-check-circle" style="color:var(--a, #2dd4bf);"></i> Group Size: ${capText}`;
        if (items[2]) items[2].innerHTML = `<i class="fas fa-check-circle" style="color:var(--a, #2dd4bf);"></i> Difficulty: ${difText}`;
      }

      // 5. Descriptions
      const overviewP = document.querySelector('.tour-page-grid p[style*="font-size: 1.1rem"]');
      if (overviewP && t.descripcion_corta) {
        overviewP.textContent = t.descripcion_corta;
      }

      // 6. Itinerary Day-by-Day (if provided)
      if (Array.isArray(t.itinerario) && t.itinerario.length > 0) {
        const itList = document.querySelector('.itinerary-list');
        if (itList) {
          itList.innerHTML = t.itinerario.map((item, idx) => `
            <div style="background:var(--f); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:24px;">
              <h3 style="color:var(--a, #2dd4bf); font-size:1.25rem; font-weight:700; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
                <i class="far fa-calendar-check" style="font-size:1.1rem;"></i> Day ${item.dia || idx + 1}: ${item.titulo || ''}
              </h3>
              <p style="color:rgba(255,255,255,0.85); font-size:1rem; line-height:1.75; margin:0;">
                ${item.descripcion || item.texto || ''}
              </p>
            </div>
          `).join('');
        }
      }
    } catch (e) {
      console.warn('Tour sync error:', e);
    }
  }

  async function syncHomePage() {
    const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html') || window.location.pathname === '';
    if (!isHome) return;

    try {
      const fetchOpts = { cache: 'no-store' };
      const ts = Date.now();
      let hRes = await fetch('/api/content/home?t=' + ts, fetchOpts).then(r => r.ok ? r.json() : null).catch(() => null);
      if (!hRes || (!hRes.stats && !hRes.about_section && !hRes.wildlife_section && !hRes.data)) {
        hRes = await fetch('/data/home.json?t=' + ts, fetchOpts).then(r => r.ok ? r.json() : null).catch(() => null);
      }
      const hData = (hRes && hRes.data) ? hRes.data : (hRes || {});

      // 1. STATS HYDRATION
      if (hData.stats && Array.isArray(hData.stats)) {
        const statsGrid = document.getElementById('home-stats-grid') || document.querySelector('.st-modern .sg') || document.querySelector('.st .sg');
        if (statsGrid) {
          hData.stats.forEach((s, idx) => {
            const card = statsGrid.querySelector(`[data-stat-idx="${idx}"]`) || statsGrid.children[idx];
            if (card) {
              const sn = card.querySelector('.sn');
              const sl = card.querySelector('.sl');
              if (sl && s.label) sl.textContent = s.label;
              if (sn) {
                if (s.type === 'counter') {
                  const target = parseInt(s.value) || 0;
                  const suffix = s.suffix !== undefined ? s.suffix : '+';
                  sn.dataset.target = target;
                  sn.dataset.suffix = suffix;
                  if (typeof window.animateCounter === 'function') {
                    window.animateCounter(sn);
                  } else {
                    sn.textContent = target + suffix;
                  }
                } else {
                  const cleanVal = String(s.value).replace(/★/g, '').trim();
                  sn.innerHTML = `${cleanVal} <i class="fas fa-star" style="color:var(--teal,#2dd4bf);font-size:0.85em;margin-left:4px;"></i>`;
                }
              }
            }
          });
        }
      }

      // 2. HERO HYDRATION
      const hero = hData.hero;
      if (hero) {
        const heroWrap = document.querySelector('.hb') || document.querySelector('.hero');
        if (heroWrap) {
          const ht = heroWrap.querySelector('.ht');
          if (ht && hero.location_tag) {
            ht.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${hero.location_tag}`;
          }
          const h1 = heroWrap.querySelector('.h1');
          if (h1 && hero.title) {
            const emp = hero.title_emphasis ? `<br><em>${hero.title_emphasis}</em>` : '';
            h1.innerHTML = `${hero.title}${emp}`;
          }
          const hs = heroWrap.querySelector('.hs');
          if (hs && hero.subtitle) hs.textContent = hero.subtitle;
        }
      }

      // 3. ABOUT SECTION HYDRATION
      const ab = hData.about_section;
      if (ab) {
        const aboutSec = document.getElementById('about');
        if (aboutSec) {
          const ey = aboutSec.querySelector('.spt .ey');
          if (ey && ab.eyebrow) ey.textContent = ab.eyebrow;
          const t = aboutSec.querySelector('.spt .h2');
          if (t && ab.title) t.textContent = ab.title;
          if (ab.paragraphs && Array.isArray(ab.paragraphs)) {
            const ps = aboutSec.querySelectorAll('.spt p.ld');
            ab.paragraphs.forEach((pObj, pIdx) => {
              const pText = typeof pObj === 'string' ? pObj : pObj.text;
              if (ps[pIdx] && pText) {
                ps[pIdx].textContent = pText;
              }
            });
          }
          const img = aboutSec.querySelector('.spi img');
          if (img && ab.image) {
            img.src = fixImgPath(ab.image);
            if (ab.image_alt) {
              img.alt = ab.image_alt;
              img.title = ab.image_alt;
            }
          }
          const cap = aboutSec.querySelector('.spi .caption-text');
          if (cap && (ab.image_caption || ab.image_alt)) {
            cap.textContent = ab.image_caption || ab.image_alt;
          }
        }
      }

      // 4. WILDLIFE SECTION HYDRATION
      const wl = hData.wildlife_section || hData.wildlife_encounters;
      if (wl) {
        const wlSec = document.getElementById('wildlife');
        if (wlSec) {
          const ey = wlSec.querySelector('.ey');
          if (ey && wl.eyebrow) ey.textContent = wl.eyebrow;
          const t = wlSec.querySelector('.h2');
          if (t && wl.title) t.textContent = wl.title;
          const p = wlSec.querySelector('.ld') || wlSec.querySelector('.lead');
          if (p && wl.text) p.textContent = wl.text;
          const img = wlSec.querySelector('.wl-img-card img') || wlSec.querySelector('img');
          if (img && wl.image) {
            img.src = fixImgPath(wl.image);
            if (wl.image_alt) {
              img.alt = wl.image_alt;
              img.title = wl.image_alt;
            }
          }
          const cap = wlSec.querySelector('.wl-caption span span');
          if (cap && wl.image_alt) {
            cap.textContent = wl.image_alt;
          }
        }
      }
    } catch(e) {
      console.warn('Home sync error:', e);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncSiteData);
  } else {
    syncSiteData();
  }
})();
