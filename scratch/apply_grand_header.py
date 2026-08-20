import glob, os, re

# 1. Update auth.js without the role badge in the topbar pill
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
        const u = (sessionStorage.getItem('cms_user') || '').toLowerCase().trim();
        const role = sessionStorage.getItem('cms_role') || (isSuperUser() ? 'superuser' : 'normal');
        let name = sessionStorage.getItem('cms_name') || u.split('@')[0] || 'Admin';
        let avatar = sessionStorage.getItem('cms_avatar') || '';

        // Siempre sincronizar con la foto más reciente de data/users.json
        if (u) {
            try {
                const r = await fetch('/data/users.json?t=' + Date.now());
                if (r.ok) {
                    const data = await r.json();
                    const found = (data.users || []).find(x => (x.email || '').toLowerCase().trim() === u);
                    if (found) {
                        if (found.foto) {
                            avatar = found.foto;
                            sessionStorage.setItem('cms_avatar', avatar);
                        }
                        if (found.name) {
                            name = found.name;
                            sessionStorage.setItem('cms_name', name);
                        }
                        if (found.role) {
                            sessionStorage.setItem('cms_role', found.role);
                        }
                    }
                }
            } catch(e) {}
        }

        const isSuper = isSuperUser();
        const initial = (name || u || 'A').charAt(0).toUpperCase();

        const avatarMarkup = avatar 
            ? `<img src="${avatar}" alt="${name}" onerror="this.outerHTML='<span class=\\'initial-avatar\\'>${initial}</span>';">`
            : `<span class="initial-avatar">${initial}</span>`;

        const huser = document.getElementById('huser');
        if (huser) {
            huser.innerHTML = `
                <div class="user-pill ${isSuper ? 'superuser' : ''}" title="${isSuper ? 'Super User - ' + u : 'Editor - ' + u}">
                    ${avatarMarkup}
                    <span class="user-pill-name">${name}</span>
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

# 2. Grand single-line header CSS with extra breathing room
grand_header_css = """
/* Grand single-line header styles with large logo */
header {
    position: sticky !important;
    top: 0 !important;
    z-index: 200 !important;
    background: rgba(3, 8, 7, 0.96) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-bottom: 1.5px solid rgba(45, 212, 191, 0.22) !important;
    box-shadow: 0 8px 36px rgba(0, 0, 0, 0.6) !important;
}
header .hw, header .header-wrap {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 8px 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 20px !important;
    flex-wrap: nowrap !important;
    box-sizing: border-box !important;
    min-height: 115px !important;
}
.logo-wrap, .logo-img-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    flex-shrink: 0 !important;
}
.logo-wrap img, .logo-img-wrap img {
    height: 110px !important;
    width: auto !important;
    max-width: none !important;
    display: block !important;
    filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.6)) !important;
    transition: transform 0.25s ease !important;
}
.logo-wrap img:hover, .logo-img-wrap img:hover {
    transform: scale(1.03) !important;
}
.logo-brand {
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    text-decoration: none !important;
}
.btn-panel {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    background: rgba(45, 212, 191, 0.14) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.4) !important;
    color: var(--teal, #2dd4bf) !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: .25s !important;
    flex-shrink: 0 !important;
}
.btn-panel:hover {
    background: var(--teal, #2dd4bf) !important;
    color: #030807 !important;
    box-shadow: 0 0 20px rgba(45, 212, 191, 0.5) !important;
}
nav.mnav {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-wrap: nowrap !important;
    flex: 1 1 auto !important;
    justify-content: center !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    margin: 0 16px !important;
}
nav.mnav::-webkit-scrollbar { display: none; }
nav.mnav a {
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    padding: 10px 15px !important;
    border-radius: 11px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    flex-shrink: 0 !important;
    letter-spacing: -0.2px !important;
    transition: all 0.25s ease !important;
}
nav.mnav a i {
    font-size: 1.2rem !important;
}
nav.mnav a:hover, nav.mnav a.active {
    color: #2dd4bf !important;
    background: rgba(45, 212, 191, 0.16) !important;
    box-shadow: 0 0 20px rgba(45, 212, 191, 0.2) !important;
}
.user-sec {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    margin-left: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}
.user-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    background: rgba(11, 38, 35, 0.75) !important;
    border: 1.5px solid rgba(45, 212, 191, 0.3) !important;
    padding: 4px 16px 4px 4px !important;
    border-radius: 40px !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.user-pill.superuser {
    border-color: rgba(201, 168, 76, 0.5) !important;
    box-shadow: 0 4px 22px rgba(201, 168, 76, 0.22) !important;
}
.user-pill img {
    width: 44px !important;
    height: 44px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #2dd4bf !important;
    display: block !important;
    box-shadow: 0 0 14px rgba(45, 212, 191, 0.5) !important;
}
.user-pill.superuser img {
    border-color: #c9a84c !important;
    box-shadow: 0 0 14px rgba(201, 168, 76, 0.5) !important;
}
.user-pill .initial-avatar {
    width: 44px !important;
    height: 44px !important;
    border-radius: 50% !important;
    background: rgba(45, 212, 191, 0.2) !important;
    color: #2dd4bf !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    border: 2px solid #2dd4bf !important;
}
.user-pill.superuser .initial-avatar {
    background: rgba(201, 168, 76, 0.2) !important;
    color: #fbbf24 !important;
    border-color: #c9a84c !important;
}
.user-pill-name {
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    white-space: nowrap !important;
}
.btn-logout {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
    color: #fff !important;
    border: none !important;
    cursor: pointer !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    transition: .25s !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.35) !important;
    white-space: nowrap !important;
}
.btn-logout:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(239, 68, 68, 0.6) !important;
}
"""

admin_dirs = ['admin', 'www.manujungleforever.com/admin']
for d in admin_dirs:
    for fpath in glob.glob(f'{d}/*.html'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean previous header style injection
        content = re.sub(r'<style>\s*/\* Single-line header styles \*/.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*/\* Grand single-line header styles.*?</style>', '', content, flags=re.DOTALL)
        
        # Replace inline logo height with 110px
        content = re.sub(r'style="height:\s*\d+px[^"]*"', 'style="height: 110px; width: auto;"', content)
        
        # Inject CSS before </head>
        content = content.replace('</head>', f'<style>\n{grand_header_css}\n</style>\n</head>')
        
        # Ensure auth.js has cache bust v=6
        content = re.sub(r'src="js/auth\.js(\?v=\d+)?"', 'src="js/auth.js?v=6"', content)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated header in {fpath}")

