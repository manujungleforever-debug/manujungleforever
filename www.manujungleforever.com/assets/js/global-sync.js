(function() {
  async function syncGlobalSiteData() {
    try {
      const isContactPage = window.location.pathname.includes('/contact/') || window.location.pathname.endsWith('/contact');

      // 1. Fetch global data
      const gRes = await fetch('/data/global.json?v=' + Date.now());
      if (!gRes.ok) return;
      const gData = await gRes.json();

      const phone1 = gData.phone_primary || '+51 901 525 679';
      const phone2 = gData.phone_secondary || '';
      const email = gData.email || 'discover@manujungleforever.com';
      const address = gData.address || 'Manu Jungle Forever 17800, Nuevo Eden, Peru';
      const addressMaps = gData.address_maps_url || 'https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc';
      const waNum = (gData.whatsapp_number || '51901525679').replace(/[^0-9]/g, '');
      const waTxt = encodeURIComponent(gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');
      const waLink = `https://api.whatsapp.com/send?phone=${waNum}&text=${waTxt}`;
      const waDirect = `https://wa.me/${waNum}`;

      const soc = gData.social || gData.redes_sociales || {};

      // 2. Floating WhatsApp button
      document.querySelectorAll('a.wa, #wa-float, a[id="wa-btn"]').forEach(el => {
        el.href = waLink;
      });

      // 3. Sync all WhatsApp links
      document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]').forEach(el => {
        if (el.classList.contains('sc') || el.classList.contains('soc-btn')) {
          el.href = waDirect;
        } else {
          el.href = waLink;
        }
      });

      // 4. Sync footer contacts
      const footer = document.querySelector('footer.ft');
      if (footer) {
        // Address link & text
        const addrA = footer.querySelector('address.fc a[href*="maps"]');
        if (addrA) {
          addrA.textContent = address;
          if (addressMaps) addrA.href = addressMaps;
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

      // 5. Contact page
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
            if (dynLoc) {
              const mapsUrl = dir.maps_url || addressMaps;
              if (mapsUrl) dynLoc.href = mapsUrl;
              const parts = [];
              if (dir.nombre) parts.push(dir.nombre);
              const sub = [dir.calle, dir.localidad, dir.pais].filter(Boolean).join(', ');
              if (sub) parts.push(sub);
              dynLoc.innerHTML = parts.join('<br>') || address;
            }

            const mapIframe = document.querySelector('.map-container iframe');
            if (mapIframe && dir.maps_embed) {
              mapIframe.src = dir.maps_embed;
            }
          }
        } catch(e) {}
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
