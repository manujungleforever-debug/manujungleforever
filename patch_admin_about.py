import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'www.hiddenjunglecusco.com/admin/index.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

about_func = """
// ─────────────────────────────────────────────────────────────────────────────
// ABOUT US
// ─────────────────────────────────────────────────────────────────────────────
async function viewAbout() {
  const data=await ghGet('www.hiddenjunglecusco.com/data/about.json');
  cFile='www.hiddenjunglecusco.com/data/about.json'; cSha=data.sha;
  const d=JSON.parse(data.content); cData=d;
  set(`
    <p class="pt">ℹ️ Página Sobre Nosotros</p><p class="ps">Contenido de "About Us"</p>
    <div class="eform">
      <div class="esec"><div class="esec-h">General</div>
        <div class="ff"><label>Título de la página</label><input id="ab-t" value="${esc(d.titulo_pagina||'')}"></div>
        <div class="ff"><label>Subtítulo de la página</label><textarea id="ab-s">${esc(d.subtitulo_pagina||'')}</textarea></div>
        ${imgWidget('ab-img','Imagen Hero',d.hero_image||'')}
      </div>
      <div class="esec"><div class="esec-h">Historia</div>
        <div class="grow2">
          <div class="ff"><label>Eyebrow</label><input id="ab-he" value="${esc(d.historia?.eyebrow||'')}"></div>
          <div class="ff"><label>Título</label><input id="ab-ht" value="${esc(d.historia?.titulo||'')}"></div>
        </div>
        <div class="ff"><label>Párrafos (separados por línea en blanco)</label>
          <textarea id="ab-hp" style="min-height:120px">${(d.historia?.paragrafos||[]).join('\\n\\n')}</textarea></div>
        ${imgWidget('ab-himg','Imagen Historia',d.historia?.imagen||'')}
      </div>
      <div class="esec"><div class="esec-h">Misión</div>
        <div class="grow2">
          <div class="ff"><label>Eyebrow</label><input id="ab-me" value="${esc(d.mision?.eyebrow||'')}"></div>
          <div class="ff"><label>Título</label><input id="ab-mt" value="${esc(d.mision?.titulo||'')}"></div>
        </div>
        <div class="ff"><label>Texto</label><textarea id="ab-mtex" style="min-height:80px">${esc(d.mision?.texto||'')}</textarea></div>
      </div>
    </div>`);

  showSaveBar(async()=>{
    const out = JSON.parse(JSON.stringify(cData));
    out.titulo_pagina = v('ab-t');
    out.subtitulo_pagina = v('ab-s');
    out.hero_image = v('ab-img');
    if(!out.historia) out.historia = {};
    out.historia.eyebrow = v('ab-he');
    out.historia.titulo = v('ab-ht');
    out.historia.paragrafos = v('ab-hp').split('\\n\\n').filter(x=>x.trim());
    out.historia.imagen = v('ab-himg');
    if(!out.mision) out.mision = {};
    out.mision.eyebrow = v('ab-me');
    out.mision.titulo = v('ab-mt');
    out.mision.texto = v('ab-mtex');
    
    const res=await ghPut(cFile,JSON.stringify(out,null,2),cSha,`update about.json`);
    cSha=res.sha;
    cData=out;
  });
}
"""

if "async function viewAbout()" not in text:
    text = text.replace('// ─────────────────────────────────────────────────────────────────────────────\n// CONTACT', about_func + '\n// ─────────────────────────────────────────────────────────────────────────────\n// CONTACT')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("viewAbout added.")
else:
    print("viewAbout already exists.")
