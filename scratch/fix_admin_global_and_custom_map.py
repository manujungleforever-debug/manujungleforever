import glob, json, os, re

custom_map_viewer = "https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc"
custom_map_embed = "https://www.google.com/maps/d/embed?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc"

# 1. Update data/global.json
with open('www.manujungleforever.com/data/global.json', 'r', encoding='utf-8') as f:
    gdata = json.load(f)

gdata['address'] = "Manu Jungle Forever 17800, Nuevo Eden, Peru"
gdata['address_maps_url'] = custom_map_viewer
gdata['email'] = gdata.get('email') or "discover@manujungleforever.com"
gdata['phone_primary'] = gdata.get('phone_primary') or "+51 901 525 679"
gdata['phone_secondary'] = gdata.get('phone_secondary') or "+51 931 022 183"
gdata['whatsapp_number'] = gdata.get('whatsapp_number') or "51901525679"

with open('www.manujungleforever.com/data/global.json', 'w', encoding='utf-8') as f:
    json.dump(gdata, f, indent=2, ensure_ascii=False)
print("Updated data/global.json with custom map viewer URL")

# 2. Update data/contact.json
with open('www.manujungleforever.com/data/contact.json', 'r', encoding='utf-8') as f:
    cdata = json.load(f)

if 'direccion' not in cdata: cdata['direccion'] = {}
cdata['direccion']['maps_url'] = custom_map_viewer
cdata['direccion']['maps_embed'] = custom_map_embed

with open('www.manujungleforever.com/data/contact.json', 'w', encoding='utf-8') as f:
    json.dump(cdata, f, indent=2, ensure_ascii=False)
print("Updated data/contact.json with custom map viewer & embed URLs")

# 3. Update data/home.json
if os.path.exists('www.manujungleforever.com/data/home.json'):
    with open('www.manujungleforever.com/data/home.json', 'r', encoding='utf-8') as f:
        hdata = json.load(f)
    hdata['map_embed_url'] = custom_map_embed
    with open('www.manujungleforever.com/data/home.json', 'w', encoding='utf-8') as f:
        json.dump(hdata, f, indent=2, ensure_ascii=False)
    print("Updated data/home.json with custom map embed URL")

# 4. Update assets/js/global-sync.js
global_sync_code = f"""(function() {{
  async function syncGlobalSiteData() {{
    try {{
      const isContactPage = window.location.pathname.includes('/contact/') || window.location.pathname.endsWith('/contact');

      // 1. Fetch global data
      const gRes = await fetch('/data/global.json?v=' + Date.now());
      if (!gRes.ok) return;
      const gData = await gRes.json();

      const phone1 = gData.phone_primary || '+51 901 525 679';
      const phone2 = gData.phone_secondary || '';
      const email = gData.email || 'discover@manujungleforever.com';
      const address = gData.address || 'Manu Jungle Forever 17800, Nuevo Eden, Peru';
      const addressMaps = gData.address_maps_url || '{custom_map_viewer}';
      const waNum = (gData.whatsapp_number || '51901525679').replace(/[^0-9]/g, '');
      const waTxt = encodeURIComponent(gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');
      const waLink = `https://api.whatsapp.com/send?phone=${{waNum}}&text=${{waTxt}}`;
      const waDirect = `https://wa.me/${{waNum}}`;

      const soc = gData.social || gData.redes_sociales || {{}};

      // 2. Floating WhatsApp button
      document.querySelectorAll('a.wa, #wa-float, a[id="wa-btn"]').forEach(el => {{
        el.href = waLink;
      }});

      // 3. Sync all WhatsApp links
      document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]').forEach(el => {{
        if (el.classList.contains('sc') || el.classList.contains('soc-btn')) {{
          el.href = waDirect;
        }} else {{
          el.href = waLink;
        }}
      }});

      // 4. Sync footer contacts
      const footer = document.querySelector('footer.ft');
      if (footer) {{
        // Address link & text
        const addrA = footer.querySelector('address.fc a[href*="maps"]');
        if (addrA) {{
          addrA.textContent = address;
          if (addressMaps) addrA.href = addressMaps;
        }}
        // Phone
        const phoneA = footer.querySelector('address.fc a[href^="tel:"]');
        if (phoneA) {{
          phoneA.textContent = phone1;
          phoneA.href = `tel:${{phone1.replace(/[^0-9+]/g, '')}}`;
        }}
        // Email
        const emailA = footer.querySelector('address.fc a[href^="mailto:"]');
        if (emailA) {{
          emailA.textContent = email;
          emailA.href = `mailto:${{email}}`;
        }}

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
      }}

      // 5. Contact page
      if (isContactPage) {{
        try {{
          const cRes = await fetch('/data/contact.json?v=' + Date.now());
          if (cRes.ok) {{
            const cData = await cRes.json();
            const cp = cData.contacto_principal || {{}};
            const cEmail = cp.email || email;
            const cT1 = cp.telefono_1 || phone1;
            const cT2 = cp.telefono_2 || phone2;
            const cWaNum = (cp.whatsapp || waNum).replace(/[^0-9]/g, '');
            const cWaTxt = encodeURIComponent(cp.whatsapp_texto || gData.whatsapp_text || 'Hello! I would like to learn more about your jungle trips');

            const dynPhones = document.getElementById('dyn-contact-phones');
            if (dynPhones) {{
              let html = '';
              if (cT1) html += `<a href="tel:${{cT1.replace(/[^0-9+]/g, '')}}">${{cT1}}</a><br>`;
              if (cWaNum) {{
                html += `<a href="https://api.whatsapp.com/send?phone=${{cWaNum}}&text=${{cWaTxt}}" target="_blank" rel="noopener">${{cT2 || ('+' + cWaNum)}}</a>`;
              }} else if (cT2) {{
                html += `<a href="tel:${{cT2.replace(/[^0-9+]/g, '')}}">${{cT2}}</a>`;
              }}
              dynPhones.innerHTML = html;
            }}

            const dynEmail = document.getElementById('dyn-contact-email');
            if (dynEmail) {{ dynEmail.href = `mailto:${{cEmail}}`; dynEmail.textContent = cEmail; }}

            const dir = cData.direccion || {{}};
            const dynLoc = document.getElementById('dyn-contact-location');
            if (dynLoc) {{
              const mapsUrl = dir.maps_url || addressMaps;
              if (mapsUrl) dynLoc.href = mapsUrl;
              const parts = [];
              if (dir.nombre) parts.push(dir.nombre);
              const sub = [dir.calle, dir.localidad, dir.pais].filter(Boolean).join(', ');
              if (sub) parts.push(sub);
              dynLoc.innerHTML = parts.join('<br>') || address;
            }}

            const mapIframe = document.querySelector('.map-container iframe');
            if (mapIframe && dir.maps_embed) {{
              mapIframe.src = dir.maps_embed;
            }}
          }}
        }} catch(e) {{}}
      }}
    }} catch(err) {{
      console.warn('Global sync error:', err);
    }}
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', syncGlobalSiteData);
  }} else {{
    syncGlobalSiteData();
  }}
}})();
"""

with open('www.manujungleforever.com/assets/js/global-sync.js', 'w', encoding='utf-8') as f:
    f.write(global_sync_code)
print("Updated assets/js/global-sync.js")

# 5. Update ALL public HTML files with custom map viewer and embed URLs
html_files = [f for f in glob.glob('www.manujungleforever.com/**/*.html', recursive=True) if '/admin/' not in f.replace('\\', '/')]

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    c = c.replace('https://maps.google.com/?q=Nuevo+Eden,+Madre+de+Dios,+Peru', custom_map_viewer)
    c = c.replace('https://www.google.com/maps?q=Nuevo+Eden,+Madre+de+Dios,+Peru&output=embed', custom_map_embed)
    c = c.replace('https://www.google.com/maps?q=Nuevo+Eden,+Madre+de+Dios,+Peru&amp;output=embed', custom_map_embed)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

print(f"Updated all {len(html_files)} public HTML files to custom map URLs.")
