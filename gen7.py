import os, re

INDEX = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin\index.html"
OUT   = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\admin"

with open(INDEX, "r", encoding="utf-8") as f:
    raw = f.read()

m_start = re.search(r'<script>\r?\n(const API\s*=)', raw)
start_idx = m_start.start(1)
m_end = re.search(r'</script>', raw[start_idx:])
end_idx = start_idx + m_end.start()
CMS_JS = raw[start_idx:end_idx]

def clean_js(js, section_id):
    js = js.replace("let cSection = 'blog'", f"let cSection = '{section_id}'")
    login_idx = js.find("// LOGIN / LOGOUT")
    api_idx = js.find("// API WRAPPERS")
    if login_idx != -1 and api_idx != -1 and api_idx > login_idx:
        js = js[:login_idx] + js[api_idx:]
    for pat in [r"^const API\s*=.*\r?\n",r"^const MEDIA_API\s*=.*\r?\n",r"^let token\s*=.*\r?\n",r"^let cUser\s*=.*\r?\n",r"^let cSection\s*=.*\r?\n",r"^let saveFnRef\s*=.*\r?\n"]:
        js = re.sub(pat, "", js, flags=re.MULTILINE)
    for fn in ["buildTopNav","buildSidebar","switchSection","showSaveBar","hideSaveBar","set","openModal","closeModal"]:
        js = re.sub(rf"\bfunction {fn}\b", f"function {fn}_DIS", js)
    return js.strip()

ALL_NAV = [
    ("gestionar-tours.html","ph-map-trifold","Tours","tours"),
    ("gestionar-blog.html","ph-pencil","Blog","blog"),
    ("gestionar-contenido.html","ph-file-text","Contenido","content"),
    ("gestionar-salidas.html","ph-calendar","Salidas","departures"),
    ("gestionar-testimonios.html","ph-star","Testimonios","testimonials"),
    ("gestionar-reclamos.html","ph-scales","Reclamos",None),
    ("gestionar-medios.html","ph-image","Medios","media"),
]

def nav_html(active_sid):
    parts = []
    for href,icon,label,sid in ALL_NAV:
        cls = ' class="active"' if sid == active_sid else ""
        parts.append(f'<a href="{href}"{cls}><i class="ph {icon}"></i> {label}</a>')
    return "\n      ".join(parts)

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
    --bg: #030807; --bg-grad: radial-gradient(ellipse at 50% 0%, #0a2e25 0%, #030807 70%);
    --hbg: rgba(3,8,7,0.9); --card: rgba(11,38,35,0.50); --bdr: rgba(45,212,191,0.14);
    --bdr-h: rgba(45,212,191,0.45); --fg: #f1f5f9; --muted: #94a3b8; --teal: #2dd4bf;
    --teal-g: rgba(45,212,191,0.28); --gold: #c9a84c; --gold-g: rgba(201,168,76,0.28);
    --danger: #ef4444; --green: #10b981; --surface: rgba(11,38,35,0.6);
    --border: rgba(45,212,191,0.14); --text: #f1f5f9; --w: #f1f5f9; --card2: rgba(20,50,40,0.5);
}
html,body { height:100%; font-family:'Poppins',sans-serif; }
body { background: var(--bg) var(--bg-grad); color: var(--fg); min-height:100vh; display:flex; flex-direction:column; overflow-x:hidden; opacity:0; transition:opacity .3s; }
input,textarea,select,button { font-family:inherit; }
a { color:var(--teal); }
header { position:sticky; top:0; z-index:200; background:var(--hbg); backdrop-filter:blur(14px); border-bottom:1px solid rgba(255,255,255,0.07); box-shadow:0 4px 24px rgba(0,0,0,.4); }
.hw { max-width:1400px; margin:0 auto; padding:10px 24px; display:flex; align-items:center; gap:14px; flex-wrap:wrap; }
.logo-brand { display:flex; align-items:center; gap:10px; text-decoration:none; flex-shrink:0; }
.logo-wrap  { position:relative; display:flex; align-items:center; }
.logo-glow  { position:absolute; inset:-5px; background:var(--teal); filter:blur(12px); opacity:.22; border-radius:50%; transition:.3s; }
.logo-brand:hover .logo-glow { opacity:.5; filter:blur(18px); }
.logo-wrap img { height:40px; width:auto; position:relative; z-index:2; }
.brand-name { font-weight:700; font-size:.9rem; letter-spacing:2px; text-transform:uppercase; background:linear-gradient(to right,var(--teal),var(--gold)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.btn-panel { display:inline-flex; align-items:center; gap:8px; background:rgba(45,212,191,0.12); border:1px solid rgba(45,212,191,0.3); color:var(--teal); padding:8px 18px; border-radius:10px; font-size:.83rem; font-weight:700; text-decoration:none; white-space:nowrap; transition:.25s; flex-shrink:0; }
.btn-panel:hover { background:var(--teal); color:#030807; box-shadow:0 0 14px var(--teal-g); }
nav.mnav { display:flex; align-items:center; gap:3px; flex-wrap:wrap; flex:1; }
nav.mnav a { font-size:.8rem; font-weight:500; color:var(--muted); text-decoration:none; padding:6px 11px; border-radius:8px; transition:.25s; white-space:nowrap; display:flex; align-items:center; gap:5px; }
nav.mnav a i { font-size:1.1rem; }
nav.mnav a:hover, nav.mnav a.active { color:var(--teal); background:rgba(45,212,191,.09); }
.user-sec { display:flex; align-items:center; gap:10px; margin-left:auto; }
.btn-logout { background:rgba(239,68,68,.08); border:1px solid rgba(239,68,68,.2); color:#f87171; cursor:pointer; font-size:.8rem; font-weight:600; padding:6px 12px; border-radius:8px; transition:.25s; display:flex; align-items:center; gap:6px; }
.btn-logout:hover { background:var(--danger); color:#fff; border-color:var(--danger); }
main { flex-grow:1; max-width:1400px; width:100%; margin:0 auto; padding:28px 24px 100px; position:relative; z-index:1; }
.pt { font-size:1.85rem; font-weight:700; letter-spacing:-.4px; background:linear-gradient(to right,#fff,#cbd5e1); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:4px; }
.ps { color:var(--muted); font-size:.87rem; margin-bottom:20px; }
.back-btn { display:inline-flex; align-items:center; gap:7px; background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1); color:var(--fg); padding:8px 16px; border-radius:9px; font-size:.82rem; font-weight:600; cursor:pointer; transition:.25s; margin-bottom:20px; }
.back-btn:hover { background:rgba(255,255,255,.12); }
.btn-primary { background:var(--teal); color:#030807; border:none; padding:9px 20px; border-radius:10px; font-weight:700; font-size:.83rem; cursor:pointer; display:inline-flex; align-items:center; gap:7px; transition:.25s; }
.btn-primary:hover { background:#16c9b5; box-shadow:0 0 14px var(--teal-g); }
.btn-primary:disabled { opacity:.5; cursor:not-allowed; }
.btn-secondary { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.09); color:var(--fg); padding:8px 17px; border-radius:10px; font-size:.82rem; font-weight:600; cursor:pointer; display:inline-flex; align-items:center; gap:6px; transition:.25s; }
.btn-secondary:hover { background:rgba(255,255,255,.11); }
.btn-danger { background:rgba(239,68,68,.08); border:1px solid rgba(239,68,68,.22); color:#f87171; padding:7px 15px; border-radius:9px; cursor:pointer; font-weight:600; font-size:.82rem; transition:.25s; }
.btn-danger:hover { background:var(--danger); color:#030807; border-color:var(--danger); }
.btn-edit { background:rgba(45,212,191,.09); border:1px solid rgba(45,212,191,.22); color:var(--teal); padding:7px 15px; border-radius:9px; cursor:pointer; font-weight:600; font-size:.82rem; transition:.25s; }
.btn-edit:hover { background:var(--teal); color:#030807; }
.list-grid, .blog-grid { display:grid; gap:12px; width:100%; box-sizing:border-box; }
.li, .blog-card-li { background:var(--card); backdrop-filter:blur(8px); border:1px solid var(--bdr); border-radius:14px; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; gap:14px; width:100%; box-sizing:border-box; transition:all .25s ease; overflow:hidden; }
.li:hover, .blog-card-li:hover { border-color:var(--bdr-h); transform:translateY(-1px); box-shadow:0 8px 24px rgba(45,212,191,.06); }
.blog-thumb { width:96px; height:66px; flex-shrink:0; border-radius:10px; overflow:hidden; background:#000; border:1px solid rgba(45,212,191,.25); }
.blog-thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.li-info { flex:1 1 0%; min-width:0; overflow:hidden; }
.li-info h3 { font-size:.95rem; font-weight:600; color:var(--fg); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.li-info span { font-size:.76rem; color:var(--muted); display:block; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.li-actions { display:flex; gap:8px; align-items:center; flex-shrink:0; }
.badge { display:inline-block; padding:3px 11px; border-radius:20px; font-size:.68rem; font-weight:700; margin-left:6px; text-transform:uppercase; }
.badge.on  { background:rgba(16,185,129,.15); color:#34d399; border:1px solid rgba(16,185,129,.25); }
.badge.off { background:rgba(239,68,68,.18);  color:#f87171; border:1px solid rgba(239,68,68,.3); }
.badge.warn{ background:rgba(245,158,11,.18); color:#fbbf24; border:1px solid rgba(245,158,11,.3); }
.eform { max-width:900px; display:flex; flex-direction:column; gap:17px; margin-bottom:60px; }
.esec { background:var(--card); backdrop-filter:blur(10px); border:1px solid var(--bdr); border-radius:16px; padding:22px; }
.esec-h { font-size:.7rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--gold); border-bottom:1px solid rgba(255,255,255,.07); padding-bottom:8px; margin-bottom:16px; }
.grow2 { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.grow3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; }
.ff { display:flex; flex-direction:column; gap:6px; margin-bottom:12px; }
.ff label { font-size:.7rem; font-weight:600; text-transform:uppercase; letter-spacing:.8px; color:var(--muted); }
.ff input,.ff textarea,.ff select { background:rgba(3,8,7,.65); border:1px solid rgba(255,255,255,.1); color:var(--fg); padding:10px 13px; border-radius:10px; font-size:.85rem; outline:none; transition:.25s; width:100%; }
.ff input:focus,.ff textarea:focus,.ff select:focus { border-color:var(--teal); box-shadow:0 0 10px var(--teal-g); }
.ff select option { background:#0a1f1b; color:var(--fg); }
.hint { font-size:.7rem; color:var(--muted); }
.save-bar { position:fixed; bottom:0; left:0; right:0; background:rgba(3,8,7,.96); backdrop-filter:blur(16px); border-top:1px solid rgba(45,212,191,.3); padding:14px 28px; display:flex; align-items:center; justify-content:flex-end; gap:12px; z-index:99999; box-shadow:0 -8px 32px rgba(0,0,0,0.8); }
.save-status { font-size:.83rem; color:var(--muted); margin-right:auto; font-weight:500; }
.save-status.ok  { color:var(--green); }
.save-status.err { color:var(--danger); }
.md-wrap { border:1px solid rgba(255,255,255,.1); border-radius:10px; overflow:hidden; }
.md-toolbar { background:rgba(0,0,0,.22); border-bottom:1px solid rgba(255,255,255,.07); padding:6px; display:flex; gap:5px; flex-wrap:wrap; }
.md-toolbar button { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.08); color:var(--fg); padding:5px 10px; border-radius:5px; cursor:pointer; font-size:.76rem; transition:.25s; }
.md-toolbar button:hover { background:var(--teal); color:#030807; }
.tgl-wrap { display:flex; align-items:center; gap:10px; }
.tgl { position:relative; display:inline-block; width:44px; height:24px; }
.tgl input { opacity:0; width:0; height:0; }
.tgl-s { position:absolute; inset:0; background:rgba(255,255,255,.1); border-radius:24px; transition:.3s; cursor:pointer; }
.tgl-s:before { content:''; position:absolute; height:18px; width:18px; left:3px; bottom:3px; background:#fff; border-radius:50%; transition:.3s; }
.tgl input:checked+.tgl-s { background:var(--teal); }
.tgl input:checked+.tgl-s:before { transform:translateX(20px); }
.img-field-wrap { display:flex; flex-direction:column; gap:6px; }
.img-input-row { display:flex; gap:8px; }
.img-input-row input { flex:1; }
.img-preview { width:100%; max-height:420px; min-height:200px; object-fit:contain; background:rgba(0,0,0,.45); border-radius:12px; margin-top:10px; padding:8px; border:1px dashed rgba(45,212,191,0.3); box-shadow:inset 0 0 20px rgba(0,0,0,0.5); display:none; }
.img-preview.show { display:block; }
.avatar-preview { width:120px; height:120px; object-fit:cover; object-position:center; border-radius:50%; margin-top:10px; border:2px solid var(--teal); box-shadow:0 4px 14px rgba(45,212,191,0.25); display:none; }
.avatar-preview.show { display:block; }
.sub-nav-tabs { display:flex; gap:7px; margin-bottom:22px; background:var(--card); padding:6px; border-radius:11px; border:1px solid var(--bdr); width:fit-content; }
.sub-nav-tabs button { background:none; border:none; color:var(--muted); padding:7px 15px; border-radius:8px; font-size:.82rem; font-weight:600; cursor:pointer; transition:.25s; }
.sub-nav-tabs button:hover,.sub-nav-tabs button.active { background:rgba(45,212,191,.12); color:var(--teal); }
.modal-bg { position:fixed; inset:0; background:rgba(2,6,5,.9); backdrop-filter:blur(7px); align-items:center; justify-content:center; z-index:400; display:none; padding:20px; }
.modal-bg.open { display:flex !important; }
.modal { background:rgba(11,38,35,.8); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,.12); border-radius:18px; width:100%; max-width:600px; max-height:88vh; display:flex; flex-direction:column; box-shadow:0 24px 56px rgba(0,0,0,.6); }
.modal.lg { max-width:920px; }
.modal-h { padding:16px 22px; border-bottom:1px solid rgba(255,255,255,.08); display:flex; align-items:center; justify-content:space-between; background:rgba(0,0,0,.14); border-radius:18px 18px 0 0; }
.modal-h h3 { font-size:.98rem; font-weight:700; color:var(--teal); }
.modal-body { padding:20px 22px; overflow-y:auto; display:flex; flex-direction:column; gap:13px; }
.modal-actions { padding:12px 22px; border-top:1px solid rgba(255,255,255,.08); background:rgba(0,0,0,.14); display:flex; justify-content:flex-end; gap:10px; align-items:center; border-radius:0 0 18px 18px; }
.loading { display:flex; align-items:center; gap:11px; color:var(--muted); font-size:.87rem; padding:28px 0; }
.spinner { width:20px; height:20px; border-radius:50%; border:2px solid rgba(45,212,191,.2); border-top-color:var(--teal); animation:spin .8s linear infinite; flex-shrink:0; }
@keyframes spin { to { transform:rotate(360deg); } }
.media-grid,.m-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(118px,1fr)); gap:8px; }
.media-item,.m-item { background:var(--card); border:2px solid var(--bdr); border-radius:9px; overflow:hidden; cursor:pointer; transition:.25s; position:relative; }
.media-item:hover,.m-item:hover { border-color:var(--teal); }
.media-item.selected,.m-item.selected { border-color:var(--teal); box-shadow:0 0 12px var(--teal-g); }
.media-item img,.media-item video,.m-item img,.m-item video { width:100%; height:84px; object-fit:cover; display:block; }
.media-item-name,.m-name { font-size:.62rem; color:var(--muted); padding:3px 6px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.media-item-del,.btn-del { position:absolute; top:4px; right:4px; background:rgba(239,68,68,.85); color:#fff; border:none; border-radius:50%; width:20px; height:20px; cursor:pointer; font-size:.68rem; display:none; align-items:center; justify-content:center; }
.media-item:hover .media-item-del,.m-item:hover .btn-del { display:flex; }
.empty { color:var(--muted); text-align:center; padding:40px; font-size:.88rem; }
code { background:rgba(45,212,191,.1); color:var(--teal); padding:2px 6px; border-radius:4px; font-size:.8em; }
.err-msg { color:#f87171; font-size:.82rem; margin-top:4px; display:none; }
.err-msg.show { display:block; }
@media (max-width:768px) {
    header .hw { padding:10px 14px; gap:10px; }
    .brand-name { font-size:.8rem; }
    nav.mnav { overflow-x:auto; white-space:nowrap; padding-bottom:4px; -webkit-overflow-scrolling:touch; }
    nav.mnav::-webkit-scrollbar { display:none; }
    main { padding:16px 12px 100px; }
    .li,.blog-card-li { flex-wrap:wrap; padding:12px 14px; gap:10px; }
    .blog-thumb { width:70px; height:52px; }
    .li-info { flex:1 1 50%; min-width:0; }
    .li-actions { width:100%; justify-content:flex-end; border-top:1px solid rgba(255,255,255,0.06); padding-top:8px; margin-top:4px; }
    .grow2,.grow3 { grid-template-columns:1fr; }
    .save-bar { padding:10px 16px; flex-wrap:wrap; gap:8px; }
    .save-status { width:100%; margin-bottom:2px; }
}
"""

def make_page(section_id, title, nav_active):
    cms_js = clean_js(CMS_JS, section_id)
    nav    = nav_html(nav_active)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>{title} - Manu Jungle Admin</title>
<meta name="robots" content="noindex,nofollow">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="icon" href="../assets/img/logo.png">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<script src="js/auth.js"></script>
<div id="pg-particles" style="position:fixed;inset:0;pointer-events:none;z-index:0;"></div>
<header>
  <div class="hw">
    <a href="panel.html" class="logo-brand">
      <div class="logo-wrap"><div class="logo-glow"></div><img src="../assets/img/logo.png" alt="Logo"></div>
      <span class="brand-name">Manu Jungle</span>
    </a>
    <a href="panel.html" class="btn-panel"><i class="ph ph-arrow-left"></i> Volver al Panel</a>
    <nav class="mnav">
      {nav}
    </nav>
    <div class="user-sec">
      <button onclick="logout()" class="btn-logout"><i class="ph ph-sign-out"></i> Salir</button>
    </div>
  </div>
</header>
<main id="mc"></main>
<div class="save-bar" id="save-bar" style="display:none">
  <span class="save-status" id="save-status"></span>
  <button class="btn-secondary" id="btn-cancel-save">Cancelar</button>
  <button class="btn-primary" id="btn-save"><i class="ph ph-floppy-disk"></i> Guardar cambios</button>
</div>
<div class="modal-bg" id="del-modal">
  <div class="modal">
    <div class="modal-h"><h3 id="del-title">Eliminar elemento</h3></div>
    <div class="modal-body"><p style="color:var(--muted);font-size:.85rem" id="del-msg">Esta accion no se puede deshacer.</p></div>
    <div class="modal-actions">
      <button class="btn-secondary" onclick="closeModal('del-modal')">Cancelar</button>
      <button class="btn-danger" id="del-confirm">Si, eliminar</button>
    </div>
  </div>
</div>
<div class="modal-bg" id="media-modal">
  <div class="modal lg">
    <div class="modal-h">
      <h3><i class="ph ph-image"></i> Galeria de Medios</h3>
      <div style="display:flex;gap:8px;">
        <button class="btn-primary" onclick="document.getElementById('media-upload').click()"><i class="ph ph-upload"></i> Subir</button>
        <button class="btn-secondary" onclick="document.getElementById('media-upload-folder').click()">Carpeta</button>
      </div>
      <input type="file" id="media-upload" accept="image/*,video/*" multiple style="display:none">
      <input type="file" id="media-upload-folder" accept="image/*,video/*" webkitdirectory directory style="display:none">
    </div>
    <div class="modal-body" id="media-modal-body"><div class="loading"><div class="spinner"></div> Cargando...</div></div>
    <div class="modal-actions">
      <span id="media-upload-prog" style="margin-right:auto;font-size:.77rem;color:var(--muted);"></span>
      <button class="btn-secondary" onclick="closeModal('media-modal')">Cancelar</button>
      <button class="btn-primary" id="media-confirm" onclick="confirmMediaSelect()" disabled>Insertar</button>
    </div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
const API = '/api/cms';
const MEDIA_API = '/api/media';
let token = sessionStorage.getItem('cms_token');
let cUser = sessionStorage.getItem('cms_user') || '';
let cSection = '{section_id}';
var cSha=null,cFile=null,cData=null,saveFnRef=null;
var currentMediaFiles=[],selectedMediaUrl=null,mediaSelectCallback=null;
var currentReclamosData=[],currentReclamoId=null;
window.sidebarItems=[];
window.activeSubSection=null;

function showSaveBar(fn,msg){{
  saveFnRef=fn;
  document.getElementById('save-bar').style.display='flex';
  const ss=document.getElementById('save-status');
  ss.textContent=msg||'';ss.className='save-status';
}}
function hideSaveBar(){{
  document.getElementById('save-bar').style.display='none';
  saveFnRef=null;
  const btn=document.getElementById('btn-save');
  if(btn){{btn.disabled=false;btn.innerHTML='<i class="ph ph-floppy-disk"></i> Guardar cambios';}}
}}
document.getElementById('btn-save').addEventListener('click',async()=>{{
  if(!saveFnRef)return;
  const btn=document.getElementById('btn-save');
  const ss=document.getElementById('save-status');
  btn.disabled=true;btn.innerHTML='<i class="ph ph-spinner ph-spin"></i> Guardando...';
  try{{
    await saveFnRef();
    ss.textContent='Guardado correctamente';ss.className='save-status ok';
    btn.innerHTML='<i class="ph ph-check-circle"></i> Guardado \u2713';
    setTimeout(()=>{{btn.disabled=false;btn.innerHTML='<i class="ph ph-floppy-disk"></i> Guardar cambios';}},1500);
  }}catch(e){{
    ss.textContent='Error: '+e.message;ss.className='save-status err';
    btn.disabled=false;btn.innerHTML='<i class="ph ph-floppy-disk"></i> Guardar cambios';
  }}
}});
document.getElementById('btn-cancel-save').addEventListener('click',()=>{{hideSaveBar();switchSection(cSection);}});

function openModal(id){{document.getElementById(id).classList.add('open');}}
function closeModal(id){{document.getElementById(id).classList.remove('open');document.getElementById(id).style.display='none';}}

function set(h){{
  let tabs='';
  if(window.sidebarItems&&window.sidebarItems.length){{
    tabs='<div class="sub-nav-tabs">'+
      window.sidebarItems.map(function(s){{
        var ac=s.id===window.activeSubSection?' class="active"':'';
        return '<button'+ac+' onclick="switchSubSection(this.dataset.id)" data-id="'+s.id+'">'+(s.label||s.id)+'</button>';
      }}).join('')+'</div>';
  }}
  document.getElementById('mc').innerHTML=tabs+h;
}}
window.switchSubSection=function(id){{window.activeSubSection=id;route(id);}};

const SEC_MAP=[
  {{id:'blog',sub:[]}},
  {{id:'content',sub:[{{id:'home',label:'Inicio'}},{{id:'about',label:'Nosotros'}},{{id:'contact',label:'Contacto'}},{{id:'global',label:'Globales'}}]}},
  {{id:'tours',sub:[]}},{{id:'departures',sub:[]}},{{id:'testimonials',sub:[]}},{{id:'media',sub:[]}},
];
function switchSection(id){{
  cSection=id;hideSaveBar();
  const sec=SEC_MAP.find(s=>s.id===id);
  if(sec&&sec.sub.length){{window.sidebarItems=sec.sub;window.activeSubSection=sec.sub[0].id;route(sec.sub[0].id);}}
  else{{window.sidebarItems=[];window.activeSubSection=null;route(id);}}
}}

document.addEventListener('DOMContentLoaded',()=>{{
  if(!token)return;
  tsParticles.load('pg-particles',{{fpsLimit:60,particles:{{number:{{value:22,density:{{enable:true,area:800}}}},color:{{value:['#c9a84c','#2dd4bf','#ffffff']}},shape:{{type:'circle'}},opacity:{{value:.4,random:true}},size:{{value:2,random:true}},move:{{enable:true,speed:.4,direction:'top',random:true,outModes:{{default:'out'}}}}}},detectRetina:true}});
  switchSection('{section_id}');
}});

// ── CMS Logic ────────────────────────────────────────────
{cms_js}
</script>
</body>
</html>"""

PAGES = [
    ("gestionar-blog.html",        "blog",         "Blog",               "blog"),
    ("gestionar-tours.html",       "tours",        "Gestionar Tours",    "tours"),
    ("gestionar-testimonios.html", "testimonials", "Testimonios",        "testimonials"),
    ("gestionar-contenido.html",   "content",      "Contenido",          "content"),
    ("gestionar-salidas.html",     "departures",   "Salidas Programadas","departures"),
    ("gestionar-medios.html",      "media",        "Galeria Multimedia", "media"),
    ("gestionar-reclamos.html",    "reclamos",     "Reclamos",           None),
]

for filename, section_id, title, nav_active in PAGES:
    html = make_page(section_id, title, nav_active)
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(path)
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    fns = re.findall(r'(?:async\s+)?function (\w+)', c)
    double_plus = '\u2795 +' in c
    ok = "auth.js" in c and "viewTours" in fns and "esc" in fns and "buildTopNav_DIS" in c and not double_plus
    print(f"{'OK' if ok else 'WARN'}: {filename} ({size//1024}kb) | fns={len(fns)} | double+={double_plus}")

print("\nDone!")
