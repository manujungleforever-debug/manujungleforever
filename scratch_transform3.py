import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Inject the <style> block in the <head>
style_block = '''
<style>
  body, main, section { background-color: #060b18 !important; background-image: none !important; }
  *::before, *::after { background-image: none !important; }
  .in-hero { padding-top: 140px !important; background: transparent !important; }
  
  /* Inputs dark styling */
  input, select, textarea {
    background: #111827 !important; 
    color: #ffffff !important; 
    border: 1px solid #374151 !important;
  }
</style>
'''
html = html.replace('</head>', style_block + '</head>')

# 2. Add inline styles to main and section
html = html.replace('<main id="main">', '<main id="main" style="background-color: #060b18 !important; background-image: none !important;">')
html = html.replace('<section class="sec" style="background:var(--k)">', '<section class="sec" style="background-color: #060b18 !important; background-image: none !important;">')

# 3. Add inline styles to cards
html = html.replace('background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:24px; padding:40px; margin-bottom: 24px;', 'background-color: #0b111e !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius:24px; padding:40px; margin-bottom: 24px;')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
