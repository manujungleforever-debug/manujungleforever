import glob, json, os, re

# 1. Update assets/js/global-sync.js
global_sync_code = """(function() {
  async function syncSiteData() {
    try {
      const isContactPage = window.location.pathname.includes('/contact/') || window.location.pathname.endsWith('/contact');
      
      // Fetch both configs in parallel without cache
      const [gRes, cRes] = await Promise.all([
        fetch('/data/global.json?v=' + Date.now()).catch(() => null),
        fetch('/data/contact.json?v=' + Date.now()).catch(() => null)
      ]);

      const gData = (gRes && gRes.ok) ? await gRes.json() : {};
      const cData = (cRes && cRes.ok) ? await cRes.json() : {};
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
    } catch(err) {
      console.warn('Sync error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncSiteData);
  } else {
    syncSiteData();
  }
})();
"""

with open('www.manujungleforever.com/assets/js/global-sync.js', 'w', encoding='utf-8') as f:
    f.write(global_sync_code)
print("Updated assets/js/global-sync.js with contact.json single source of truth")

# 2. Clean viewGlobal in admin files
clean_view_global = """async function viewGlobal() {
  const data=await ghGet('www.manujungleforever.com/data/global.json');
  cFile='www.manujungleforever.com/data/global.json'; cSha=data.sha;
  const d=JSON.parse(data.content); cData=d;
  set(`
    <div style="display:flex;align-items:center;margin-bottom:15px;"><div class="btn-card-icon card-icon-contenido"><i class="ph ph-gear"></i></div><div><p class="pt" style="margin-bottom:0">Datos Globales del Sitio</p><p class="ps">Información general de marca, redes sociales y SEO</p></div></div>
    <div class="eform">
      <div class="esec"><div class="esec-h">Identidad de Marca</div>
        <div class="grow2">
          <div class="ff"><label>Nombre del negocio</label><input id="g-n" value="${esc(d.site_name||'')}"></div>
          <div class="ff"><label>Eslogan</label><input id="g-sl" value="${esc(d.slogan||'')}"></div>
        </div>
        <div class="ff"><label>Tagline (descripción breve)</label><textarea id="g-tg">${esc(d.tagline||'')}</textarea></div>
      </div>
      <div class="esec"><div class="esec-h">Imágenes del Sitio</div>
        ${imgWidget('g-logo','Logo principal',d.logo_main||'')}
        ${imgWidget('g-fav','Favicon',d.favicon||'')}
      </div>
      <div class="esec"><div class="esec-h">Redes Sociales</div>
        <div class="grow2">
          <div class="ff"><label>Facebook</label><input id="g-fb" value="${esc(d.social?.facebook||d.redes_sociales?.facebook||'')}"></div>
          <div class="ff"><label>Instagram</label><input id="g-ig" value="${esc(d.social?.instagram||d.redes_sociales?.instagram||'')}"></div>
        </div>
        <div class="grow2">
          <div class="ff"><label>TripAdvisor</label><input id="g-ta" value="${esc(d.social?.tripadvisor||d.redes_sociales?.tripadvisor||'')}"></div>
          <div class="ff"><label>YouTube</label><input id="g-yt" value="${esc(d.social?.youtube||'')}"></div>
        </div>
        <div class="grow2">
          <div class="ff"><label>TikTok</label><input id="g-tt" value="${esc(d.social?.tiktok||d.redes_sociales?.tiktok||'')}"></div>
          <div class="ff"><label>Airbnb</label><input id="g-ab" value="${esc(d.social?.airbnb||d.redes_sociales?.airbnb||'')}"></div>
        </div>
      </div>
      <div class="esec"><div class="esec-h">SEO por Defecto</div>
        <div class="ff"><label>Sufijo del título</label><input id="g-ts" value="${esc(d.seo?.default_title_suffix||'')}"><span class="hint">Ej: | Manu Jungle Forever</span></div>
        <div class="ff"><label>Descripción por defecto</label><textarea id="g-td">${esc(d.seo?.default_description||'')}</textarea></div>
        ${imgWidget('g-og','Imagen OG por defecto',d.seo?.default_og_image||'')}
      </div>
      <div class="esec"><div class="esec-h">Copyright</div>
        <div class="ff"><label>Texto de copyright</label><input id="g-cp" value="${esc(d.copyright||'')}"></div>
      </div>
    </div>`);
  showSaveBar(async()=>{
    const dd={...d,site_name:v('g-n'),slogan:v('g-sl'),tagline:v('g-tg'),logo_main:v('g-logo'),favicon:v('g-fav'),copyright:v('g-cp'),
      social:{...d.social,facebook:v('g-fb'),instagram:v('g-ig'),tripadvisor:v('g-ta'),youtube:v('g-yt'),tiktok:v('g-tt'),airbnb:v('g-ab')},
      redes_sociales:{facebook:v('g-fb'),instagram:v('g-ig'),tripadvisor:v('g-ta'),airbnb:v('g-ab'),whatsapp:d.redes_sociales?.whatsapp||'https://wa.me/51901525679',tiktok:v('g-tt')},
      seo:{...d.seo,default_title_suffix:v('g-ts'),default_description:v('g-td'),default_og_image:v('g-og')}};
    const res=await ghPut(cFile,JSON.stringify(dd,null,2),cSha,'update: global');
    cSha=res.sha; cData=dd;
  });
}"""

for f in glob.glob('admin/*.html') + glob.glob('www.manujungleforever.com/admin/*.html'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'async function viewGlobal()' in content:
        content = re.sub(r'async function viewGlobal\(\) \{[\s\S]*?\n\}', clean_view_global, content)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"Streamlined viewGlobal in {f}")
