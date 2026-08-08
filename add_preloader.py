import os
import re

base_dir = "www.manujungleforever.com"

# The preloader HTML/JS with correct timing logic
preloader_html = """
<div id="preloader">
  <img src="assets/img/logo.png" alt="Loading Manu Jungle Forever">
</div>
<script>
  var _preloaderStart = Date.now();
  window.addEventListener('load', function() {
    var elapsed = Date.now() - _preloaderStart;
    var minDuration = 3000; 
    var delay = Math.max(500, minDuration - elapsed);
    setTimeout(function() {
      var preloader = document.getElementById('preloader');
      if (preloader) {
        preloader.classList.add('loaded');
        setTimeout(function() { preloader.style.display = 'none'; }, 700);
      }
    }, delay);
  });
</script>
"""

for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if 'id="preloader"' not in content:
            content = content.replace(
                '<a class="skip" href="#main">Skip to content</a>', 
                '<a class="skip" href="#main">Skip to content</a>\n' + preloader_html
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
