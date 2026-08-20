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

    async function setupUserInterface() {
        const u = sessionStorage.getItem('cms_user') || '';
        const role = sessionStorage.getItem('cms_role') || (isSuperUser() ? 'superuser' : 'normal');
        let name = sessionStorage.getItem('cms_name') || u.split('@')[0] || 'Admin';
        let avatar = sessionStorage.getItem('cms_avatar') || '';

        // Si no tiene avatar en session, buscarlo en data/users.json
        if (!avatar && u) {
            try {
                const r = await fetch('/data/users.json');
                if (r.ok) {
                    const data = await r.json();
                    const found = (data.users || []).find(x => (x.email || '').toLowerCase() === u.toLowerCase());
                    if (found) {
                        if (found.foto) {
                            avatar = found.foto;
                            sessionStorage.setItem('cms_avatar', avatar);
                        }
                        if (found.name) {
                            name = found.name;
                            sessionStorage.setItem('cms_name', name);
                        }
                    }
                }
            } catch(e) {}
        }

        const isSuper = isSuperUser();
        const initial = (name || u || 'A').charAt(0).toUpperCase();
        const roleLabel = isSuper ? 'SUPER USER' : 'EDITOR';
        const roleClass = isSuper ? 'superuser' : 'normal';

        const avatarMarkup = avatar 
            ? `<img src="${avatar}" alt="${name}" onerror="this.outerHTML='<span class=\'initial-avatar\'>${initial}</span>';">`
            : `<span class="initial-avatar">${initial}</span>`;

        const huser = document.getElementById('huser');
        if (huser) {
            huser.innerHTML = `
                <div class="user-pill ${isSuper ? 'superuser' : ''}">
                    ${avatarMarkup}
                    <span class="user-pill-name" title="${u}">${name}</span>
                    <span class="badge ${roleClass}">${roleLabel}</span>
                </div>
            `;
        }

        const adminNameEl = document.getElementById('admin-name');
        if (adminNameEl) {
            adminNameEl.textContent = name;
        }
    }

    window.setupUserInterface = setupUserInterface;
})();

function isSuperUser() {
    const role = (sessionStorage.getItem('cms_role') || '').toLowerCase();
    const user = (sessionStorage.getItem('cms_user') || '').toLowerCase();
    
    if (!role || ['superuser', 'admin'].includes(role)) return true;
    if (['kemmesik@gmail.com', 'jordyleonidas@manujungleforever.com', 'manujungleforever@gmail.com', 'admin'].includes(user)) return true;
    
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
