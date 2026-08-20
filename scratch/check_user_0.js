
const API = '/api/cms';
const MEDIA_API = '/api/media';
let token = sessionStorage.getItem('cms_token');
let cUser = sessionStorage.getItem('cms_user') || '';
let cRole = sessionStorage.getItem('cms_role') || 'normal';
var cSha=null, cFile='www.manujungleforever.com/data/users.json', cData=null, saveFnRef=null;

function set(h){ document.getElementById('mc').innerHTML=h; }
function v(id){ return document.getElementById(id)?.value??''; }
function esc(s){ return String(s||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function showSaveBar(fn,msg){
  saveFnRef=fn;
  document.getElementById('save-bar').style.display='flex';
  const ss=document.getElementById('save-status');
  ss.textContent=msg||''; ss.className='save-status';
}
function hideSaveBar(){
  document.getElementById('save-bar').style.display='none';
  saveFnRef=null;
}
document.getElementById('btn-save').addEventListener('click',async()=>{
  if(!saveFnRef)return;
  const btn=document.getElementById('btn-save');
  const ss=document.getElementById('save-status');
  btn.disabled=true; btn.innerHTML='<i class="ph ph-spinner ph-spin"></i> Guardando...';
  try{
    await saveFnRef();
    ss.textContent='Guardado correctamente'; ss.className='save-status ok';
    btn.innerHTML='<i class="ph ph-check-circle"></i> Guardado ✓';
    setTimeout(()=>{btn.disabled=false;btn.innerHTML='<i class="ph ph-floppy-disk"></i> Guardar cambios';},1500);
  }catch(e){
    ss.textContent='Error: '+e.message; ss.className='save-status err';
    btn.disabled=false; btn.innerHTML='<i class="ph ph-floppy-disk"></i> Guardar cambios';
  }
});
document.getElementById('btn-cancel-save').addEventListener('click',()=>{hideSaveBar();viewUsers();});

async function ghGet(path) {
  const r = await fetch(`${API}/file?path=${encodeURIComponent(path)}`,{headers:{Authorization:`Bearer ${token}`}});
  if (r.status===401){sessionStorage.clear();location.reload();}
  if (!r.ok){const e=await r.json().catch(()=>({}));throw new Error(e.error||'Error al cargar');}
  return r.json();
}

async function ghPut(path, content, sha, msg) {
  const r = await fetch(`${API}/file`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, content, sha, message: msg || `update: ${path}` })
  });
  if (r.status === 401) { sessionStorage.clear(); location.reload(); }
  const d = await r.json();
  if (!r.ok) throw new Error(d.error || 'Error al guardar');
  return d;
}

// ── R2 UPLOAD HELPER ──
async function r2Upload(file, progressEl) {
  if (progressEl) progressEl.textContent = 'Subiendo a R2...';
  const r = await fetch(`${MEDIA_API}`, {
    method: 'POST',
    headers: { 
      Authorization: `Bearer ${token}`, 
      'X-File-Name': encodeURIComponent(file.name),
      'Content-Type': file.type || 'application/octet-stream'
    },
    body: file
  });
  if (r.status===401){sessionStorage.clear();location.reload();}
  
  let d;
  try {
    d = await r.json();
  } catch(e) {
    throw new Error(`Error del servidor (HTTP ${r.status}). Verifica la configuración de R2.`);
  }
  
  if(!r.ok) throw new Error(d.error||'Error subiendo archivo');
  return d.file;
}

// ── GALERÍA MODAL ──
let targetInputId = null;
let targetPrevId = null;

async function pickImage(inputId, prevId) {
  targetInputId = inputId;
  targetPrevId = prevId;
  document.getElementById('gallery-modal').classList.add('open');
  const grid = document.getElementById('gallery-grid');
  const loader = document.getElementById('gallery-loading');
  grid.innerHTML = '';
  loader.style.display = 'block';

  try {
    const r = await fetch(`${MEDIA_API}`, { headers: { Authorization: `Bearer ${token}` } });
    const d = await r.json();
    loader.style.display = 'none';
    const files = d.files || [];
    if (files.length === 0) {
      grid.innerHTML = '<p style="color:var(--muted);grid-column:1/-1;">No hay imágenes en R2 todavía.</p>';
      return;
    }
    files.forEach(f => {
      const item = document.createElement('div');
      item.className = 'gallery-item';
      item.innerHTML = `<img src="${esc(f.url)}" alt="img">`;
      item.onclick = () => {
        selectGalleryImage(f.url);
      };
      grid.appendChild(item);
    });
  } catch(e) {
    loader.textContent = 'Error al cargar galería: ' + e.message;
  }
}

function selectGalleryImage(url) {
  if (targetInputId) {
    const inp = document.getElementById(targetInputId);
    if (inp) inp.value = url;
  }
  if (targetPrevId) {
    updateAvatarPreview(targetInputId, targetPrevId);
  }
  closeGalleryModal();
}

function closeGalleryModal() {
  document.getElementById('gallery-modal').classList.remove('open');
  targetInputId = null;
  targetPrevId = null;
}

function updateAvatarPreview(inputId, prevId) {
  const inp = document.getElementById(inputId);
  const prev = document.getElementById(prevId);
  const placeholder = document.getElementById('avatar-placeholder');
  if (!inp || !prev) return;
  const url = inp.value.trim();
  if (url) {
    prev.src = url;
    prev.classList.add('show');
    if (placeholder) placeholder.style.display = 'none';
  } else {
    prev.src = '';
    prev.classList.remove('show');
    if (placeholder) placeholder.style.display = 'block';
  }
}

document.addEventListener('DOMContentLoaded',()=>{
  if(!token)return;
  if (typeof tsParticles !== 'undefined') {
    tsParticles.load('pg-particles', {
      fpsLimit: 60,
      particles: {
        number: { value: 24, density: { enable: true, area: 800 } },
        color: { value: ['#c9a84c', '#2dd4bf', '#ffffff'] },
        shape: { type: 'circle' },
        opacity: { value: 0.35, random: true, animation: { enable: true, speed: 0.4, minimumValue: 0.08, sync: false } },
        size: { value: 2.2, random: true, animation: { enable: true, speed: 0.6, minimumValue: 0.4, sync: false } },
        move: { enable: true, speed: 0.45, direction: 'top', random: true, straight: false, outModes: { default: 'out' } }
      },
      detectRetina: true
    });
  }
  viewUsers();
});

async function viewUsers() {
  set('<div class="loading" style="padding:40px 0;display:flex;align-items:center;gap:12px;color:var(--muted);"><div class="spinner" style="width:20px;height:20px;border-radius:50%;border:2px solid rgba(45,212,191,.2);border-top-color:var(--teal);animation:spin .8s linear infinite;"></div> Cargando usuarios...</div>');
  try {
    const data = await ghGet(cFile);
    cSha = data.sha;
    cData = JSON.parse(data.content);
    const users = cData.users || [];

    const superCount = users.filter(u => u.role === 'superuser').length;
    const normalCount = users.filter(u => u.role === 'normal').length;

    let html = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:14px;">
        <div style="display:flex;align-items:center;">
          <div class="btn-card-icon card-icon-users"><i class="ph ph-users-three"></i></div>
          <div>
            <p class="pt" style="margin-bottom:0">Gestión de Usuarios y Perfiles</p>
            <p class="ps">${users.length} cuentas registradas con avatar y control de roles</p>
          </div>
        </div>
        <button class="btn-primary" onclick="editUser(-1)">+ Nuevo Usuario</button>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;">
        <div class="esec" style="padding:16px;">
          <div style="font-size:1.8rem;font-weight:700;color:var(--gold);">${superCount}</div>
          <div style="font-size:0.8rem;color:var(--muted);">Super Usuarios (Acceso Total)</div>
        </div>
        <div class="esec" style="padding:16px;">
          <div style="font-size:1.8rem;font-weight:700;color:var(--teal);">${normalCount}</div>
          <div style="font-size:0.8rem;color:var(--muted);">Editores / Normales (Control de Posts)</div>
        </div>
        <div class="esec" style="padding:16px;">
          <div style="font-size:1.8rem;font-weight:700;color:#fff;">${users.length}</div>
          <div style="font-size:0.8rem;color:var(--muted);">Total de Cuentas</div>
        </div>
      </div>

      <div class="list-grid">`;

    users.forEach((u, i) => {
      const isSuper = u.role === 'superuser';
      const initial = (u.name || u.email).charAt(0).toUpperCase();
      const isProtected = ['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com'].includes(u.email.toLowerCase());
      const roleLabel = isSuper ? '⭐ SUPER USER' : '📝 EDITOR / NORMAL';
      const badgeCls = isSuper ? 'superuser' : 'normal';
      const foto = u.foto || u.avatar || '';

      const avatarMarkup = foto 
        ? `<div class="user-avatar ${badgeCls}"><img src="${esc(foto)}" class="user-avatar-img" alt="${esc(u.name)}" onerror="this.style.display='none';this.parentElement.textContent='${initial}';"></div>`
        : `<div class="user-avatar ${badgeCls}">${initial}</div>`;

      html += `
        <div class="li">
          <div style="display:flex;align-items:center;gap:16px;flex:1;min-width:0;">
            ${avatarMarkup}
            <div class="li-info">
              <h3>
                ${esc(u.name)} 
                <span class="badge ${badgeCls}">${roleLabel}</span>
                <span class="badge ${u.activo !== false ? 'on' : 'off'}">${u.activo !== false ? 'Activo' : 'Inactivo'}</span>
              </h3>
              <span>📧 <strong>${esc(u.email)}</strong> · Registrado: ${u.created_at ? u.created_at.split('T')[0] : '2026-08-19'} ${isProtected ? '· 🔒 Cuenta Principal Protegida' : ''}</span>
            </div>
          </div>
          <div class="li-actions">
            <button class="btn-edit" onclick="editUser(${i})"><i class="ph ph-pencil"></i> Editar Perfil / Clave</button>
            ${!isProtected ? `<button class="btn-danger" onclick="deleteUser(${i})" title="Eliminar usuario"><i class="ph ph-trash"></i></button>` : ''}
          </div>
        </div>`;
    });

    html += `</div>`;
    set(html);

  } catch(e) {
    set(`<p style="color:var(--danger);padding:20px;">❌ Error al cargar usuarios: ${e.message}</p>`);
  }
}

window.triggerUserAvatarUpload = function() {
  const name = document.getElementById('u-name') ? document.getElementById('u-name').value.trim() : '';
  const email = document.getElementById('u-email') ? document.getElementById('u-email').value.trim() : '';
  if (!name && !email) {
    alert('Por favor, ingresa el Nombre o Correo del usuario antes de subir la imagen de perfil.');
    document.getElementById('u-name').focus();
    return;
  }
  document.getElementById('u-upload-file').click();
};

window.takeUserAvatarPhoto = function() {
  const name = document.getElementById('u-name') ? document.getElementById('u-name').value.trim() : '';
  const email = document.getElementById('u-email') ? document.getElementById('u-email').value.trim() : '';
  if (!name && !email) {
    alert('Por favor, ingresa el Nombre o Correo del usuario antes de tomar la fotografía.');
    document.getElementById('u-name').focus();
    return;
  }
  document.getElementById('u-camera-file').click();
};

window.removeUserAvatar = function() {
  const inp = document.getElementById('u-foto');
  if (inp) {
    inp.value = '';
    updateAvatarPreview('u-foto', 'u-foto-prev');
  }
};

window.uploadUserAvatar = async function(input) {
  if (!input.files || input.files.length === 0) return;
  const file = input.files[0];
  const email = (document.getElementById('u-email')?.value.trim() || 'usuario').toLowerCase();
  const cleanEmail = email.replace(/[^a-z0-9_-]/gi, '-').replace(/-+/g, '-');
  const ext = (file.name && file.name.includes('.')) ? file.name.split('.').pop().toLowerCase() : 'jpg';

  const fileName = `usuarios/${cleanEmail}/avatar_${Date.now()}.${ext}`;
  const renamedFile = new File([file], fileName, { type: file.type || 'image/jpeg' });

  const btn = document.getElementById('btn-upload-avatar');
  const oldText = btn ? btn.innerHTML : '';
  if (btn) {
    btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Subiendo...';
    btn.disabled = true;
  }

  try {
    const res = await r2Upload(renamedFile, null);
    const url = (typeof res === 'object' && res && res.url) ? res.url : (res || `/media/${fileName}`);
    const fotoInput = document.getElementById('u-foto');
    if (fotoInput) {
      fotoInput.value = url;
      updateAvatarPreview('u-foto', 'u-foto-prev');
    }
  } catch(e) {
    alert('Error al subir foto de perfil a R2: ' + e.message);
  } finally {
    if (btn) {
      btn.innerHTML = oldText;
      btn.disabled = false;
    }
    input.value = '';
  }
};

window.editUser = function(idx) {
  const u = idx === -1 
    ? { id: 'usr_' + Date.now(), email: '', name: '', role: 'normal', activo: true, password_hash: '', foto: '' } 
    : cData.users[idx];
  const isSuperAccount = ['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com'].includes((u.email || '').toLowerCase());
  const foto = u.foto || u.avatar || '';
  const initial = (u.name || u.email || 'U').charAt(0).toUpperCase();
  const isSuper = u.role === 'superuser';

  set(`
    <button class="back-btn" onclick="viewUsers()">← Volver a usuarios</button>
    <div class="eform">
      <!-- FOTO DE PERFIL / AVATAR -->
      <div class="esec">
        <div class="esec-h">Imagen de Perfil / Avatar</div>
        <div class="avatar-upload-card">
          <div class="avatar-preview-wrap ${isSuper ? 'superuser' : ''}">
            <img id="u-foto-prev" class="avatar-preview-img ${foto ? 'show' : ''}" src="${esc(foto)}" alt="Avatar">
            <span id="avatar-placeholder" class="avatar-preview-placeholder" style="display:${foto ? 'none' : 'block'};">${initial}</span>
          </div>
          <div class="avatar-controls">
            <div class="ff" style="margin-bottom:6px;">
              <label>Ruta o URL de Imagen</label>
              <input id="u-foto" value="${esc(foto)}" placeholder="https://... o sube una imagen" oninput="updateAvatarPreview('u-foto', 'u-foto-prev')">
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button type="button" class="btn-primary" id="btn-upload-avatar" onclick="triggerUserAvatarUpload()" style="background:#0284c7;color:white;border:none;" title="Subir desde tu dispositivo"><i class="ph ph-upload-simple"></i> Subir Foto</button>
              <button type="button" class="btn-primary" onclick="takeUserAvatarPhoto()" style="background:var(--teal);color:#030807;border:none;" title="Tomar foto con la cámara"><i class="ph ph-camera"></i> Tomar Foto</button>
              <button type="button" class="btn-secondary" onclick="pickImage('u-foto', 'u-foto-prev')" title="Elegir de galería R2"><i class="ph ph-image"></i> Galería</button>
              ${foto ? `<button type="button" class="btn-danger" onclick="removeUserAvatar()" title="Quitar foto"><i class="ph ph-trash"></i> Quitar</button>` : ''}
              <input type="file" id="u-upload-file" accept="image/*" style="display:none" onchange="uploadUserAvatar(this)">
              <input type="file" id="u-camera-file" accept="image/*" capture="environment" style="display:none" onchange="uploadUserAvatar(this)">
            </div>
            <span class="hint">Las fotos se guardan automáticamente en Cloudflare R2 organizadas en la carpeta <code>usuarios/{email}/</code>.</span>
          </div>
        </div>
      </div>

      <!-- DATOS DEL USUARIO -->
      <div class="esec">
        <div class="esec-h">${idx === -1 ? 'Crear Nuevo Usuario' : 'Datos del Usuario'}</div>
        <div class="grow2">
          <div class="ff">
            <label>Nombre Completo</label>
            <input id="u-name" value="${esc(u.name)}" placeholder="Ej: Gloria">
          </div>
          <div class="ff">
            <label>Correo Electrónico (Login)</label>
            <input type="email" id="u-email" value="${esc(u.email)}" placeholder="usuario@manujungleforever.com" ${isSuperAccount ? 'readonly style="opacity:0.75;"' : ''}>
          </div>
        </div>
        <div class="grow2">
          <div class="ff">
            <label>Rol de Usuario</label>
            <select id="u-role" ${isSuperAccount ? 'disabled' : ''}>
              <option value="superuser" ${u.role === 'superuser' ? 'selected' : ''}>⭐ Super User (Acceso total a todo el panel y usuarios)</option>
              <option value="normal" ${u.role === 'normal' ? 'selected' : ''}>📝 Editor / Normal (Gestión y edición de Posts y Contenido)</option>
            </select>
            ${isSuperAccount ? '<span class="hint">El rol de este Super Usuario está protegido.</span>' : ''}
          </div>
          <div class="ff">
            <label>Estado de Cuenta</label>
            <select id="u-act">
              <option value="true" ${u.activo !== false ? 'selected' : ''}>✅ Activo</option>
              <option value="false" ${u.activo === false ? 'selected' : ''}>🔒 Inactivo / Suspendido</option>
            </select>
          </div>
        </div>
      </div>

      <!-- SEGURIDAD -->
      <div class="esec">
        <div class="esec-h">Seguridad y Cambio de Contraseña</div>
        <div class="grow2">
          <div class="ff">
            <label>${idx === -1 ? 'Contraseña Inicial *' : 'Nueva Contraseña (Opcional)'}</label>
            <input type="password" id="u-pass" placeholder="${idx === -1 ? 'Mínimo 6 caracteres' : 'Dejar en blanco para mantener la actual'}">
            <span class="hint">Por defecto: <code>123456aytana</code></span>
          </div>
          <div class="ff">
            <label>Confirmar Contraseña</label>
            <input type="password" id="u-pass-conf" placeholder="Repite la contraseña">
          </div>
        </div>
      </div>
    </div>`);

  showSaveBar(async () => {
    const name = v('u-name').trim();
    const email = v('u-email').toLowerCase().trim();
    const role = isSuperAccount ? 'superuser' : v('u-role');
    const activo = v('u-act') === 'true';
    const foto = v('u-foto').trim();
    const pass = v('u-pass').trim();
    const passConf = v('u-pass-conf').trim();

    if (!name || !email) throw new Error('Nombre y correo son obligatorios.');

    let newHash = u.password_hash;
    if (idx === -1) {
      const finalPass = pass || '123456aytana';
      if (pass && pass !== passConf) throw new Error('Las contraseñas no coinciden.');
      newHash = await sha256(finalPass);
    } else {
      if (pass) {
        if (pass !== passConf) throw new Error('Las contraseñas no coinciden.');
        if (pass.length < 6) throw new Error('La contraseña debe tener al menos 6 caracteres.');
        newHash = await sha256(pass);
      }
    }

    const updated = {
      id: u.id || ('usr_' + Date.now()),
      email,
      name,
      role,
      foto,
      password_hash: newHash,
      activo,
      created_at: u.created_at || new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    if (idx === -1) {
      if (cData.users.some(x => x.email.toLowerCase() === email)) {
        throw new Error('Ya existe un usuario con este correo electrónico.');
      }
      cData.users.unshift(updated);
    } else {
      cData.users[idx] = updated;
    }

    // Si es el usuario actual, actualizar la sesión
    if (email === cUser.toLowerCase()) {
      sessionStorage.setItem('cms_name', updated.name);
      sessionStorage.setItem('cms_avatar', updated.foto || '');
      const huser = document.getElementById('huser');
      if (huser && typeof window.isSuperUser === 'function') {
        const isSuper = window.isSuperUser();
        const roleBadge = isSuper 
          ? '<span style="font-size:0.68rem;background:rgba(201,168,76,0.2);color:#c9a84c;padding:2px 7px;border-radius:6px;margin-left:6px;border:1px solid rgba(201,168,76,0.3);">SUPER USER</span>'
          : '<span style="font-size:0.68rem;background:rgba(45,212,191,0.15);color:#2dd4bf;padding:2px 7px;border-radius:6px;margin-left:6px;border:1px solid rgba(45,212,191,0.3);">EDITOR</span>';
        const avatarHtml = updated.foto 
          ? `<img src="${esc(updated.foto)}" style="width:26px;height:26px;border-radius:50%;object-fit:cover;border:1.5px solid ${isSuper ? '#c9a84c' : '#2dd4bf'};vertical-align:middle;margin-right:6px;display:inline-block;">`
          : `<span style="font-size:1rem;margin-right:4px;vertical-align:middle;">👤</span>`;
        huser.innerHTML = `${avatarHtml}<span style="vertical-align:middle;">${updated.name}</span> ${roleBadge}`;
      }
    }

    const res = await ghPut(cFile, JSON.stringify(cData, null, 2), cSha, `update user: ${updated.email}`);
    cSha = res.sha;
    document.querySelector('.back-btn').textContent = '← Usuarios (guardado ✓)';
    setTimeout(() => { viewUsers(); }, 1200);
  });
};

window.deleteUser = async function(idx) {
  const u = cData.users[idx];
  if (!u) return;
  if (['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com'].includes(u.email.toLowerCase())) {
    return alert('No puedes eliminar este Super Usuario principal.');
  }
  if (!confirm(`¿Estás seguro de eliminar permanentemente al usuario "${u.name} (${u.email})"?`)) return;

  cData.users.splice(idx, 1);
  const res = await ghPut(cFile, JSON.stringify(cData, null, 2), cSha, `delete user: ${u.email}`);
  cSha = res.sha;
  await viewUsers();
};
