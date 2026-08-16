import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

style_update = '''
<style>
  body, main, section { background-color: #060b18 !important; background-image: none !important; }
  *::before, *::after { background-image: none !important; }
  
  /* UNIFICACIÓN DEL HEADER / NAVBAR */
  header, #N, .site-header, .hdr { 
    background: transparent !important; 
    background-color: #060b18 !important; 
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  }
  header::before, header::after, #N::before, #N::after { 
    display: none !important; 
    background: none !important; 
  }
  
  /* REESTRUCTURACIÓN DEL HERO */
  .in-hero { padding-top: 180px !important; background: transparent !important; }
  .title-container {
    padding: 180px 0 60px 0 !important;
    text-align: center;
    position: relative;
    z-index: 10;
  }
  
  /* Inputs dark styling */
  input, select, textarea {
    background: #111827 !important; 
    color: #ffffff !important; 
    border: 1px solid #374151 !important;
  }
</style>
'''

# Replace the old style block
html = re.sub(r'<style>.*?</style>', style_update, html, flags=re.DOTALL)

# Fix the title container just in case it didn't have the class
html = html.replace('<div style="text-align:center; padding: 140px 0 60px 0;">', '<div class="title-container">')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
