import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'www.hiddenjunglecusco.com/admin/index.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Patch viewTours
text = text.replace(
    '<p class="pt">🌿 Tours</p><p class="ps">${ts.length} tours registrados</p>',
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px"><div><p class="pt">🌿 Tours</p><p class="ps">${ts.length} tours registrados</p></div><button class="btn-primary" onclick="editTour(-1)">+ Nuevo Tour</button></div>'
)

# Patch editTour signature and logic
edit_tour_old = """window.editTour = function(idx) {
  const t=cData.tours[idx];"""
edit_tour_new = """window.editTour = function(idx) {
  const t= idx === -1 ? {nombre:'', estado:'activo', categoria:'wildlife', duracion_dias:1, duracion_noches:0, precio_desde:0, capacidad_min:1, capacidad_max:12, dificultad:'Fácil', temporada:'', descripcion_corta:'', descripcion_larga:'', imagen_hero:'', galeria:[], itinerario:[], incluye:[], no_incluye:[], destacado:false} : cData.tours[idx];"""
text = text.replace(edit_tour_old, edit_tour_new)

edit_tour_save_old = """cData.tours[idx]={...t,nombre:v('t-n'),estado:v('t-e'),categoria:v('t-c'),
      duracion_dias:+v('t-d'),duracion_noches:+v('t-dn'),precio_desde:+v('t-p'),
      capacidad_min:+v('t-cmin'),capacidad_max:+v('t-cmax'),
      dificultad:v('t-dif'),temporada:v('t-tmp'),
      destacado:document.getElementById('t-dest').checked,
      imagen_hero:v('t-img'),imagen_alt:v('t-imgalt'),
      descripcion_corta:v('t-dc'),descripcion_larga:document.getElementById('t-dl').value};
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update tour: ${t.nombre}`);"""

edit_tour_save_new = """const updated = {...t,nombre:v('t-n'),estado:v('t-e'),categoria:v('t-c'),
      duracion_dias:+v('t-d'),duracion_noches:+v('t-dn'),precio_desde:+v('t-p'),
      capacidad_min:+v('t-cmin'),capacidad_max:+v('t-cmax'),
      dificultad:v('t-dif'),temporada:v('t-tmp'),
      destacado:document.getElementById('t-dest').checked,
      imagen_hero:v('t-img'),imagen_alt:v('t-imgalt'),
      descripcion_corta:v('t-dc'),descripcion_larga:document.getElementById('t-dl').value};
    if (idx === -1) {
        if(!updated.id) updated.id = 'tour-' + Date.now();
        if(!updated.slug) updated.slug = updated.nombre.toLowerCase().replace(/[^a-z0-9-]/g,'-');
        cData.tours.unshift(updated);
    } else {
        cData.tours[idx] = updated;
    }
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update tour: ${updated.nombre}`);"""
text = text.replace(edit_tour_save_old, edit_tour_save_new)

# Patch viewDeps
text = text.replace(
    '<p class="pt">📅 Salidas Programadas</p><p class="ps">${ts.length} fechas</p>',
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px"><div><p class="pt">📅 Salidas Programadas</p><p class="ps">${ts.length} fechas</p></div><button class="btn-primary" onclick="editDep(-1)">+ Nueva Salida</button></div>'
)

edit_dep_old = """window.editDep = function(idx) {
  const t=cData.salidas[idx];"""
edit_dep_new = """window.editDep = function(idx) {
  const t= idx === -1 ? {tour_nombre:'', fecha_salida:'', fecha_regreso:'', precio:0, plazas_totales:12, plazas_disponibles:12, estado:'disponible', notas:''} : cData.salidas[idx];"""
text = text.replace(edit_dep_old, edit_dep_new)

edit_dep_save_old = """cData.salidas[idx]={...t,tour_nombre:v('d-tn'),fecha_salida:v('d-fs'),
      fecha_regreso:v('d-fr'),precio:+v('d-p'),plazas_totales:+v('d-pt'),
      plazas_disponibles:+v('d-pd'),estado:v('d-e'),notas:v('d-n')};
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update salida: ${t.tour_nombre}`);"""

edit_dep_save_new = """const updated = {...t,tour_nombre:v('d-tn'),fecha_salida:v('d-fs'),
      fecha_regreso:v('d-fr'),precio:+v('d-p'),plazas_totales:+v('d-pt'),
      plazas_disponibles:+v('d-pd'),estado:v('d-e'),notas:v('d-n')};
    if(idx===-1) {
       if(!updated.id) updated.id = 'dep-' + Date.now();
       cData.salidas.unshift(updated);
    } else {
       cData.salidas[idx] = updated;
    }
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update salida: ${updated.tour_nombre}`);"""
text = text.replace(edit_dep_save_old, edit_dep_save_new)

# Patch viewTestims
text = text.replace(
    '<p class="pt">⭐ Testimonios de Clientes</p><p class="ps">${ts.length} testimonios</p>',
    '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px"><div><p class="pt">⭐ Testimonios de Clientes</p><p class="ps">${ts.length} testimonios</p></div><button class="btn-primary" onclick="editTestim(-1)">+ Nuevo Testimonio</button></div>'
)

edit_testim_old = """window.editTestim = function(idx) {
  const t=cData.testimonials[idx];"""
edit_testim_new = """window.editTestim = function(idx) {
  const t= idx === -1 ? {nombre:'', pais:'', bandera:'', tour:'', fecha:'', rating:5, texto:'', foto:'', activo:true} : cData.testimonials[idx];"""
text = text.replace(edit_testim_old, edit_testim_new)

edit_testim_save_old = """cData.testimonials[idx]={...t,nombre:v('tm-n'),pais:v('tm-p'),bandera:v('tm-fl'),
      tour:v('tm-t'),fecha:v('tm-f'),rating:+v('tm-r'),texto:v('tm-tx'),
      foto:v('tm-img'),activo:document.getElementById('tm-a').checked};
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update testimonio: ${t.nombre}`);"""

edit_testim_save_new = """const updated = {...t,nombre:v('tm-n'),pais:v('tm-p'),bandera:v('tm-fl'),
      tour:v('tm-t'),fecha:v('tm-f'),rating:+v('tm-r'),texto:v('tm-tx'),
      foto:v('tm-img'),activo:document.getElementById('tm-a').checked};
    if(idx===-1){
      if(!updated.id) updated.id = Date.now();
      cData.testimonials.unshift(updated);
    } else {
      cData.testimonials[idx] = updated;
    }
    const res=await ghPut(cFile,JSON.stringify(cData,null,2),cSha,`update testimonio: ${updated.nombre}`);"""
text = text.replace(edit_testim_save_old, edit_testim_save_new)


with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Arrays patched!")
