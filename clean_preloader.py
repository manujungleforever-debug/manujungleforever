"""
clean_preloader.py
Detecta páginas con preloader duplicado (viejo + nuevo) y elimina el viejo.
El viejo: usa hjc_preloaded | tiene hjcSpin (con mayúscula) | tiene hjc-spin-ring
El nuevo: usa hjc_loaded    | tiene hjcSpin en @keyframes  | tiene hjc-ring-1
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'www.hiddenjunglecusco.com'

# Patrón del bloque CSS viejo (entre /* ── Global Preloader ── */ y el </style> siguiente)
OLD_CSS_PATTERN = re.compile(
    r'/\* ── Global Preloader ── \*/.*?(?=\n</style>|\Z)',
    re.DOTALL
)

# Patrón del bloque HTML viejo del preloader
# <div id="hjc-preloader">...</div>\n<script>...hjc_preloaded...</script>
OLD_HTML_PATTERN = re.compile(
    r'<!-- GLOBAL PRELOADER -->\s*<div id="hjc-preloader">.*?</script>',
    re.DOTALL
)

# También el bloque sin comentario pero con hjc_preloaded
OLD_HTML_PATTERN2 = re.compile(
    r'<div id="hjc-preloader">[\s\S]*?hjc_preloaded[\s\S]*?</script>',
    re.DOTALL
)

# CSS viejo de WhatsApp (wa-wrap duplicado con clases distintas)
OLD_WA_CSS_PATTERN = re.compile(
    r'/\* ── WhatsApp Neon Pulse ── \*/.*?(?=\n</style>|\Z)',
    re.DOTALL
)

fixed = 0
clean = 0

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ("https_", "'https_", 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if not fname.endswith('.html') or fname == 'original_raw.html':
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Check if page has both old and new preloader markers
        has_old_css  = '/* ── Global Preloader ── */' in content
        has_new_css  = '/* ── Global Preloader (HJC) ── */' in content
        has_old_html = 'hjc_preloaded' in content
        has_new_html = 'hjc_loaded' in content
        has_old_wa   = '/* ── WhatsApp Neon Pulse ── */' in content
        has_new_wa   = '/* ── WhatsApp Neon Float ── */' in content

        if not (has_old_css or has_old_html or has_old_wa):
            clean += 1
            continue

        original = content

        # Remove old preloader CSS block
        if has_old_css and has_new_css:
            content = re.sub(
                r'/\* ── Global Preloader ── \*/.*?(?=\n</style>)',
                '',
                content,
                flags=re.DOTALL
            )

        # Remove old WhatsApp CSS block
        if has_old_wa and has_new_wa:
            content = re.sub(
                r'/\* ── WhatsApp Neon Pulse ── \*/.*?(?=\n</style>)',
                '',
                content,
                flags=re.DOTALL
            )

        # Remove old preloader HTML+script block (hjc_preloaded version)
        if has_old_html and has_new_html:
            # Remove <!-- GLOBAL PRELOADER --> comment + old div block
            content = re.sub(
                r'<!-- GLOBAL PRELOADER -->\s*\n?<div id="hjc-preloader">[\s\S]*?</script>',
                '',
                content,
                flags=re.DOTALL
            )
            # In case no comment, match directly
            if 'hjc_preloaded' in content:
                content = re.sub(
                    r'<div id="hjc-preloader">[\s\S]*?hjc_preloaded[\s\S]*?</script>',
                    '',
                    content,
                    flags=re.DOTALL
                )

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            rel = os.path.relpath(fpath, ROOT)
            print(f"  FIXED: {rel}")
            fixed += 1
        else:
            clean += 1

print(f"\nFixed: {fixed} | Already clean: {clean}")
