"""
inject_animations.py
Safely injects:
  1. Preloader (logo palpitante + anillos giratorios) — solo primera carga (sessionStorage)
  2. WhatsApp floating button con pulso neón

Reglas críticas:
  - NUNCA modifica atributos del tag <body>
  - Solo inserta HTML/CSS, no reemplaza estructuras existentes
  - Detecta si ya está inyectado y lo saltea o reemplaza limpiamente
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'www.hiddenjunglecusco.com'

# ── CSS del Preloader ──────────────────────────────────────────────────────────
PRELOADER_CSS = """
/* ── Global Preloader (HJC) ── */
#hjc-preloader {
  position: fixed; inset: 0;
  background: radial-gradient(ellipse at center, #0a1a0f 0%, #050d08 100%);
  z-index: 999999;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.7s ease, visibility 0.7s ease;
}
#hjc-preloader.hjc-fade { opacity: 0; visibility: hidden; }
.hjc-wrap {
  position: relative; width: 180px; height: 180px;
  display: flex; align-items: center; justify-content: center;
}
.hjc-logo {
  width: 96px; height: 96px; border-radius: 50%; z-index: 10;
  animation: hjcPulse 2s ease-in-out infinite;
  filter: drop-shadow(0 0 6px rgba(57,255,106,0.25));
}
.hjc-ring {
  position: absolute; top: 50%; left: 50%;
  border-radius: 50%; background: transparent; pointer-events: none;
}
.hjc-ring-1 {
  width: 128px; height: 128px;
  border: 2.5px solid transparent;
  border-top-color: #39ff6a; border-bottom-color: #39ff6a;
  box-shadow: 0 0 12px rgba(57,255,106,0.35);
  animation: hjcSpin 3s linear infinite;
}
.hjc-ring-2 {
  width: 152px; height: 152px;
  border: 2px solid transparent;
  border-left-color: #c9a84c; border-right-color: #c9a84c;
  box-shadow: 0 0 10px rgba(201,168,76,0.3);
  animation: hjcSpin 5s linear infinite reverse;
}
.hjc-ring-3 {
  width: 176px; height: 176px;
  border: 1.5px dashed rgba(57,255,106,0.35);
  animation: hjcSpin 8s linear infinite;
}
@keyframes hjcSpin {
  to { transform: translate(-50%,-50%) rotate(360deg); }
}
@keyframes hjcPulse {
  0%,100% { transform: scale(1);    filter: drop-shadow(0 0 5px rgba(57,255,106,0.25)); }
  50%      { transform: scale(1.08); filter: drop-shadow(0 0 18px rgba(57,255,106,0.65)); }
}
"""

# ── HTML del Preloader ─────────────────────────────────────────────────────────
PRELOADER_HTML = """<!-- HJC Preloader -->
<div id="hjc-preloader">
  <div class="hjc-wrap">
    <div class="hjc-ring hjc-ring-1"></div>
    <div class="hjc-ring hjc-ring-2"></div>
    <div class="hjc-ring hjc-ring-3"></div>
    <img src="{rel}wp-content/uploads/2018/01/cropped-HJC_Logo_PlainSeal_2Color-192x192.png"
         alt="Hidden Jungle Cusco" class="hjc-logo">
  </div>
</div>
<script>
(function(){{
  var p = document.getElementById('hjc-preloader');
  if (!p) return;
  if (sessionStorage.getItem('hjc_loaded')) {{ p.style.display='none'; return; }}
  var t0 = Date.now(), done = false;
  function hide() {{
    var elapsed = Date.now() - t0;
    if (elapsed < 2500) {{ setTimeout(hide, 2500 - elapsed); return; }}
    p.classList.add('hjc-fade');
    sessionStorage.setItem('hjc_loaded','1');
    setTimeout(function(){{ p.parentNode && p.parentNode.removeChild(p); }}, 750);
  }}
  window.addEventListener('load', function(){{ done=true; hide(); }});
  setTimeout(function(){{ if(!done){{ done=true; hide(); }} }}, 7000);
}})();
</script>
"""

# ── CSS del botón WhatsApp ─────────────────────────────────────────────────────
WA_CSS = """
/* ── WhatsApp Neon Float ── */
.wa-wrap {
  position: fixed; bottom: 28px; right: 28px;
  width: 60px; height: 60px; z-index: 9998;
  display: flex; align-items: center; justify-content: center;
}
.wa-ring {
  position: absolute; top: 0; left: 0;
  width: 60px; height: 60px; border-radius: 50%;
  border: 2px solid #39ff6a; opacity: 0;
  animation: waPulse 2.6s ease-out infinite;
  pointer-events: none;
}
.wa-ring:nth-child(2) { animation-delay: 0.8s; }
.wa-ring:nth-child(3) { animation-delay: 1.6s; }
@keyframes waPulse {
  0%   { transform: scale(1);   opacity: .85; }
  100% { transform: scale(2.5); opacity: 0;   }
}
.wa {
  position: relative; z-index: 1;
  width: 60px; height: 60px; border-radius: 50%;
  background: linear-gradient(135deg,#25d366,#128c50);
  color: #fff; font-size: 1.75rem;
  display: flex; align-items: center; justify-content: center;
  text-decoration: none;
  box-shadow: 0 0 0 3px rgba(57,255,106,.3), 0 0 18px rgba(57,255,106,.5), 0 8px 24px rgba(0,0,0,.4);
  animation: waBeat 2.6s ease-in-out infinite;
  transition: transform .25s, box-shadow .25s;
  bottom: auto !important; right: auto !important; margin: 0 !important;
}
.wa:hover {
  transform: scale(1.12);
  box-shadow: 0 0 0 4px rgba(57,255,106,.5), 0 0 30px rgba(57,255,106,.8), 0 12px 32px rgba(0,0,0,.5);
}
@keyframes waBeat {
  0%,100% { transform: scale(1);    }
  50%      { transform: scale(1.07); }
}
"""

# ── HTML del botón WhatsApp ────────────────────────────────────────────────────
WA_HTML = """<div class="wa-wrap" id="whats-flotante">
  <span class="wa-ring"></span>
  <span class="wa-ring"></span>
  <span class="wa-ring"></span>
  <a href="https://api.whatsapp.com/send?phone=51923289231&text=Hello!%20I%20would%20like%20to%20learn%20more%20about%20your%20jungle%20trips"
     class="wa" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
    <i class="fab fa-whatsapp"></i>
  </a>
</div>
"""

# ── Calcular el prefijo relativo según la profundidad del archivo ──────────────
def rel_prefix(filepath):
    rel = os.path.relpath(filepath, ROOT)
    depth = len(rel.split(os.sep)) - 1  # número de carpetas entre el archivo y ROOT
    return '../' * depth if depth > 0 else ''

# ── Procesar cada archivo HTML ─────────────────────────────────────────────────
html_files = []
for dirpath, dirs, files in os.walk(ROOT):
    # Excluir directorios del sistema WordPress que no son páginas reales
    dirs[:] = [d for d in dirs if d not in ('https_', "'https_", 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if fname.endswith('.html') and fname != 'original_raw.html':
            html_files.append(os.path.join(dirpath, fname))

print(f"Total HTML files found: {len(html_files)}")

injected = 0
skipped  = 0
errors   = 0

for fpath in sorted(html_files):
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Solo procesar archivos que tengan estructura HTML real
        if '<body' not in content or '</html>' not in content:
            skipped += 1
            continue

        changed = False
        rel = rel_prefix(fpath)

        # ── 1. Inyectar CSS del preloader + WA antes del </style> más cercano al </head> ──
        # Usamos el bloque <style> que ya existe en la página o añadimos uno nuevo
        preloader_marker = '/* ── Global Preloader (HJC) ── */'
        wa_marker        = '/* ── WhatsApp Neon Float ── */'

        if preloader_marker not in content:
            # Insertar antes del cierre </style> que esté dentro del <head>
            # Buscamos el </style> que aparece ANTES de </head>
            head_end = content.find('</head>')
            style_end = content.rfind('</style>', 0, head_end) if head_end > 0 else -1
            if style_end > 0:
                content = content[:style_end] + PRELOADER_CSS + '\n' + content[style_end:]
            else:
                # No hay style block antes del </head> — añadir bloque nuevo
                if head_end > 0:
                    content = content[:head_end] + '<style>' + PRELOADER_CSS + '</style>\n' + content[head_end:]
            changed = True

        if wa_marker not in content:
            head_end = content.find('</head>')
            style_end = content.rfind('</style>', 0, head_end) if head_end > 0 else -1
            if style_end > 0:
                content = content[:style_end] + WA_CSS + '\n' + content[style_end:]
            else:
                if head_end > 0:
                    content = content[:head_end] + '<style>' + WA_CSS + '</style>\n' + content[head_end:]
            changed = True

        # ── 2. Inyectar HTML del preloader justo DESPUÉS de <body (preservando attrs) ──
        if 'id="hjc-preloader"' not in content:
            # Encontrar fin del tag <body ...>
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                insert_pos = body_match.end()
                preloader_with_rel = PRELOADER_HTML.replace('{rel}', rel)
                content = content[:insert_pos] + '\n' + preloader_with_rel + content[insert_pos:]
                changed = True

        # ── 3. Reemplazar el botón WA simple por el wrapper con anillos ──
        # Patrón: <a href="...whatsapp..." class="wa" ...>...</a> que NO esté dentro de wa-wrap
        if 'class="wa-wrap"' not in content:
            # Quitar cualquier versión vieja del botón flotante (id="whats-flotante" en <a>)
            content = re.sub(
                r'<a\s[^>]*id=["\']whats-flotante["\'][^>]*>.*?</a>',
                '', content, flags=re.DOTALL
            )
            # También quitar <a class="wa" ...> standalone (fuera de wa-wrap)
            content = re.sub(
                r'\n?<a\s+href="https://api\.whatsapp[^"]*"\s+class="wa"[^>]*>.*?</a>\n?',
                '', content, flags=re.DOTALL
            )
            # Insertar nuevo bloque wa-wrap antes de </body>
            body_close = content.rfind('</body>')
            if body_close > 0:
                content = content[:body_close] + '\n' + WA_HTML + '\n' + content[body_close:]
                changed = True

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            injected += 1
            rel_display = os.path.relpath(fpath, ROOT)
            print(f"  ✅ {rel_display}")
        else:
            skipped += 1

    except Exception as e:
        errors += 1
        print(f"  ❌ ERROR {fpath}: {e}")

print(f"\nDone: {injected} injected | {skipped} skipped | {errors} errors")
