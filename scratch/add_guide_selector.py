import os, re

files = [
    'admin/gestionar-salidas.html',
    'www.manujungleforever.com/admin/gestionar-salidas.html'
]

guide_select_code = """<div class="ff"><label>Guía Asignado</label>
          <select id="d-g" onchange="if(this.value==='__add_new__') addCustomItem('d-g', 'Nombre completo del nuevo guía:')">
            <option value="">-- Sin asignar / Por definir --</option>
            ${(() => {
              const baseGuides = ['Jordy Lonidas Llaqui Chusi', 'Alex Machaca'];
              const existingGuides = (cData?.salidas || []).map(x => (x.guia_asignado || '').trim()).filter(Boolean);
              const currentGuide = (s.guia_asignado || '').trim();
              const allGuides = Array.from(new Set([...baseGuides, ...existingGuides, currentGuide].filter(Boolean))).sort();
              return allGuides.map(g => `<option value="${esc(g)}" ${currentGuide === g ? 'selected' : ''}>${esc(g)}</option>`).join('') +
                     '<option value="__add_new__" style="font-weight:bold;color:#2dd4bf;">+ Añadir nuevo guía...</option>';
            })()}
          </select>
        </div>"""

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Replace plain text input for guia_asignado with select dropdown + add custom option
    c = re.sub(
        r'<div class="ff"><label>Guía Asignado</label><input id="d-g"[^>]*></div>',
        guide_select_code,
        c
    )
    
    # Ensure save handles __add_new__ fallback
    c = re.sub(
        r"guia_asignado:\s*v\('d-g'\)",
        "guia_asignado: v('d-g') === '__add_new__' ? '' : v('d-g')",
        c
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated guide selector in {fpath}")

print("Guide selector successfully added.")
