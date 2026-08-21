/**
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
      const baseText = this.text.replace(/\.+$/, '');
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
