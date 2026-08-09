import os, glob, re

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'
files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

script_pattern = re.compile(r'(<div id="preloader">.*?</div>\s*)<script>.*?window\.addEventListener\(\'load\'.*?</script>', re.DOTALL)

replacement = r'''\1<script>
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
</script>'''

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, count = script_pattern.subn(replacement, content)
        if count > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {os.path.relpath(fpath, base)}')
    except Exception as e:
        pass
