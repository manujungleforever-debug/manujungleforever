import os
import re

base_dir = "www.manujungleforever.com"
index_path = os.path.join(base_dir, "index.php")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject the Language Selector next to "Book Now"
lang_selector_html = """
    <div class="lang-selector">
      <div id="google_translate_element" style="display:none;"></div>
      <select id="custom_lang_selector" onchange="changeLanguageByButtonClick(this.value)">
        <option value="en">EN</option>
        <option value="es">ES</option>
      </select>
    </div>
    <a href="contact/index.html" class="nb">Book Now</a>"""

content = content.replace('    <a href="contact/index.html" class="nb">Book Now</a>', lang_selector_html)

# 2. Inject Google Translate JS before </body>
gt_js = """
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en', includedLanguages: 'en,es', layout: google.translate.TranslateElement.InlineLayout.SIMPLE, autoDisplay: false}, 'google_translate_element');
}
function changeLanguageByButtonClick(lang) {
  var selectField = document.querySelector("#google_translate_element select");
  if(selectField) {
    selectField.value = lang;
    selectField.dispatchEvent(new Event('change'));
  }
}
</script>
<script type="text/javascript" src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>"""

content = content.replace("</body>", gt_js)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Injected GTranslate into index.php")
