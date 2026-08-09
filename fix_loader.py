import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_loader = """<script>
  (function(){
    var p = document.getElementById('preloader');
    // Mostrar solo una vez por sesion, o si hay un parametro "lang=" en la URL
    if(sessionStorage.getItem('mjf_loader_shown') === '1' && !window.location.search.includes('lang=')) {
      if(p) p.style.display = 'none';
    } else {
      sessionStorage.setItem('mjf_loader_shown', '1');
      window.addEventListener('load', function() {
        setTimeout(function() {
          if (p) {
            p.classList.add('loaded');
            setTimeout(function() { p.style.display = 'none'; }, 700);
          }
        }, 800); // Pequeña espera para que se vea la animacion
      });
    }
  })();
</script>"""

new_loader = """<script>
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

old_translate = """function doTranslate(lang) {
  document.cookie = "googtrans=/en/" + lang + "; path=/;";
  window.location.reload();
}"""

new_translate = """function doTranslate(lang) {
  localStorage.removeItem('mjf_loader_shown');
  document.cookie = "googtrans=/en/" + lang + "; path=/;";
  window.location.reload();
}"""


for fpath in files:
    if fpath.endswith('admin\\index.html') or 'admin/index.html' in fpath.replace('\\','/'):
        continue
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace(old_loader, new_loader)
        new_content = new_content.replace(old_translate, new_translate)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Updated {fpath}")
    except Exception as e:
        print(f"Error {fpath}: {e}")
