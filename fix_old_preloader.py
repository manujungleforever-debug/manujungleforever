"""
fix_old_preloader.py
Para los archivos que aun tienen el preloader VIEJO (hjc_preloaded):
1. Elimina el bloque CSS viejo del preloader
2. Elimina el HTML+JS viejo del preloader
3. Inyecta el CSS y HTML nuevos
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'www.hiddenjunglecusco.com'

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

def make_preloader_html(rel):
    return """<!-- HJC Preloader -->
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
""".replace('{rel}', rel)

def rel_prefix(filepath):
    rel = os.path.relpath(filepath, ROOT)
    depth = len(rel.split(os.sep)) - 1
    return '../' * depth if depth > 0 else ''

fixed = 0

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if fname != 'index.html':
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        if 'hjc_preloaded' not in content:
            continue  # already new, skip

        rel = rel_prefix(fpath)
        original = content

        # Step 1: Remove OLD preloader CSS block entirely
        content = re.sub(
            r'/\* ── Global Preloader ── \*/[\s\S]*?(?=\n</style>)',
            '',
            content,
            flags=re.DOTALL
        )
        # Also remove old WhatsApp Neon Pulse CSS if present and new one not there
        if '/* ── WhatsApp Neon Pulse ── */' in content and '/* ── WhatsApp Neon Float ── */' not in content:
            content = re.sub(
                r'/\* ── WhatsApp Neon Pulse ── \*/[\s\S]*?(?=\n</style>)',
                '',
                content,
                flags=re.DOTALL
            )

        # Step 2: Remove the OLD preloader HTML+JS block completely
        # Pattern: <!-- GLOBAL PRELOADER --> (optional) + <div id="hjc-preloader">...</div> + <script>...hjc_preloaded...</script>
        content = re.sub(
            r'(?:<!-- GLOBAL PRELOADER -->\s*)?\n?<div id="hjc-preloader">[\s\S]*?</script>\s*\n?',
            '',
            content,
            flags=re.DOTALL
        )

        # Step 3: Inject NEW CSS before first </style> in <head>
        if '/* ── Global Preloader (HJC) ── */' not in content:
            head_end = content.find('</head>')
            style_end = content.rfind('</style>', 0, head_end) if head_end > 0 else -1
            if style_end > 0:
                content = content[:style_end] + PRELOADER_CSS + '\n' + content[style_end:]
            elif head_end > 0:
                content = content[:head_end] + '<style>' + PRELOADER_CSS + '</style>\n' + content[head_end:]

        # Step 4: Inject NEW preloader HTML right after <body...>
        if 'hjc_loaded' not in content:
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + make_preloader_html(rel) + content[insert_pos:]

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            rel_display = os.path.relpath(fpath, ROOT)
            print(f"  FIXED: {rel_display}")
            fixed += 1

print(f"\nTotal fixed: {fixed}")
