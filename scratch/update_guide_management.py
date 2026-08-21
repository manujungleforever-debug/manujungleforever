import json, os, re

# 1. Standardize departures.json guides
deps_path = 'www.manujungleforever.com/data/departures.json'
with open(deps_path, 'r', encoding='utf-8') as f:
    deps_data = json.load(f)

for s in deps_data.get('salidas', []):
    if s.get('guia_asignado') == 'Jordy Llaqui':
        s['guia_asignado'] = 'Jordy Lonidas Llaqui Chusi'

with open(deps_path, 'w', encoding='utf-8') as f:
    json.dump(deps_data, f, indent=2, ensure_ascii=False)
print("Updated departures.json guide names.")

# 2. Update admin/gestionar-salidas.html & www.manujungleforever.com/admin/gestionar-salidas.html
files = [
    'admin/gestionar-salidas.html',
    'www.manujungleforever.com/admin/gestionar-salidas.html'
]

remove_guide_js = """
window.removeCustomGuide = function(selectId) {
  const sel = document.getElementById(selectId);
  if (!sel) return;
  const realOptions = Array.from(sel.options).filter(o => o.value && !o.value.startsWith('__'));
  if (!realOptions.length) {
    alert('No hay guías registrados para eliminar.');
    sel.value = '';
    return;
  }
  const guideListStr = realOptions.map((o, idx) => `${idx + 1}. ${o.value}`).join('\\n');
  setTimeout(function() {
    const choice = prompt(`Escriba el NÚMERO o el NOMBRE del guía que desea eliminar de la lista:\\n\\n${guideListStr}`);
    if (choice && choice.trim()) {
      const cleanChoice = choice.trim();
      let target = null;
      const num = parseInt(cleanChoice, 10);
      if (!isNaN(num) && num >= 1 && num <= realOptions.length) {
        target = realOptions[num - 1].value;
      } else {
        const found = realOptions.find(o => o.value.toLowerCase() === cleanChoice.toLowerCase());
        if (found) target = found.value;
      }
      
      if (target) {
        if (confirm(`¿Eliminar al guía "${target}" de la lista?\\n(Si hay salidas que lo tenían asignado, quedarán sin guía asignado).`)) {
          const optToRemove = Array.from(sel.options).find(o => o.value === target);
          if (optToRemove) optToRemove.remove();
          sel.value = '';
          if (window.cData && window.cData.salidas) {
            window.cData.salidas.forEach(s => {
              if (s.guia_asignado === target) s.guia_asignado = '';
            });
          }
          const saveBar = document.getElementById('save-bar');
          if (saveBar && saveFnRef) saveBar.style.display = 'flex';
          alert(`✓ Guía "${target}" eliminado correctamente.`);
        }
      } else {
        alert('❌ No se encontró el guía especificado.');
      }
    }
    sel.value = '';
  }, 10);
};
"""

guide_select_new = """<div class="ff"><label>Guía Asignado</label>
          <select id="d-g" onchange="if(this.value==='__add_new__') addCustomItem('d-g', 'Nombre completo del nuevo guía:'); else if(this.value==='__remove_guide__') removeCustomGuide('d-g');">
            <option value="">-- Sin asignar / Por definir --</option>
            ${(() => {
              const baseGuides = ['Alex Machaca', 'Jordy Lonidas Llaqui Chusi'];
              const existingGuides = (cData?.salidas || []).map(x => (x.guia_asignado || '').trim()).filter(Boolean);
              const currentGuide = (s.guia_asignado || '').trim();
              const allGuides = Array.from(new Set([...baseGuides, ...existingGuides, currentGuide].filter(Boolean))).sort();
              return allGuides.map(g => `<option value="${esc(g)}" ${currentGuide === g ? 'selected' : ''}>${esc(g)}</option>`).join('') +
                     '<option value="__add_new__" style="font-weight:bold;color:#2dd4bf;">+ Añadir nuevo guía...</option>' +
                     '<option value="__remove_guide__" style="font-weight:bold;color:#ef4444;">- Eliminar un guía de la lista...</option>';
            })()}
          </select>
        </div>"""

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Add removeCustomGuide function if not present
    if 'window.removeCustomGuide' not in c:
        c = c.replace('window.addCustomItem = function', remove_guide_js + '\nwindow.addCustomItem = function')

    # Replace guide selector
    c = re.sub(
        r'<div class="ff"><label>Guía Asignado</label>\s*<select id="d-g"[\s\S]*?<\/select>\s*<\/div>',
        guide_select_new,
        c
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated remove guide logic in {fpath}")

print("Done.")
