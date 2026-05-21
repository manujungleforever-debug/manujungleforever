import os, re, sys

ROOT = 'www.hiddenjunglecusco.com'

NEW_CSS = """/* ── Global Preloader (HJC) ── */
#hjc-preloader {
  position: fixed; inset: 0;
  background: radial-gradient(ellipse at center, #0a1a0f 0%, #030805 100%);
  z-index: 999999;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.6s ease, visibility 0.6s ease;
}
#hjc-preloader.hjc-fade { opacity: 0; visibility: hidden; }
.hjc-wrap {
  position: relative; width: 220px; height: 220px;
  display: flex; align-items: center; justify-content: center;
}
.hjc-logo {
  width: 100px; height: 100px; border-radius: 50%; z-index: 10;
  animation: hjcPulse 3s ease-in-out infinite;
  filter: drop-shadow(0 0 8px rgba(57,255,106,0.15));
}
.hjc-ring {
  position: absolute; top: 50%; left: 50%;
  border-radius: 50%; background: transparent; pointer-events: none;
  border: 1px solid rgba(57,255,106,0.1);
}
.hjc-ring-1 {
  width: 140px; height: 140px;
  border-top-color: rgba(57,255,106,0.8);
  border-bottom-color: rgba(57,255,106,0.8);
  animation: hjcSpin 8s linear infinite;
}
.hjc-ring-2 {
  width: 170px; height: 170px;
  border: 1px dashed rgba(201,168,76,0.4);
  animation: hjcSpin 12s linear infinite reverse;
}
.hjc-ring-3 {
  width: 200px; height: 200px;
  border-left-color: rgba(57,255,106,0.6);
  border-right-color: rgba(57,255,106,0.6);
  animation: hjcSpin 18s linear infinite;
}
@keyframes hjcSpin {
  0%   { transform: translate(-50%,-50%) rotate(0deg); }
  100% { transform: translate(-50%,-50%) rotate(360deg); }
}
@keyframes hjcPulse {
  0%,100% { transform: scale(1);    filter: drop-shadow(0 0 5px rgba(57,255,106,0.15)); }
  50%     { transform: scale(1.03); filter: drop-shadow(0 0 12px rgba(57,255,106,0.3)); }
}
"""

fixed = 0

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if not fname.endswith('.html') or fname == 'original_raw.html': continue
        
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Find the Global Preloader (HJC) block
        if '/* ── Global Preloader (HJC) ── */' in content:
            # We want to replace everything from /* ── Global Preloader (HJC) ── */ 
            # to either /* ── WhatsApp Neon Float ── */ OR </style>
            
            # Using regex to match the block
            new_content = re.sub(
                r'/\* ── Global Preloader \(HJC\) ── \*/[\s\S]*?(?=\n/\* ── WhatsApp Neon Float ── \*/|\n</style>)',
                NEW_CSS.strip(),
                content
            )
            
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed += 1
                print(f"Patched: {os.path.relpath(fpath, ROOT)}")

print(f"\nTotal fixed: {fixed}")
