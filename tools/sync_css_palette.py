#!/usr/bin/env python3
"""
sync_css_palette.py
Replica los cambios de paleta marrón/selvática a todas las páginas públicas.
Uso: python tools/sync_css_palette.py  (desde raíz del proyecto)
"""

import os
import re
import glob

# ──────────────────────────────────────────────
ROOT = os.path.join(os.path.dirname(__file__), '..', 'www.manujungleforever.com')

SKIP_DIRS = {'admin', 'data'}
SKIP_FILES = {
    'panel.html', 'gestionar-tours.html', 'gestionar-salidas.html',
    'gestionar-testimonios.html', 'gestionar-reclamos.html',
    'gestionar-medios.html', 'gestionar-usuarios.html', 'gestionar-contenido.html'
}

# Reemplazos de color: azul noche → marrón cálido
COLOR_MAP = [
    (r'rgba\(15,\s*23,\s*42,', 'rgba(22,15,9,'),
    (r'rgba\(8,\s*56,\s*51,',  'rgba(14,35,30,'),
    (r'rgba\(5,\s*13,\s*8,',   'rgba(10,7,4,'),
    (r'rgba\(3,\s*12,\s*10,',  'rgba(8,5,3,'),
    (r'rgba\(3,\s*8,\s*6,',    'rgba(8,5,3,'),
    (r'#070B14',               '#0c0805'),
    (r'#0b1329',               '#160f09'),
    (r'#101d3f',               '#22170f'),
]

NAV_OLD = r'background:linear-gradient\(90deg,\s*rgba\(15,23,42,([0-9.]+)\)\s*0%,\s*rgba\(8,56,51,([0-9.]+)\)\s*100%\)'
def NAV_NEW(m): return f'background:linear-gradient(90deg,rgba(22,15,9,{m.group(1)}) 0%,rgba(14,35,30,{m.group(2)}) 100%)'

def should_skip(path):
    parts = os.path.normpath(path).split(os.sep)
    for part in parts:
        if part in SKIP_DIRS:
            return True
    return os.path.basename(path) in SKIP_FILES

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    content = original
    for old, new in COLOR_MAP:
        content = re.sub(old, new, content, flags=re.IGNORECASE)
    content = re.sub(NAV_OLD, NAV_NEW, content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    pattern = os.path.join(ROOT, '**', '*.html')
    files = glob.glob(pattern, recursive=True)
    modified, skipped, unchanged = [], [], []
    for filepath in sorted(files):
        rel = os.path.relpath(filepath, ROOT)
        if should_skip(filepath):
            skipped.append(rel)
            continue
        if process_file(filepath):
            modified.append(rel)
        else:
            unchanged.append(rel)
    print(f"\n  Modificados : {len(modified)}")
    print(f"  Sin cambios : {len(unchanged)}")
    print(f"  Omitidos    : {len(skipped)}\n")
    for f in modified:
        print(f"  >> {f}")

if __name__ == '__main__':
    main()
