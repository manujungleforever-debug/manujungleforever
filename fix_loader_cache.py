import os
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# Regex to match the old preloader script block
preloader_regex = re.compile(r"<script>\s*window\.addEventListener\('load',\s*function\(\)\s*\{[\s\S]*?getElementById\('preloader'\)[\s\S]*?\}\);\s*</script>")

new_preloader_script = """<script>
  window.addEventListener('load', function() {
    var preloader = document.getElementById('preloader');
    if (!preloader) return;
    if (sessionStorage.getItem('loaderShown')) {
      preloader.style.display = 'none';
    } else {
      sessionStorage.setItem('loaderShown', 'true');
      setTimeout(function() {
        preloader.classList.add('loaded');
        setTimeout(function() { preloader.style.display = 'none'; }, 700);
      }, 3000);
    }
  });
</script>"""

# Also update changeLanguageByButtonClick if present to reset loader
lang_btn_regex = re.compile(r"function\s+changeLanguageByButtonClick\(lang\)\s*\{([\s\S]*?dispatchEvent\(new Event\('change'\)\);)\s*\}")

new_lang_btn = """function changeLanguageByButtonClick(lang) {
  var selectField = document.querySelector("#google_translate_element select");
  if(selectField) {
    selectField.value = lang;
    selectField.dispatchEvent(new Event('change'));
    
    var preloader = document.getElementById('preloader');
    if (preloader) {
      preloader.style.display = 'flex';
      preloader.classList.remove('loaded');
      setTimeout(function() {
        preloader.classList.add('loaded');
        setTimeout(function() { preloader.style.display = 'none'; }, 700);
      }, 1500); // Shorter delay when changing language
    }
  }
}"""

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.php'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            content = preloader_regex.sub(new_preloader_script, content)
            
            if 'changeLanguageByButtonClick' in content:
                content = lang_btn_regex.sub(new_lang_btn, content)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated: {filepath}")

print("Done updating preloader cache logic.")
