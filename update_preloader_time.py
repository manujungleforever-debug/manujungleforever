import os
import re

base_dir = "www.manujungleforever.com"

# The new advanced preloader logic
new_js = """<script>
  var _preloaderStart = Date.now();
  window.addEventListener('load', function() {
    var elapsed = Date.now() - _preloaderStart;
    var minDuration = 3000; // Force it to show for at least 3 seconds
    var delay = Math.max(500, minDuration - elapsed); // Always wait at least 500ms after load
    setTimeout(function() {
      var preloader = document.getElementById('preloader');
      if (preloader) {
        preloader.classList.add('loaded');
        setTimeout(function() { preloader.style.display = 'none'; }, 700);
      }
    }, delay);
  });
</script>"""

old_js_regex = r"<script>\s*window\.addEventListener\('load', function\(\) \{\s*setTimeout\([^>]+>.*?<\/script>"

for file_name in ["index.php", "index.html"]:
    file_path = os.path.join(base_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace old preloader JS with new one
        if "window.addEventListener('load'" in content and "setTimeout" in content:
            content = re.sub(old_js_regex, new_js, content, flags=re.DOTALL)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

# Update rebuild_tours.py as well
rebuild_script = "rebuild_tours.py"
if os.path.exists(rebuild_script):
    # Just running rebuild_tours will copy the new JS from index.php!
    # Let's verify if rebuild_tours copies JS. It extracts from top to <main id="main"> or <section class="hero">.
    # The preloader script is right after <a class="skip"...>, which is before <header>, so it IS extracted!
    pass
