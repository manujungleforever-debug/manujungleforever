/**
 * thinking-orb.js — Ultra-Fine Fiber-Optic "Solving" Orb Loader
 * Inspired by orbs.jakubantalik.com ("Solving" preset)
 * Features intertwined neon cyan/turquoise parametric filaments, micro-sparks,
 * fluid vortex tension, and 60fps lightweight canvas rendering.
 */

(function() {
  class SolvingOrb {
    constructor(options = {}) {
      this.text = options.text || 'Guardando cambios...';
      this.subtext = options.subtext || 'Sincronizando datos con GitHub y Cloudflare Pages';
      this.size = options.size || 48; // Canvas display size in px
      this.speed = options.speed || 0.022;
      this.strandCount = options.strandCount || 20; // Number of intertwined fiber filaments
      this.pointsPerStrand = options.pointsPerStrand || 64; // Resolution per filament
      this.nodeSparkCount = options.nodeSparkCount || 36; // Luminous crossover nodes
      
      this.time = 0;
      this.rotX = 0.45;
      this.rotY = 0.2;
      this.rotZ = 0.1;
      this.animId = null;
      this.active = false;
      
      this.initNodes();
    }

    initNodes() {
      // Pre-calculate node sparks along the harmonic sphere
      this.nodeOffsets = [];
      for (let i = 0; i < this.nodeSparkCount; i++) {
        this.nodeOffsets.push({
          strandIdx: Math.floor(Math.random() * this.strandCount),
          tOffset: Math.random() * Math.PI * 2,
          speedMult: 0.8 + Math.random() * 0.4,
          sizeMult: 0.7 + Math.random() * 0.6
        });
      }
    }

    renderTo(container) {
      if (typeof container === 'string') {
        container = document.querySelector(container);
      }
      if (!container) return;

      const pill = document.createElement('div');
      pill.className = 'thinking-orb-pill solving-preset';
      
      const canvas = document.createElement('canvas');
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = this.size * dpr;
      canvas.height = this.size * dpr;
      canvas.style.width = this.size + 'px';
      canvas.style.height = this.size + 'px';
      canvas.className = 'thinking-orb-canvas';

      const labelWrap = document.createElement('div');
      labelWrap.className = 'thinking-orb-text-col';

      const mainLabel = document.createElement('div');
      mainLabel.className = 'thinking-orb-title';
      const cleanTitle = this.text.replace(/\.+$/, '');
      mainLabel.innerHTML = `${cleanTitle}<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>`;

      labelWrap.appendChild(mainLabel);
      if (this.subtext) {
        const subLabel = document.createElement('div');
        subLabel.className = 'thinking-orb-subtext';
        subLabel.textContent = this.subtext;
        labelWrap.appendChild(subLabel);
      }

      pill.appendChild(canvas);
      pill.appendChild(labelWrap);
      
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
        this.time += this.speed;
        this.rotY += this.speed * 0.85;
        this.rotX += this.speed * 0.45;
        this.rotZ += this.speed * 0.3;
        this.draw();
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

      const dpr = this.dpr;
      const w = this.size * dpr;
      const h = this.size * dpr;
      const cx = w / 2;
      const cy = h / 2;
      const baseR = (this.size * 0.40) * dpr;

      ctx.clearRect(0, 0, w, h);

      // 1. Center Glow Nebula Core
      const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, baseR * 1.05);
      coreGrad.addColorStop(0, 'rgba(0, 242, 254, 0.28)');
      coreGrad.addColorStop(0.45, 'rgba(16, 185, 129, 0.12)');
      coreGrad.addColorStop(0.85, 'rgba(6, 182, 212, 0.04)');
      coreGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = coreGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, baseR * 1.1, 0, Math.PI * 2);
      ctx.fill();

      // 3D Rotation Matrix Trigonometry
      const cosX = Math.cos(this.rotX), sinX = Math.sin(this.rotX);
      const cosY = Math.cos(this.rotY), sinY = Math.sin(this.rotY);
      const cosZ = Math.cos(this.rotZ), sinZ = Math.sin(this.rotZ);

      const project = (x, y, z) => {
        // Rotate Y
        let x1 = x * cosY - z * sinY;
        let z1 = z * cosY + x * sinY;
        // Rotate X
        let y1 = y * cosX - z1 * sinX;
        let z2 = z1 * cosX + y * sinX;
        // Rotate Z
        let x2 = x1 * cosZ - y1 * sinZ;
        let y2 = y1 * cosZ + x1 * sinZ;

        const fov = 350 * dpr;
        const scale = fov / (fov + z2);
        return {
          px: cx + x2 * scale,
          py: cy + y2 * scale,
          z: z2,
          scale: scale
        };
      };

      ctx.save();
      ctx.globalCompositeOperation = 'lighter';

      // 2. Render Intertwined Fiber Optic Strands ("Solving" Harmonic Mesh)
      const numStrands = this.strandCount;
      const ptsPerStrand = this.pointsPerStrand;
      const t = this.time;

      for (let s = 0; s < numStrands; s++) {
        // Spatial angle orientation of each filament loop
        const phi = (s / numStrands) * Math.PI;
        const phaseOffset = s * 0.35 + (s % 2 === 0 ? t * 0.4 : -t * 0.3);
        
        ctx.beginPath();
        let firstPt = true;
        let avgZ = 0;

        for (let p = 0; p <= ptsPerStrand; p++) {
          const theta = (p / ptsPerStrand) * Math.PI * 2;
          
          // Solving fluid tension wave formula
          const wave1 = Math.sin(theta * 3 + t * 2.2 + phaseOffset) * 0.16;
          const wave2 = Math.cos(theta * 5 - t * 1.6 + phi) * 0.09;
          const r = baseR * (0.92 + wave1 + wave2);

          // Parametric spherical torus coordinates
          const x0 = r * Math.cos(theta) * Math.cos(phi);
          const y0 = r * Math.sin(theta);
          const z0 = r * Math.cos(theta) * Math.sin(phi);

          const proj = project(x0, y0, z0);
          avgZ += proj.z;

          if (firstPt) {
            ctx.moveTo(proj.px, proj.py);
            firstPt = false;
          } else {
            ctx.lineTo(proj.px, proj.py);
          }
        }

        avgZ /= (ptsPerStrand + 1);

        // Filament Depth Coloring (Cian #00f2fe to Turquoise #10b981 to Deep Teal #06b6d4)
        const depthNorm = Math.max(0, Math.min(1, (avgZ + baseR) / (baseR * 2)));
        const alpha = 0.22 + depthNorm * 0.55;
        
        ctx.lineWidth = Math.max(0.65, 0.9 * dpr * (0.8 + depthNorm * 0.4));
        
        if (s % 3 === 0) {
          ctx.strokeStyle = `rgba(0, 242, 254, ${alpha})`; // Electric Cyan
        } else if (s % 3 === 1) {
          ctx.strokeStyle = `rgba(45, 212, 191, ${alpha * 0.95})`; // Neon Teal
        } else {
          ctx.strokeStyle = `rgba(16, 185, 129, ${alpha * 0.85})`; // Emerald Mint
        }
        
        ctx.stroke();
      }

      // 3. Render Luminous Node Sparks (Intersection Energy Particles)
      for (let n = 0; n < this.nodeOffsets.length; n++) {
        const node = this.nodeOffsets[n];
        const theta = node.tOffset + t * node.speedMult;
        const phi = (node.strandIdx / numStrands) * Math.PI;

        const wave = Math.sin(theta * 3 + t * 2.2) * 0.15;
        const r = baseR * (0.92 + wave);

        const x0 = r * Math.cos(theta) * Math.cos(phi);
        const y0 = r * Math.sin(theta);
        const z0 = r * Math.cos(theta) * Math.sin(phi);

        const proj = project(x0, y0, z0);

        if (proj.z > -baseR * 0.4) {
          const sparkNorm = Math.max(0.2, (proj.z + baseR) / (baseR * 2));
          const sparkSize = Math.max(0.7, 1.1 * dpr * node.sizeMult * sparkNorm);

          ctx.beginPath();
          ctx.arc(proj.px, proj.py, sparkSize, 0, Math.PI * 2);
          
          if (sparkNorm > 0.65) {
            ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(1, sparkNorm * 1.3)})`;
          } else {
            ctx.fillStyle = `rgba(0, 242, 254, ${sparkNorm * 0.95})`;
          }
          ctx.fill();
        }
      }

      ctx.restore();
    }
  }

  // Inject updated CSS for the Solving Orb modal capsule
  function injectSolvingStyles() {
    if (document.getElementById('solving-orb-custom-styles')) return;
    const s = document.createElement('style');
    s.id = 'solving-orb-custom-styles';
    s.textContent = `
      #thinking-global-overlay {
        position: fixed !important;
        inset: 0 !important;
        background: rgba(4, 9, 13, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        z-index: 99999999 !important;
        display: none;
        align-items: center !important;
        justify-content: center !important;
        padding: 20px !important;
        opacity: 0;
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        pointer-events: all !important;
      }
      #thinking-global-overlay.active {
        display: flex !important;
        opacity: 1 !important;
      }
      .thinking-modal-card {
        background: radial-gradient(circle at 50% 30%, rgba(18, 30, 36, 0.95) 0%, rgba(8, 14, 18, 0.98) 100%) !important;
        border: 1.5px solid rgba(0, 242, 254, 0.35) !important;
        border-radius: 24px !important;
        padding: 24px 32px !important;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85),
                    0 0 35px rgba(0, 242, 254, 0.22),
                    inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        max-width: 480px !important;
        width: 100% !important;
        animation: orbModalPop 0.32s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards !important;
      }
      .thinking-orb-pill.solving-preset {
        display: inline-flex !important;
        align-items: center !important;
        gap: 16px !important;
        background: rgba(12, 22, 28, 0.75) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(45, 212, 191, 0.3) !important;
        border-radius: 9999px !important;
        padding: 8px 24px 8px 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 
                    0 0 20px rgba(0, 242, 254, 0.18),
                    inset 0 1px 1px rgba(255, 255, 255, 0.12) !important;
        transition: all 0.3s ease !important;
      }
      .thinking-orb-text-col {
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        text-align: left !important;
      }
      .thinking-orb-title {
        font-family: 'Poppins', 'Outfit', system-ui, -apple-system, sans-serif !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.2px !important;
        display: inline-flex !important;
        align-items: baseline !important;
      }
      .thinking-orb-subtext {
        font-size: 0.78rem !important;
        color: rgba(255, 255, 255, 0.65) !important;
        font-weight: 400 !important;
        margin-top: 3px !important;
        letter-spacing: 0.2px !important;
      }
      .thinking-modal-subtext {
        color: rgba(255, 255, 255, 0.68) !important;
        font-size: 0.83rem !important;
        font-weight: 400 !important;
        margin-top: 14px !important;
        text-align: center !important;
        letter-spacing: 0.2px !important;
      }
      .thinking-orb-canvas {
        display: block !important;
        flex-shrink: 0 !important;
        border-radius: 50% !important;
        filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.6)) !important;
      }
      .thinking-dots span {
        display: inline-block;
        opacity: 0.3;
        animation: thinkingDotPulse 1.4s infinite ease-in-out both;
      }
      .thinking-dots span:nth-child(1) { animation-delay: 0.0s; }
      .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
      .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
      @keyframes thinkingDotPulse {
        0%, 80%, 100% { opacity: 0.2; transform: translateY(0); }
        40% { opacity: 1; color: #00f2fe; transform: translateY(-2px); }
      }
    `;
    document.head.appendChild(s);
  }

  // Global HTML template generator
  window.getThinkingLoaderHTML = function(text, subtext) {
    injectSolvingStyles();
    const id = 'orb_' + Math.random().toString(36).substr(2, 9);
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) window.renderThinkingOrb(el, text, subtext);
    }, 15);
    return `<div class="thinking-orb-container"><div id="${id}"></div></div>`;
  };

  // Helper to mount and auto-animate in any container
  window.renderThinkingOrb = function(targetEl, text, subtext) {
    injectSolvingStyles();
    if (typeof targetEl === 'string') targetEl = document.querySelector(targetEl);
    if (!targetEl) return null;
    const orb = new SolvingOrb({ size: 42, text: text || 'Guardando cambios...', subtext: subtext || '' });
    orb.renderTo(targetEl);
    return orb;
  };

  // Global Fullscreen Overlay for Saving & Background Actions
  window.showThinkingOverlay = function(title = 'Guardando cambios...', subtext = 'Sincronizando datos con GitHub y Cloudflare Pages') {
    injectSolvingStyles();
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
    const orb = new SolvingOrb({ size: 54, text: title, subtext: '' });
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

  // Aliases for compatibility
  window.ThinkingOrb = SolvingOrb;
  window.SolvingOrb = SolvingOrb;

  document.addEventListener('DOMContentLoaded', () => {
    injectSolvingStyles();
    document.querySelectorAll('.loading, .thinking-orb-mount').forEach(el => {
      if (!el.dataset.thinkingInitialized) {
        el.dataset.thinkingInitialized = 'true';
        window.renderThinkingOrb(el);
      }
    });
  });
})();
