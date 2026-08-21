import json, os

tours_path = 'www.manujungleforever.com/data/tours.json'
deps_path = 'www.manujungleforever.com/data/departures.json'

with open(tours_path, 'r', encoding='utf-8') as f:
    tours_data = json.load(f)

with open(deps_path, 'r', encoding='utf-8') as f:
    deps_data = json.load(f)

# Map tour prices
tour_price_map = {}
for t in tours_data.get('tours', []):
    t['moneda'] = 'USD'
    t['precio_desde'] = int(t.get('precio_desde', 0))
    tour_price_map[t.get('id')] = t['precio_desde']
    if t.get('slug'):
        tour_price_map[t.get('slug')] = t['precio_desde']

# Standardize departures
for s in deps_data.get('salidas', []):
    s['moneda'] = 'USD'
    tid = s.get('tour_id')
    # If price is 0 or unassigned, use tour price
    if not s.get('precio') or s.get('precio') == 0:
        if tid in tour_price_map:
            s['precio'] = tour_price_map[tid]
    else:
        s['precio'] = int(s['precio'])

    # Standardize passengers
    for p in s.get('pasajeros', []):
        costo = p.get('costo') or p.get('monto_total') or s.get('precio') or 0
        p['costo'] = int(costo)
        if 'monto_total' in p:
            del p['monto_total'] # Normalize to 'costo'
        
        pagado = p.get('monto_pagado', 0)
        p['monto_pagado'] = int(pagado)
        
        saldo = p.get('saldo_pendiente')
        if saldo is None:
            p['saldo_pendiente'] = max(0, p['costo'] - p['monto_pagado'])
        else:
            p['saldo_pendiente'] = int(saldo)
        
        if p['monto_pagado'] >= p['costo'] and p['costo'] > 0:
            p['estado_pago'] = 'pagado'
        elif p['monto_pagado'] > 0:
            p['estado_pago'] = 'reserva'
        else:
            p['estado_pago'] = 'pendiente'

# Save back to data
with open(tours_path, 'w', encoding='utf-8') as f:
    json.dump(tours_data, f, indent=2, ensure_ascii=False)

with open(deps_path, 'w', encoding='utf-8') as f:
    json.dump(deps_data, f, indent=2, ensure_ascii=False)

print("Standardized tours.json and departures.json with USD pricing.")
