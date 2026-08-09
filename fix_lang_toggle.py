import os, glob

base = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com'

files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True) + glob.glob(os.path.join(base, '**', '*.php'), recursive=True)

old_block = """    <div class="ls-custom" tabindex="0">
      <div class="ls-current"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</div>
      <ul class="ls-options">
        <li onclick="doTranslate('en')"><span class="flg">&#x1F1FA;&#x1F1F8;</span> EN</li>
        <li onclick="doTranslate('es')"><span class="flg">&#x1F1EA;&#x1F1F8;</span> ES</li>
      </ul>
    </div>"""

new_block = """    <button class="lang-toggle" onclick="document.cookie.indexOf('googtrans=/en/es')!==-1 ? doTranslate('en') : doTranslate('es')" translate="no">
      <script>
        if(document.cookie.indexOf('googtrans=/en/es')!==-1) {
          document.write('<span class="flg">&#x1F1FA;&#x1F1F8;</span> EN');
        } else {
          document.write('<span class="flg">&#x1F1EA;&#x1F1F8;</span> ES');
        }
      </script>
    </button>"""

for fpath in files:
    if fpath.endswith('admin\\index.html') or 'admin/index.html' in fpath.replace('\\','/'):
        continue
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace(old_block, new_block)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Updated {fpath}")
    except Exception as e:
        pass
