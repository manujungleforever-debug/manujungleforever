import glob, os, re

# 1. Update thinking-orb.css
css_content = """/**
 * Thinking Orb Component Styles - Premium 3D Point-Cloud Loader
 */

#thinking-global-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(2, 6, 5, 0.85) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  z-index: 99999999 !important;
  display: none;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 16px !important;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  opacity: 0;
  pointer-events: all !important;
}

#thinking-global-overlay.active {
  display: flex !important;
  opacity: 1 !important;
}

.thinking-modal-card {
  background: rgba(13, 20, 24, 0.92) !important;
  border: 1px solid rgba(45, 212, 191, 0.35) !important;
  border-radius: 24px !important;
  padding: 28px 36px !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75),
              0 0 35px rgba(45, 212, 191, 0.22) !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  animation: orbModalPop 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
}

@keyframes orbModalPop {
  0% { transform: scale(0.85); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.thinking-modal-subtext {
  color: rgba(255, 255, 255, 0.65) !important;
  font-size: 0.82rem !important;
  font-weight: 400 !important;
  margin-top: 12px !important;
  letter-spacing: 0.3px !important;
}

.thinking-orb-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  width: 100%;
}

.thinking-orb-pill {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  background: rgba(13, 20, 24, 0.8);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(45, 212, 191, 0.3);
  border-radius: 9999px;
  padding: 8px 24px 8px 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 
              0 0 20px rgba(45, 212, 191, 0.15),
              inset 0 1px 1px rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
  user-select: none;
}

.thinking-orb-pill:hover {
  border-color: rgba(45, 212, 191, 0.5);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55), 0 0 25px rgba(45, 212, 191, 0.25);
}

.thinking-orb-canvas {
  display: block;
  flex-shrink: 0;
  border-radius: 50%;
  filter: drop-shadow(0 0 8px rgba(45, 212, 191, 0.55));
}

.thinking-orb-text {
  font-family: 'Poppins', 'Outfit', system-ui, -apple-system, sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #f1f5f9;
  letter-spacing: 0.2px;
  display: inline-flex;
  align-items: baseline;
}

.thinking-dots {
  display: inline-flex;
  margin-left: 1px;
}

.thinking-dots span {
  display: inline-block;
  opacity: 0.3;
  animation: thinkingDotPulse 1.4s infinite ease-in-out both;
}

.thinking-dots span:nth-child(1) { animation-delay: 0.0s; }
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
.thinking-dots span:nth-child(4) { animation-delay: 0.6s; }

@keyframes thinkingDotPulse {
  0%, 80%, 100% {
    opacity: 0.25;
    transform: translateY(0);
  }
  40% {
    opacity: 1;
    transform: translateY(-2px);
    color: var(--teal, #2dd4bf);
    text-shadow: 0 0 8px rgba(45, 212, 191, 0.8);
  }
}

.loading {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border: none !important;
  background: transparent !important;
}
"""

with open('admin/css/thinking-orb.css', 'w', encoding='utf-8') as f:
    f.write(css_content)
with open('www.manujungleforever.com/admin/css/thinking-orb.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# 2. Update thinking-orb.js
js_orb_content = """/**
 * Thinking Orb - Animated 3D Particle Orb Loader Component
 * Exact design with 3D sphere point-cloud rotation & "Thinking...." pill capsule.
 */

(function() {
  class ThinkingOrb {
    constructor(options = {}) {
      this.text = options.text || 'Thinking....';
      this.size = options.size || 36; // canvas diameter in px
      this.pointsCount = options.pointsCount || 140;
      this.speed = options.speed || 0.024;
      this.radius = this.size * 0.42;
      this.rotX = 0.35;
      this.rotY = 0;
      this.points = [];
      this.animId = null;
      this.active = false;
      this.initPoints();
    }

    initPoints() {
      const phi = Math.PI * (3 - Math.sqrt(5));
      for (let i = 0; i < this.pointsCount; i++) {
        const y = 1 - (i / (this.pointsCount - 1)) * 2;
        const radiusAtY = Math.sqrt(1 - y * y);
        const theta = phi * i;
        const x = Math.cos(theta) * radiusAtY;
        const z = Math.sin(theta) * radiusAtY;
        this.points.push({ x, y, z, baseRadius: (Math.random() * 0.4 + 0.8) });
      }
    }

    renderTo(container) {
      if (typeof container === 'string') {
        container = document.querySelector(container);
      }
      if (!container) return;

      const pill = document.createElement('div');
      pill.className = 'thinking-orb-pill';
      
      const canvas = document.createElement('canvas');
      const dpr = window.devicePixelRatio || 1;
      canvas.width = this.size * dpr;
      canvas.height = this.size * dpr;
      canvas.style.width = this.size + 'px';
      canvas.style.height = this.size + 'px';
      canvas.className = 'thinking-orb-canvas';

      const label = document.createElement('span');
      label.className = 'thinking-orb-text';
      const baseText = this.text.replace(/\\.+$/, '');
      label.innerHTML = `${baseText}<span class="thinking-dots"><span>.</span><span>.</span><span>.</span><span>.</span></span>`;

      pill.appendChild(canvas);
      pill.appendChild(label);
      container.innerHTML = '';
      container.appendChild(pill);

      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.dpr = dpr;
      this.start();
      return pill;
    }

    start() {
      if (this.active) return;
      this.active = true;
      const animate = () => {
        if (!this.active) return;
        this.draw();
        this.rotY += this.speed;
        this.rotX += this.speed * 0.35;
        this.animId = requestAnimationFrame(animate);
      };
      animate();
    }

    stop() {
      this.active = false;
      if (this.animId) {
        cancelAnimationFrame(this.animId);
        this.animId = null;
      }
    }

    draw() {
      const ctx = this.ctx;
      if (!ctx) return;
      const w = this.size * this.dpr;
      const h = this.size * this.dpr;
      const cx = w / 2;
      const cy = h / 2;
      const r = this.radius * this.dpr;

      ctx.clearRect(0, 0, w, h);

      const cosY = Math.cos(this.rotY), sinY = Math.sin(this.rotY);
      const cosX = Math.cos(this.rotX), sinX = Math.sin(this.rotX);

      const projected = [];
      for (let i = 0; i < this.points.length; i++) {
        const p = this.points[i];
        let x1 = p.x * cosY - p.z * sinY;
        let z1 = p.z * cosY + p.x * sinY;
        let y1 = p.y * cosX - z1 * sinX;
        let z2 = z1 * cosX + p.y * sinX;

        const fov = 300;
        const scale = fov / (fov + z2 * r);
        const px = cx + x1 * r * scale;
        const py = cy + y1 * r * scale;
        const alpha = Math.max(0.15, (z2 + 1.2) / 2.4);
        const pSize = Math.max(0.85, (z2 + 1.3) * 1.1 * this.dpr * p.baseRadius);

        projected.push({ px, py, z: z2, alpha, size: pSize });
      }

      projected.sort((a, b) => a.z - b.z);

      for (let i = 0; i < projected.length; i++) {
        const pt = projected[i];
        ctx.beginPath();
        ctx.arc(pt.px, pt.py, pt.size, 0, Math.PI * 2);
        
        if (pt.z > 0.25) {
          ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(1, pt.alpha * 1.25)})`;
        } else {
          ctx.fillStyle = `rgba(45, 212, 191, ${pt.alpha * 0.95})`;
        }
        ctx.fill();
      }
    }
  }

  // Global HTML template generator
  window.getThinkingLoaderHTML = function(text) {
    const id = 'orb_' + Math.random().toString(36).substr(2, 9);
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) window.renderThinkingOrb(el, text);
    }, 15);
    return `<div class="thinking-orb-container"><div id="${id}"></div></div>`;
  };

  // Helper to mount and auto-animate in any container
  window.renderThinkingOrb = function(targetEl, text) {
    if (typeof targetEl === 'string') targetEl = document.querySelector(targetEl);
    if (!targetEl) return null;
    const orb = new ThinkingOrb({ size: 36, text: text || 'Thinking....' });
    orb.renderTo(targetEl);
    return orb;
  };

  // Global Fullscreen Overlay for Saving & Background Actions
  window.showThinkingOverlay = function(title = 'Guardando cambios....', subtext = 'Sincronizando datos con GitHub y Cloudflare Pages') {
    let overlay = document.getElementById('thinking-global-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'thinking-global-overlay';
      document.body.appendChild(overlay);
    }
    overlay.innerHTML = `
      <div class="thinking-modal-card">
        <div id="thinking-orb-mount"></div>
        <div class="thinking-modal-subtext">${subtext}</div>
      </div>
    `;
    const mount = document.getElementById('thinking-orb-mount');
    const orb = new ThinkingOrb({ size: 48, text: title });
    orb.renderTo(mount);
    overlay.classList.add('active');
    window._activeThinkingOrb = orb;
  };

  window.hideThinkingOverlay = function() {
    const overlay = document.getElementById('thinking-global-overlay');
    if (overlay) {
      overlay.classList.remove('active');
      setTimeout(() => {
        if (window._activeThinkingOrb) {
          window._activeThinkingOrb.stop();
          window._activeThinkingOrb = null;
        }
      }, 300);
    }
  };

  // MutationObserver to auto-upgrade any dynamic `.loading` container into Thinking Orb
  const observer = new MutationObserver((mutations) => {
    document.querySelectorAll('.loading').forEach(el => {
      if (!el.dataset.thinkingInitialized) {
        el.dataset.thinkingInitialized = 'true';
        window.renderThinkingOrb(el);
      }
    });
  });

  document.addEventListener('DOMContentLoaded', () => {
    observer.observe(document.body, { childList: true, subtree: true });
    document.querySelectorAll('.loading, .thinking-orb-mount').forEach(el => {
      el.dataset.thinkingInitialized = 'true';
      window.renderThinkingOrb(el);
    });
  });

  window.ThinkingOrb = ThinkingOrb;
})();
"""

with open('admin/js/thinking-orb.js', 'w', encoding='utf-8') as f:
    f.write(js_orb_content)
with open('www.manujungleforever.com/admin/js/thinking-orb.js', 'w', encoding='utf-8') as f:
    f.write(js_orb_content)

# 3. Update auth.js
auth_content = """(function () {
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
    f.write(auth_content)
with open('www.manujungleforever.com/admin/js/auth.js', 'w', encoding='utf-8') as f:
    f.write(auth_content)

# 4. Ensure all admin HTML files have thinking-orb.js & auth.js & css loaded in <head> with ?v=8
admin_dirs = ['admin', 'www.manujungleforever.com/admin']

for d in admin_dirs:
    for fpath in glob.glob(os.path.join(d, 'gestionar-*.html')) + glob.glob(os.path.join(d, 'index.html')) + glob.glob(os.path.join(d, 'panel.html')):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()

        # Ensure css in head
        if 'thinking-orb.css' not in c:
            c = c.replace('</head>', '  <link rel="stylesheet" href="css/thinking-orb.css?v=8">\n</head>')
        else:
            c = re.sub(r'href="css/thinking-orb\.css(?:\?v=\d+)?"', 'href="css/thinking-orb.css?v=8"', c)

        # Ensure js in head or top of body
        if 'js/thinking-orb.js' not in c:
            c = c.replace('</head>', '  <script src="js/thinking-orb.js?v=8"></script>\n</head>')
        else:
            c = re.sub(r'src="js/thinking-orb\.js(?:\?v=\d+)?"', 'src="js/thinking-orb.js?v=8"', c)

        c = re.sub(r'src="js/auth\.js(?:\?v=\d+)?"', 'src="js/auth.js?v=8"', c)

        # In gestionar-salidas.html: ensure savePax, deletePax, adjPlaza show Thinking Orb
        if 'gestionar-salidas.html' in fpath:
            # savePax
            c = re.sub(
                r"window\.savePax\s*=\s*async\s*function\(sIdx,\s*pIdx,\s*event\)\s*\{",
                "window.savePax = async function(sIdx, pIdx, event) {\n  if(window.showThinkingOverlay) window.showThinkingOverlay('Guardando pasajero....', 'Sincronizando manifiesto con GitHub y Cloudflare');",
                c
            )
            c = re.sub(
                r"cSha\s*=\s*res\.sha;\s*viewPax\(sIdx\);",
                "cSha = res.sha;\n    if(window.hideThinkingOverlay) window.hideThinkingOverlay();\n    viewPax(sIdx);",
                c
            )
            # deletePax
            c = re.sub(
                r"window\.deletePax\s*=\s*async\s*function\(sIdx,\s*pIdx\)\s*\{",
                "window.deletePax = async function(sIdx, pIdx) {\n  if (!confirm('¿Estás seguro de eliminar este pasajero?')) return;\n  if(window.showThinkingOverlay) window.showThinkingOverlay('Eliminando pasajero....');",
                c
            )
            # adjPlaza
            c = re.sub(
                r"window\.adjPlaza\s*=\s*async\s*function\(idx,\s*diff\)\s*\{",
                "window.adjPlaza = async function(idx, diff) {\n  if(window.showThinkingOverlay) window.showThinkingOverlay('Actualizando plazas....');",
                c
            )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated scripts and overlay hooks in {fpath}")

print("All components updated successfully.")
