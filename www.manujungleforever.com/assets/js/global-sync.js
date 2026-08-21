(function() {
  async function syncGlobalSiteData() {
    try {
      const isContactPage = window.location.pathname.includes('/contact/') || window.location.pathname.endsWith('/contact');

      // 1. Fetch global data (no cache)
      const gRes = await fetch('/data/global.json?v=' + Date.now());
      if (!gRes.ok) return;
      const gData = await gRes.json();

      const phone1 = gData.phone_primary || '+51 931 022 183';
      const phone2 = gData.phone_secondary || '+51 901 525 679';
      const email = gData.email || 'discover@manujungleforever.com';
      const address = gData.address || 'Manu Jungle Forever 17800, Nuevo Eden, Peru';
      const addressMaps = gData.address_maps_url || 'https://goo.gl/maps/B8NjhLZizA6YKwKD6';
      const waNum = (gData.whatsapp_number || '51901525679').replace(/[^0-9]/g, '');
      const waTxt = encodeURIComponent(gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');
      const waLink = `https://api.whatsapp.com/send?phone=${waNum}&text=${waTxt}`;
      const waDirect = `https://wa.me/${waNum}`;

      const soc = gData.social || gData.redes_sociales || {};
      const socFb = soc.facebook || '#';
      const socIg = soc.instagram || '#';
      const socTa = soc.tripadvisor || '#';
      const socAb = soc.airbnb || '#';
      const socTt = soc.tiktok || '#';

      // 2. Floating WhatsApp button (class="wa" or id="wa-float")
      document.querySelectorAll('a.wa, #wa-float, a[id="wa-btn"]').forEach(el => {
        el.href = waLink;
      });

      // 3. Sync all WhatsApp links
      document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]').forEach(el => {
        if (el.classList.contains('sc') || el.classList.contains('soc-btn')) {
          // footer/social icon → use direct wa.me link
          el.href = waDirect;
        } else {
          // inline or button → use full link with message text
          el.href = waLink;
        }
      });

      // 4. Sync footer contacts
      const footer = document.querySelector('footer.ft');
      if (footer) {
        // Address
        const addrIcon = footer.querySelector('address.fc i.fa-map-marker-alt, address.fc i.fa-location-dot');
        if (addrIcon) {
          const a = addrIcon.parentElement.querySelector('a');
          if (a) { a.textContent = address; if (addressMaps) a.href = addressMaps; }
        }
        // Phone
        const phoneIcon = footer.querySelector('address.fc i.fa-phone');
        if (phoneIcon) {
          const a = phoneIcon.parentElement.querySelector('a');
          if (a) { a.textContent = phone1; a.href = `tel:${phone1.replace(/[^0-9+]/g, '')}`; }
        }
        // Email
        const emailIcon = footer.querySelector('address.fc i.fa-envelope');
        if (emailIcon) {
          const a = emailIcon.parentElement.querySelector('a');
          if (a) { a.textContent = email; a.href = `mailto:${email}`; }
        }

        // Social Links (.so)
        const elFb = footer.querySelector('.so a[aria-label="Facebook"]');
        if (elFb) elFb.href = socFb;
        const elIg = footer.querySelector('.so a[aria-label="Instagram"]');
        if (elIg) elIg.href = socIg;
        const elTa = footer.querySelector('.so a[aria-label="TripAdvisor"]');
        if (elTa) elTa.href = socTa;
        const elAb = footer.querySelector('.so a[aria-label="Airbnb"]');
        if (elAb) elAb.href = socAb;
        const elWa = footer.querySelector('.so a[aria-label="WhatsApp"]');
        if (elWa) elWa.href = waDirect;
        const elTt = footer.querySelector('.so a[aria-label="TikTok"]');
        if (elTt) elTt.href = socTt;
      }

      // 5. Contact page: also sync from contact.json
      if (isContactPage) {
        try {
          const cRes = await fetch('/data/contact.json?v=' + Date.now());
          if (cRes.ok) {
            const cData = await cRes.json();
            const cp = cData.contacto_principal || {};
            const cEmail = cp.email || email;
            const cT1 = cp.telefono_1 || phone1;
            const cT2 = cp.telefono_2 || phone2;
            const cWaNum = (cp.whatsapp || waNum).replace(/[^0-9]/g, '');
            const cWaTxt = encodeURIComponent(cp.whatsapp_texto || gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');

            const dynPhones = document.getElementById('dyn-contact-phones');
            if (dynPhones) {
              let html = '';
              if (cT1) html += `<a href="tel:${cT1.replace(/[^0-9+]/g, '')}">${cT1}</a><br>`;
              if (cWaNum) {
                html += `<a href="https://api.whatsapp.com/send?phone=${cWaNum}&text=${cWaTxt}" target="_blank" rel="noopener">${cT2 || ('+' + cWaNum)}</a>`;
              } else if (cT2) {
                html += `<a href="tel:${cT2.replace(/[^0-9+]/g, '')}">${cT2}</a>`;
              }
              dynPhones.innerHTML = html;
            }

            const dynEmail = document.getElementById('dyn-contact-email');
            if (dynEmail) { dynEmail.href = `mailto:${cEmail}`; dynEmail.textContent = cEmail; }

            const dir = cData.direccion || {};
            const dynLoc = document.getElementById('dyn-contact-location');
            if (dynLoc && (dir.nombre || dir.localidad || dir.pais)) {
              if (dir.maps_url) dynLoc.href = dir.maps_url;
              const parts = [];
              if (dir.nombre) parts.push(dir.nombre);
              const sub = [dir.calle, dir.localidad, dir.pais].filter(Boolean).join(', ');
              if (sub) parts.push(sub);
              dynLoc.innerHTML = parts.join('<br>');
            }

            const hor = cData.horario || {};
            const dynHours = document.getElementById('dyn-contact-hours');
            if (dynHours && (hor.dias || hor.horas || hor.nota)) {
              let hParts = [];
              if (hor.dias || hor.horas) hParts.push(`<strong>${hor.dias || 'Monday – Sunday'}</strong>: ${hor.horas || '8:00 AM – 8:00 PM (Peru Time)'}`);
              if (hor.nota) hParts.push(`<span style="font-size:0.82rem;color:rgba(255,255,255,0.6)">${hor.nota}</span>`);
              dynHours.innerHTML = hParts.join('<br>');
            }

            // Sync social row in contact page
            const sr = document.querySelector('.social-row');
            if (sr) {
              const elFbc = sr.querySelector('a[aria-label="Facebook"]'); if (elFbc) elFbc.href = socFb;
              const elIgc = sr.querySelector('a[aria-label="Instagram"]'); if (elIgc) elIgc.href = socIg;
              const elTac = sr.querySelector('a[aria-label="TripAdvisor"]'); if (elTac) elTac.href = socTa;
              const elAbc = sr.querySelector('a[aria-label="Airbnb"]'); if (elAbc) elAbc.href = socAb;
              const elWac = sr.querySelector('a[aria-label="WhatsApp"]'); if (elWac) elWac.href = `https://api.whatsapp.com/send?phone=${cWaNum}&text=${cWaTxt}`;
              const elTtc = sr.querySelector('a[aria-label="TikTok"]'); if (elTtc) elTtc.href = socTt;
            }
          }
        } catch(e) { console.warn('Contact sync:', e); }
      }

    } catch(err) {
      console.warn('Global sync error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncGlobalSiteData);
  } else {
    syncGlobalSiteData();
  }
})();
