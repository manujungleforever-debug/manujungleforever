import glob, os, re

admin_dirs = ['admin', 'www.manujungleforever.com/admin']

for d in admin_dirs:
    # ── 1. GESTIONAR-SALIDAS.HTML ──
    salidas_file = os.path.join(d, 'gestionar-salidas.html')
    if os.path.exists(salidas_file):
        with open(salidas_file, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # viewPax Costo Base
        c = re.sub(r'\|\s*Costo Base:\s*\$\{s\.precio\s*\|\|\s*0\}', '| Costo Base: $${s.precio || 0} USD', c)
        
        # viewPax Pagado / Saldo
        c = re.sub(r'Pagado:\s*\$\{p\.monto_pagado\|\|0\}\s*\/\s*Saldo:\s*\$\{p\.saldo_pendiente\|\|0\}', 'Pagado: $${p.monto_pagado||0} USD / Saldo: $${p.saldo_pendiente||0} USD', c)
        
        # editPax labels
        c = c.replace('<label>Costo del Tour ($)</label>', '<label>Costo del Tour ($ USD)</label>')
        c = c.replace('<label>Monto Pagado ($)</label>', '<label>Monto Pagado ($ USD)</label>')
        c = c.replace('<label>Saldo Pendiente ($)</label>', '<label>Saldo Pendiente ($ USD)</label>')
        
        # editDep window._toursMap and autofill price
        old_edit_dep_tours = "let toursList = [];\n  try {\n    const toursData = await ghGet('www.manujungleforever.com/data/tours.json');\n    toursList = JSON.parse(toursData.content).tours || [];\n  } catch(e) { console.error('Error load tours', e); }"
        new_edit_dep_tours = """let toursList = [];
  window._toursMap = {};
  try {
    const toursData = await ghGet('www.manujungleforever.com/data/tours.json');
    toursList = JSON.parse(toursData.content).tours || [];
    toursList.forEach(t => {
      if(t.id) window._toursMap[t.id] = t;
      if(t.slug) window._toursMap[t.slug] = t;
    });
  } catch(e) { console.error('Error load tours', e); }"""
        c = c.replace(old_edit_dep_tours, new_edit_dep_tours)
        
        # Replace onchange in #d-tid
        c = re.sub(
            r'<select id="d-tid"[^>]*>',
            '<select id="d-tid" onchange="const t = window._toursMap && (window._toursMap[this.value] || window._toursMap[this.options[this.selectedIndex].value]); if(t) { document.getElementById(\'d-n\').value = t.nombre; if(t.precio_desde) document.getElementById(\'d-p\').value = t.precio_desde; } else { document.getElementById(\'d-n\').value = this.options[this.selectedIndex].text; }">',
            c
        )
        
        # Replace Precio label in editDep
        c = re.sub(r'<label>Precio\s*\(\$\{s\.moneda\|\|\'USD\'\}\)<\/label>', '<label>Precio por persona ($ USD)</label>', c)
        c = re.sub(r'<label>Precio\s*\(USD\)<\/label>', '<label>Precio por persona ($ USD)</label>', c)
        
        # CSV Export header
        c = c.replace('let csv = "Nombre,Nacionalidad,Pasaporte,WhatsApp,Email,Dietas,Medicas,Pagado,Saldo\\n";', 'let csv = "Nombre,Nacionalidad,Pasaporte,WhatsApp,Email,Dietas,Medicas,Costo ($ USD),Pagado ($ USD),Saldo ($ USD)\\n";')
        c = c.replace('let csv = "Nombre,Nacionalidad,Pasaporte,WhatsApp,Email,Dietas,Medicas,Monto Total,Pagado,Saldo\\n";', 'let csv = "Nombre,Nacionalidad,Pasaporte,WhatsApp,Email,Dietas,Medicas,Costo ($ USD),Pagado ($ USD),Saldo ($ USD)\\n";')
        
        with open(salidas_file, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated pricing standardization in {salidas_file}")

    # ── 2. GESTIONAR-TOURS.HTML ──
    tours_file = os.path.join(d, 'gestionar-tours.html')
    if os.path.exists(tours_file):
        with open(tours_file, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # Label in editTour
        c = c.replace('<label>Precio desde (USD)</label>', '<label>Precio desde ($ USD)</label>')
        
        # Sync departures price when tour is saved
        sync_code = """
    // Synchronize departure prices linked to this tour in departures.json
    try {
      const depData = await ghGet('www.manujungleforever.com/data/departures.json');
      if (depData && depData.content) {
        const dJson = JSON.parse(depData.content);
        let depModified = false;
        (dJson.salidas || []).forEach(sal => {
          if (sal.tour_id === updated.id || sal.tour_id === updated.slug) {
            sal.tour_nombre = updated.nombre;
            sal.moneda = 'USD';
            sal.precio = updated.precio_desde;
            depModified = true;
          }
        });
        if (depModified) {
          await ghPut('www.manujungleforever.com/data/departures.json', JSON.stringify(dJson, null, 2), depData.sha, `sync departures price with tour: ${updated.nombre}`);
        }
      }
    } catch(err) {
      console.warn('Could not sync departures with tour price:', err);
    }
"""
        if 'sync departures price with tour' not in c and 'await syncGuidedToursMenuInPages' in c:
            c = c.replace('await syncGuidedToursMenuInPages(cData.tours, MENU_PAGES_TO_SYNC);', 'await syncGuidedToursMenuInPages(cData.tours, MENU_PAGES_TO_SYNC);' + sync_code)
        
        with open(tours_file, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated pricing standardization in {tours_file}")

print("All admin files updated with standardized USD pricing logic.")
