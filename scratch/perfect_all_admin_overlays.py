import glob, os, re

# 1. Update auth.js
auth_code = """(function () {
    const token = sessionStorage.getItem('cms_token');
    const isLoginScreen = window.location.href.includes('index.html') || window.location.pathname === '/admin/' || window.location.pathname.endsWith('/admin');

    if (!token) { 
        if (!isLoginScreen) {
            window.location.href = 'index.html'; 
        } else {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => { document.body.style.opacity = '1'; });
            } else {
                if (document.body) document.body.style.opacity = '1';
            }
        }
        return; 
    }
    
    // Auth success - show body and render User Capsule immediately
    function renderUserCapsule() {
        const u = (sessionStorage.getItem('cms_user') || '').toLowerCase().trim();
        let name = sessionStorage.getItem('cms_name') || u.split('@')[0] || 'Admin';
        let avatar = sessionStorage.getItem('cms_avatar') || '';
        const isSuper = isSuperUser();
        const initial = (name || u || 'A').charAt(0).toUpperCase();
        const roleLabel = isSuper ? 'SUPER USER' : 'EDITOR';
        const roleClass = isSuper ? 'superuser' : 'normal';

        const avatarMarkup = avatar 
            ? `<img src="${avatar}" alt="${name}" onerror="this.outerHTML='<span class=\\'initial-avatar\\'>${initial}</span>';">`
            : `<span class="initial-avatar">${initial}</span>`;

        const huser = document.getElementById('huser');
        if (huser) {
            huser.innerHTML = `
                <div class="user-pill ${isSuper ? 'superuser' : ''}" title="${u}">
                    ${avatarMarkup}
                    <div class="user-pill-info">
                        <span class="user-pill-name">${name}</span>
                        <span class="user-pill-badge ${roleClass}">${roleLabel}</span>
                    </div>
                </div>
            `;
        }

        const adminNameEl = document.getElementById('admin-name');
        if (adminNameEl) {
            adminNameEl.textContent = name;
        }
    }

    async function syncUserData() {
        const u = (sessionStorage.getItem('cms_user') || '').toLowerCase().trim();
        if (u) {
            try {
                const r = await fetch('/data/users.json?t=' + Date.now());
                if (r.ok) {
                    const data = await r.json();
                    const found = (data.users || []).find(x => (x.email || '').toLowerCase().trim() === u);
                    if (found) {
                        if (found.foto) {
                            sessionStorage.setItem('cms_avatar', found.foto);
                        }
                        if (found.name) {
                            sessionStorage.setItem('cms_name', found.name);
                        }
                        if (found.role) {
                            sessionStorage.setItem('cms_role', found.role);
                        }
                        renderUserCapsule();
                    }
                }
            } catch(e) {}
        }
    }

    // Run render immediately and on DOMContentLoaded
    renderUserCapsule();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { 
            document.body.style.opacity = '1';
            renderUserCapsule();
            syncUserData();
        });
    } else {
        if (document.body) document.body.style.opacity = '1';
        renderUserCapsule();
        syncUserData();
    }

    window.renderUserCapsule = renderUserCapsule;
    window.setupUserInterface = renderUserCapsule;
})();

function isSuperUser() {
    const role = (sessionStorage.getItem('cms_role') || '').toLowerCase();
    const user = (sessionStorage.getItem('cms_user') || '').toLowerCase();
    
    if (!role || ['superuser', 'admin', 'super user'].includes(role)) return true;
    if (['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com', 'manujungleforever@gmail.com', 'admin'].includes(user)) return true;
    
    return role !== 'normal' && role !== 'editor';
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}

async function sha256(str) {
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}
"""

with open('admin/js/auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_code)
with open('www.manujungleforever.com/admin/js/auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_code)

# 2. Perfect all admin HTML files
admin_dirs = ['admin', 'www.manujungleforever.com/admin']

for d in admin_dirs:
    for fpath in glob.glob(os.path.join(d, 'gestionar-*.html')) + glob.glob(os.path.join(d, 'index.html')) + glob.glob(os.path.join(d, 'panel.html')):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()

        c = re.sub(r'href="css/thinking-orb\.css(?:\?v=\d+)?"', 'href="css/thinking-orb.css?v=9"', c)
        c = re.sub(r'src="js/thinking-orb\.js(?:\?v=\d+)?"', 'src="js/thinking-orb.js?v=9"', c)
        c = re.sub(r'src="js/auth\.js(?:\?v=\d+)?"', 'src="js/auth.js?v=9"', c)

        if 'gestionar-salidas.html' in fpath:
            # Fix savePax with try/finally
            save_pax_new = """window.savePax = async function(sIdx, pIdx, event) {
  const s = cData.salidas[sIdx];
  const p = {
    nombre_completo: v('p-n'),
    nacionalidad: v('p-na'),
    fecha_nacimiento: v('p-fn'),
    pasaporte: v('p-pa'),
    whatsapp: v('p-w'),
    email: v('p-e'),
    restricciones_dieteticas: v('p-rd'),
    condiciones_medicas: v('p-cm'),
    costo: +v('p-costo'),
    estado_pago: v('p-ep'),
    monto_pagado: +v('p-mp'),
    saldo_pendiente: +v('p-sp'),
    foto: v('p-foto')
  };
  
  if (!s.pasajeros) s.pasajeros = [];
  if (pIdx === -1) {
    s.pasajeros.push(p);
  } else {
    s.pasajeros[pIdx] = p;
  }
  
  if (window.showThinkingOverlay) window.showThinkingOverlay('Guardando pasajero....', 'Sincronizando manifiesto con GitHub y Cloudflare');
  
  try {
    const res = await ghPut(cFile, JSON.stringify(cData, null, 2), null, `update pax in: ${s.id}`);
    cSha = res.sha;
    viewPax(sIdx);
    if(typeof viewDeps === 'function') viewDeps();
  } catch(e) {
    console.error(e);
    alert('Error: ' + e.message);
  } finally {
    if (window.hideThinkingOverlay) window.hideThinkingOverlay();
  }
};"""
            c = re.sub(r"window\.savePax\s*=\s*async\s*function\(sIdx,\s*pIdx,\s*event\)\s*\{[\s\S]*?^\};", save_pax_new, c, flags=re.MULTILINE)

            # Fix deletePax with try/finally
            delete_pax_new = """window.deletePax = async function(sIdx, pIdx) {
  if (!confirm('¿Estás seguro de eliminar este pasajero? Esta acción no se puede deshacer.')) return;
  const s = cData.salidas[sIdx];
  s.pasajeros.splice(pIdx, 1);
  
  if (window.showThinkingOverlay) window.showThinkingOverlay('Eliminando pasajero....');
  
  try {
    const res = await ghPut(cFile, JSON.stringify(cData, null, 2), null, `delete pax in: ${s.id}`);
    cSha = res.sha;
    viewPax(sIdx);
    if(typeof viewDeps === 'function') viewDeps();
  } catch(e) {
    console.error(e);
    alert('Error al eliminar: ' + e.message);
  } finally {
    if (window.hideThinkingOverlay) window.hideThinkingOverlay();
  }
};"""
            c = re.sub(r"window\.deletePax\s*=\s*async\s*function\(sIdx,\s*pIdx\)\s*\{[\s\S]*?^\};", delete_pax_new, c, flags=re.MULTILINE)

            # Fix adjPlaza with try/finally
            adj_plaza_new = """window.adjPlaza = async function(idx, diff) {
  const s = cData.salidas[idx];
  const newVal = (s.plazas_disponibles||0) + diff;
  if (newVal < 0 || newVal > (s.plazas_totales||0)) return;
  s.plazas_disponibles = newVal;
  if (newVal === 0) s.estado = 'completo';
  else if (newVal <= 2) s.estado = 'limitado';
  else s.estado = 'disponible';
  
  if (window.showThinkingOverlay) window.showThinkingOverlay('Actualizando plazas....');
  try {
    const res = await ghPut(cFile, JSON.stringify(cData, null, 2), cSha, `adj plaza: ${s.id}`);
    cSha = res.sha;
    await viewDeps();
  } catch(e) {
    console.error(e);
    alert('Error: ' + e.message);
  } finally {
    if (window.hideThinkingOverlay) window.hideThinkingOverlay();
  }
};"""
            c = re.sub(r"window\.adjPlaza\s*=\s*async\s*function\(idx,\s*diff\)\s*\{[\s\S]*?^\};", adj_plaza_new, c, flags=re.MULTILINE)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)

print("Updated all admin templates.")
