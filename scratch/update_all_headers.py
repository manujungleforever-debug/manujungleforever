import glob, os, re

# 1. Update auth.js with robust avatar and single-line user-pill rendering
auth_js_content = """(function () {
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
            ? `<img src="${avatar}" alt="${name}" onerror="this.outerHTML='<span class=\\'initial-avatar\\'>${initial}</span>';">`
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
"""

with open('admin/js/auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_js_content)
with open('www.manujungleforever.com/admin/js/auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_js_content)

print("Updated auth.js")

# Common CSS for single-line header
header_css = """
/* Single-line header styles */
header .hw, header .header-wrap {
    max-width: 1560px !important;
    margin: 0 auto !important;
    padding: 10px 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 12px !important;
    flex-wrap: nowrap !important;
}
.logo-wrap img, .logo-img-wrap img {
    height: 42px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
}
.logo-brand {
    flex-shrink: 0 !important;
}
nav.mnav {
    display: flex !important;
    align-items: center !important;
    gap: 3px !important;
    flex-wrap: nowrap !important;
    flex: 1 1 auto !important;
    justify-content: center !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    margin: 0 8px !important;
}
nav.mnav::-webkit-scrollbar { display: none; }
nav.mnav a {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 6px 9px !important;
    border-radius: 8px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    flex-shrink: 0 !important;
}
.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
.user-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 3px 10px 3px 4px;
    border-radius: 24px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #f1f5f9;
}
.user-pill img {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid var(--teal, #2dd4bf);
    display: block;
}
.user-pill .initial-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(45, 212, 191, 0.2);
    color: var(--teal, #2dd4bf);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.8rem;
    border: 1.5px solid var(--teal, #2dd4bf);
}
.user-pill.superuser .initial-avatar {
    background: rgba(201, 168, 76, 0.2);
    color: #fbbf24;
    border-color: #c9a84c;
}
.user-pill.superuser img {
    border-color: #c9a84c;
}
.user-pill-name {
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
"""

admin_dirs = ['admin', 'www.manujungleforever.com/admin']
for d in admin_dirs:
    for fpath in glob.glob(f'{d}/*.html'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace inline 120px logo height with 42px
        content = re.sub(r'style="height:\s*120px[^"]*"', 'style="height: 42px; width: auto;"', content)
        
        # Inject the CSS before </head> if not already there
        if 'Single-line header styles' not in content:
            content = content.replace('</head>', f'<style>\n{header_css}\n</style>\n</head>')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated header styles in {fpath}")

