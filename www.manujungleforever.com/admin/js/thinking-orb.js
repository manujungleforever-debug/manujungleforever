/**
 * thinking-orb.js — Mathematically Perfect Spherical Solving Orb
 * Features strict spherical clamping (100% round 3D silhouette),
 * intertwined geodesic/orbital fiber filaments (0.5-0.7px ultra-fine),
 * luminous core mass, depth-attenuated alpha, and 60 FPS requestAnimationFrame.
 */

(function() {
  class SolvingOrb {
    constructor(options = {}) {
      this.text = options.text || 'Guardando cambios...';
      this.size = options.size || 48; // Display size in px
      this.speed = options.speed || 0.016;
      this.strandCount = options.strandCount || 28; // Number of spherical orbital rings
      this.pointsPerStrand = options.pointsPerStrand || 80; // Smooth curve resolution
      this.nodeSparkCount = options.nodeSparkCount || 36; // Luminous surface nodes
      
      this.time = 0;
      this.rotX = 0.35;
      this.rotY = 0.0;
      this.rotZ = 0.15;
      this.animId = null;
      this.active = false;
      
      this.initNodes();
    }

    initNodes() {
      // Micro-sparks distributed along the spherical orbital rings
      this.nodeOffsets = [];
      for (let i = 0; i < this.nodeSparkCount; i++) {
        this.nodeOffsets.push({
          strandIdx: i % this.strandCount,
          thetaOffset: (i / this.nodeSparkCount) * Math.PI * 2,
          speedMult: 0.85 + (i % 5) * 0.08
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
      const dpr = Math.max(1, window.devicePixelRatio || 1);
      canvas.width = Math.round(this.size * dpr);
      canvas.height = Math.round(this.size * dpr);
      canvas.style.width = this.size + 'px';
      canvas.style.height = this.size + 'px';
      canvas.className = 'thinking-orb-canvas';

      const mainLabel = document.createElement('span');
      mainLabel.className = 'thinking-orb-title';
      const cleanTitle = this.text.replace(/\.+$/, '');
      mainLabel.innerHTML = `${cleanTitle}<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>`;

      // Clean structure: Pill has ONLY the canvas and the title
      pill.appendChild(canvas);
      pill.appendChild(mainLabel);
      
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
        this.rotY += 0.014;
        this.rotX += 0.007;
        this.rotZ += 0.004;
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
      const w = this.canvas.width;
      const h = this.canvas.height;
      const cx = w / 2;
      const cy = h / 2;
      const baseR = (this.size * 0.41) * dpr;

      ctx.clearRect(0, 0, w, h);

      // 1. Internal Core Mass Gradient (Solid Sphere Density & Inner Glow)
      const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, baseR * 0.98);
      coreGrad.addColorStop(0, 'rgba(0, 242, 254, 0.32)');
      coreGrad.addColorStop(0.40, 'rgba(45, 212, 191, 0.16)');
      coreGrad.addColorStop(0.75, 'rgba(16, 185, 129, 0.06)');
      coreGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = coreGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, baseR * 1.0, 0, Math.PI * 2);
      ctx.fill();

      // 3D Precession Rotation Matrix
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

        const fov = 380 * dpr;
        const scale = fov / (fov + z2);
        return {
          px: cx + x2 * scale,
          py: cy + y2 * scale,
          z: z2
        };
      };

      ctx.save();
      // Optical additive blending for brilliant glowing filaments
      ctx.globalCompositeOperation = 'lighter';

      const numStrands = this.strandCount;
      const ptsPerStrand = this.pointsPerStrand;
      const t = this.time;

      // 2. Strict Spherical Orbital Filaments (Mathematically Clamped Sphere Surface)
      for (let s = 0; s < numStrands; s++) {
        // Inclination angle for orbital plane
        const phi = (s / numStrands) * Math.PI;
        // Precession phase angle
        const psi = s * 0.42 + t * (s % 2 === 0 ? 0.35 : -0.28);
        
        const cosPhi = Math.cos(phi), sinPhi = Math.sin(phi);
        const cosPsi = Math.cos(psi), sinPsi = Math.sin(psi);

        ctx.beginPath();
        let firstPt = true;
        let avgZ = 0;

        for (let p = 0; p <= ptsPerStrand; p++) {
          const theta = (p / ptsPerStrand) * Math.PI * 2;
          const cosTheta = Math.cos(theta);
          const sinTheta = Math.sin(theta);

          // Strict spherical geodesic coordinates: u = cos(theta), v = sin(theta)*cos(phi), w = sin(theta)*sin(phi)
          // 0% deformation: perfect 3D sphere
          const x0 = baseR * (cosTheta * cosPsi - sinTheta * cosPhi * sinPsi);
          const y0 = baseR * (cosTheta * sinPsi + sinTheta * cosPhi * cosPsi);
          const z0 = baseR * (sinTheta * sinPhi);

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

        // Depth Attenuation: Back strands (z < 0) are dim (0.18-0.35); front strands (z > 0) are bright (0.75-1.0)
        const depthNorm = Math.max(0, Math.min(1, (avgZ + baseR) / (baseR * 2)));
        const alpha = avgZ > 0 ? (0.65 + depthNorm * 0.35) : (0.16 + depthNorm * 0.45);
        
        // Strict ultra-fine line width: 0.55px to 0.70px
        ctx.lineWidth = Math.max(0.5 * dpr, 0.65 * dpr * (0.85 + depthNorm * 0.3));

        if (s % 3 === 0) {
          ctx.strokeStyle = `rgba(0, 242, 254, ${alpha})`; // Electric Cyan
        } else if (s % 3 === 1) {
          ctx.strokeStyle = `rgba(45, 212, 191, ${alpha * 0.95})`; // Neon Turquoise
        } else {
          ctx.strokeStyle = `rgba(6, 182, 212, ${alpha * 0.88})`; // Vibrant Teal
        }

        ctx.stroke();
      }

      // 3. Luminous Surface Sparks at Intersection Nodes
      for (let n = 0; n < this.nodeOffsets.length; n++) {
        const node = this.nodeOffsets[n];
        const s = node.strandIdx;
        const phi = (s / numStrands) * Math.PI;
        const psi = s * 0.42 + t * (s % 2 === 0 ? 0.35 : -0.28);
        const theta = node.thetaOffset + t * node.speedMult;

        const cosPhi = Math.cos(phi), sinPhi = Math.sin(phi);
        const cosPsi = Math.cos(psi), sinPsi = Math.sin(psi);
        const cosTheta = Math.cos(theta), sinTheta = Math.sin(theta);

        const r = baseR * (1.0 + 0.025 * Math.sin(theta * 3 + t * 2.0));
        const x0 = r * (cosTheta * cosPsi - sinTheta * cosPhi * sinPsi);
        const y0 = r * (cosTheta * sinPsi + sinTheta * cosPhi * cosPsi);
        const z0 = r * (sinTheta * sinPhi);

        const proj = project(x0, y0, z0);

        // Only draw visible sparks on the frontal/upper hemisphere
        if (proj.z > -baseR * 0.25) {
          const sparkNorm = Math.max(0.2, (proj.z + baseR) / (baseR * 2));
          const sparkRadius = Math.max(0.45 * dpr, 0.65 * dpr * sparkNorm);

          ctx.beginPath();
          ctx.arc(proj.px, proj.py, sparkRadius, 0, Math.PI * 2);
          
          if (sparkNorm > 0.65) {
            ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(1, sparkNorm * 1.35)})`;
          } else {
            ctx.fillStyle = `rgba(0, 242, 254, ${sparkNorm * 0.95})`;
          }
          ctx.fill();
        }
      }

      ctx.restore();
    }
  }

  // Inject styles for the Solving Orb modal and pill
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
        padding: 26px 34px !important;
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
        gap: 14px !important;
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
      .thinking-orb-title {
        font-family: 'Poppins', 'Outfit', system-ui, -apple-system, sans-serif !important;
        font-size: 0.98rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.2px !important;
        display: inline-flex !important;
        align-items: baseline !important;
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
        filter: drop-shadow(0 0 12px rgba(0, 242, 254, 0.65)) !important;
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
  window.getThinkingLoaderHTML = function(text) {
    injectSolvingStyles();
    const id = 'orb_' + Math.random().toString(36).substr(2, 9);
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) window.renderThinkingOrb(el, text);
    }, 15);
    return `<div class="thinking-orb-container"><div id="${id}"></div></div>`;
  };

  // Helper to mount and auto-animate in any container
  window.renderThinkingOrb = function(targetEl, text) {
    injectSolvingStyles();
    if (typeof targetEl === 'string') targetEl = document.querySelector(targetEl);
    if (!targetEl) return null;
    const orb = new SolvingOrb({ size: 42, text: text || 'Guardando cambios...' });
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
    // Se estructura limpiamente: cápsula central (pill) y subtexto único.
    overlay.innerHTML = `
      <div class="thinking-modal-card" style="display:flex; flex-direction:column; align-items:center; gap:16px;">
        <div id="thinking-orb-mount"></div>
        <div class="thinking-modal-subtext" style="text-align:center; opacity:0.8; font-size:0.85rem; margin-top:-8px;">${subtext}</div>
      </div>
    `;
    const mount = document.getElementById('thinking-orb-mount');
    const orb = new SolvingOrb({ size: 52, text: title });
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
