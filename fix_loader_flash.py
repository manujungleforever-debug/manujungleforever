import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_loader = """<script>
  (function(){
    var p = document.getElementById('preloader');
    if(localStorage.getItem('mjf_loader_shown') === '1') {
      if(p) p.style.display = 'none';
    } else {
      localStorage.setItem('mjf_loader_shown', '1');
      window.addEventListener('load', function() {
        setTimeout(function() {
          if (p) {
            p.classList.add('loaded');
            setTimeout(function() { p.style.display = 'none'; }, 700);
          }
        }, 2300); // Wait 2.3s + 0.7s animation = 3s total
      });
    }
  })();
</script>"""

new_loader = """<script>
  (function(){
    var p = document.getElementById('preloader');
    if(localStorage.getItem('mjf_loader_shown') === '1') {
      if(p) p.style.display = 'none';
      if (document.cookie.indexOf("googtrans=/en/es") !== -1) {
        document.documentElement.style.opacity = '0';
        window.addEventListener('load', function() {
           setTimeout(function() {
             document.documentElement.style.transition = 'opacity 0.5s ease';
             document.documentElement.style.opacity = '1';
           }, 600);
        });
      }
    } else {
      localStorage.setItem('mjf_loader_shown', '1');
      window.addEventListener('load', function() {
        setTimeout(function() {
          if (p) {
            p.classList.add('loaded');
            setTimeout(function() { p.style.display = 'none'; }, 700);
          }
        }, 2300);
      });
    }
  })();
</script>"""

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
