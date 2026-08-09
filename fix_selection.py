import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_loader = """      if (document.cookie.indexOf("googtrans=/en/es") !== -1) {
        document.documentElement.style.opacity = '0';
        window.addEventListener('load', function() {
           setTimeout(function() {
             document.documentElement.style.transition = 'opacity 0.5s ease';
             document.documentElement.style.opacity = '1';
           }, 600);
        });
      }"""

new_loader = """      if (document.cookie.indexOf("googtrans=/en/es") !== -1) {
        document.documentElement.style.opacity = '0';
        window.addEventListener('load', function() {
           setTimeout(function() {
             if (window.getSelection) { window.getSelection().removeAllRanges(); }
             document.documentElement.style.transition = 'opacity 0.5s ease';
             document.documentElement.style.opacity = '1';
             setTimeout(function() { if (window.getSelection) { window.getSelection().removeAllRanges(); } }, 500);
           }, 600);
        });
      }"""

for fpath in files:
    if fpath.endswith('admin\\index.html') or 'admin/index.html' in fpath.replace('\\','/'):
        continue
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace(old_loader, new_loader)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Updated {fpath}")
    except Exception as e:
        print(f"Error {fpath}: {e}")
