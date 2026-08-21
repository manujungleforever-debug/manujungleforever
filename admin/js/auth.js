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
            ? `<img src="${avatar}" alt="${name}" onerror="this.outerHTML='<span class=\'initial-avatar\'>${initial}</span>';">`
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
