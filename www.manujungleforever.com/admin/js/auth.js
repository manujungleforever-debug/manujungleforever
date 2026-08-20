(function () {
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
    
    // Auth success - show body
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { 
            document.body.style.opacity = '1';
            setupUserInterface();
        });
    } else {
        if (document.body) document.body.style.opacity = '1';
        setupUserInterface();
    }

    function setupUserInterface() {
        const u = sessionStorage.getItem('cms_user') || '';
        const role = sessionStorage.getItem('cms_role') || (isSuperUser() ? 'superuser' : 'normal');
        const name = sessionStorage.getItem('cms_name') || u.split('@')[0] || 'Admin';

        const adminNameEl = document.getElementById('admin-name');
        if (adminNameEl) {
            adminNameEl.textContent = name;
        }

        const huser = document.getElementById('huser');
        if (huser) {
            const isSuper = isSuperUser();
            const roleBadge = isSuper 
                ? '<span style="font-size:0.68rem;background:rgba(201,168,76,0.2);color:#c9a84c;padding:2px 7px;border-radius:6px;margin-left:6px;border:1px solid rgba(201,168,76,0.3);">SUPER USER</span>'
                : '<span style="font-size:0.68rem;background:rgba(45,212,191,0.15);color:#2dd4bf;padding:2px 7px;border-radius:6px;margin-left:6px;border:1px solid rgba(45,212,191,0.3);">EDITOR</span>';
            huser.innerHTML = `👤 ${name} ${roleBadge}`;
        }
    }
})();

function isSuperUser() {
    const role = (sessionStorage.getItem('cms_role') || '').toLowerCase();
    const user = (sessionStorage.getItem('cms_user') || '').toLowerCase();
    
    // Si no hay rol guardado aún (sesión previa) o es una de las cuentas superuser o admin
    if (!role || ['superuser', 'admin'].includes(role)) return true;
    if (['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com', 'manujungleforever@gmail.com', 'admin'].includes(user)) return true;
    
    // Solo es false si explícitamente el rol es 'normal' y no es una de las cuentas maestras
    return role !== 'normal';
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}

async function sha256(str) {
    const enc = new TextEncoder();
    const data = enc.encode(str + 'mjf_salt_2026');
    const hash = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

window.isSuperUser = isSuperUser;
window.logout = logout;
window.sha256 = sha256;
