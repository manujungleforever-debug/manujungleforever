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

      // 1. Floating WhatsApp button
      document.querySelectorAll('a.wa, #wa-float, a[id="wa-btn"]').forEach(el => {
        el.href = waLink;
      });

      // 2. Sync all WhatsApp links
      document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]').forEach(el => {
        if (el.classList.contains('sc') || el.classList.contains('soc-btn')) {
          el.href = waDirect;
        } else {
          el.href = waLink;
        }
      });

      // 3. Sync footer contacts
      const footer = document.querySelector('footer.ft');
      if (footer) {
        // Address link & text
        const addrA = footer.querySelector('address.fc a[href*="maps"]');
        if (addrA) {
          addrA.textContent = addressText;
          if (mapsUrl) addrA.href = mapsUrl;
        }
        // Phone
        const phoneA = footer.querySelector('address.fc a[href^="tel:"]');
        if (phoneA) {
          phoneA.textContent = phone1;
          phoneA.href = `tel:${phone1.replace(/[^0-9+]/g, '')}`;
        }
        // Email
        const emailA = footer.querySelector('address.fc a[href^="mailto:"]');
        if (emailA) {
          emailA.textContent = email;
          emailA.href = `mailto:${email}`;
        }

        // Social Links
        const elFb = footer.querySelector('.so a[aria-label="Facebook"]');
        if (elFb && soc.facebook) elFb.href = soc.facebook;
        const elIg = footer.querySelector('.so a[aria-label="Instagram"]');
        if (elIg && soc.instagram) elIg.href = soc.instagram;
        const elTa = footer.querySelector('.so a[aria-label="TripAdvisor"]');
        if (elTa) elTa.href = soc.tripadvisor || '#';
        const elAb = footer.querySelector('.so a[aria-label="Airbnb"]');
        if (elAb) elAb.href = soc.airbnb || '#';
        const elWa = footer.querySelector('.so a[aria-label="WhatsApp"]');
        if (elWa) elWa.href = waDirect;
        const elTt = footer.querySelector('.so a[aria-label="TikTok"]');
        if (elTt) elTt.href = soc.tiktok || '#';
      }

      // 4. Contact page specifics
      if (isContactPage) {
        if (cData.titulo_pagina) {
          const h1 = document.querySelector('.in-hero .h1');
          if (h1) h1.textContent = cData.titulo_pagina;
        }
        if (cData.subtitulo_pagina) {
          const hs = document.querySelector('.in-hero .hs');
          if (hs) hs.textContent = cData.subtitulo_pagina;
        }
        if (cData.hero_image && !cData.hero_image.includes('placeholder.jpg')) {
          const hero = document.querySelector('.in-hero');
          if (hero) hero.style.backgroundImage = `url('${fixImgPath(cData.hero_image)}')`;
        }

        const dynPhones = document.getElementById('dyn-contact-phones');
        if (dynPhones) {
          let html = '';
          if (phone1) html += `<a href="tel:${phone1.replace(/[^0-9+]/g, '')}">${phone1}</a><br>`;
          if (waNum) {
            html += `<a href="${waLink}" target="_blank" rel="noopener">${phone2 || ('+' + waNum)}</a>`;
          } else if (phone2) {
            html += `<a href="tel:${phone2.replace(/[^0-9+]/g, '')}">${phone2}</a>`;
          }
          dynPhones.innerHTML = html;
        }

        const dynEmail = document.getElementById('dyn-contact-email');
        if (dynEmail) { dynEmail.href = `mailto:${email}`; dynEmail.textContent = email; }

        const dynLoc = document.getElementById('dyn-contact-location');
        if (dynLoc) {
          if (mapsUrl) dynLoc.href = mapsUrl;
          dynLoc.innerHTML = addrParts.join('<br>') || addressText;
        }

        const mapIframe = document.querySelector('.map-container iframe');
        if (mapIframe && dir.maps_embed) {
          mapIframe.src = dir.maps_embed;
        }

        const hor = cData.horario || {};
        const dynHours = document.getElementById('dyn-contact-hours');
        if (dynHours && (hor.dias || hor.horas || hor.nota)) {
          let hParts = [];
          if (hor.dias || hor.horas) hParts.push(`<strong>${hor.dias || 'Monday – Sunday'}</strong>: ${hor.horas || '8:00 AM – 8:00 PM (Peru Time)'}`);
          if (hor.nota) hParts.push(`<span style="font-size:0.82rem;color:rgba(255,255,255,0.6)">${hor.nota}</span>`);
          dynHours.innerHTML = hParts.join('<br>');
        }

        const sr = document.querySelector('.social-row');
        if (sr) {
          const elFbc = sr.querySelector('a[aria-label="Facebook"]'); if (elFbc && soc.facebook) elFbc.href = soc.facebook;
          const elIgc = sr.querySelector('a[aria-label="Instagram"]'); if (elIgc && soc.instagram) elIgc.href = soc.instagram;
          const elTac = sr.querySelector('a[aria-label="TripAdvisor"]'); if (elTac) elTac.href = soc.tripadvisor || '#';
          const elAbc = sr.querySelector('a[aria-label="Airbnb"]'); if (elAbc) elAbc.href = soc.airbnb || '#';
          const elWac = sr.querySelector('a[aria-label="WhatsApp"]'); if (elWac) elWac.href = waLink;
          const elTtc = sr.querySelector('a[aria-label="TikTok"]'); if (elTtc) elTtc.href = soc.tiktok || '#';
        }
      }

      // 5. Individual Tour Page dynamic hydration from D1
      await syncTourPage();
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncSiteData);
  } else {
    syncSiteData();
  }
})();
