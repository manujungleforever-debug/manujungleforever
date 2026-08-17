import codecs
import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

# 1. Remove the <style>...</style> block in the <head> completely
html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)

# 2. Locate and replace the entire header div block
old_header_pattern = r'<!-- HEADER CLEAN \(SIN IMAGEN DE SELVA\) -->\s*<div class="in-hero"[^>]*>.*?<\/div>'

new_header = '''<!-- HEADER CLEAN (SIN IMAGEN DE SELVA) -->
<section class="relative pt-32 pb-12 flex flex-col items-center justify-center text-center bg-transparent">
  <!-- Tag superior verde esmeralda -->
  <span class="text-[#10b981] font-semibold tracking-widest text-xs uppercase mb-2">
    — MANU JUNGLE FOREVER
  </span>

  <!-- Título principal en Blanco Puro -->
  <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight mb-3">
    Complaints Book
  </h1>

  <!-- Subtítulo en Gris Claro Legible -->
  <p class="text-[#94a3b8] text-sm md:text-base max-w-xl mx-auto px-4 mb-6">
    In accordance with the Consumer Protection Code, Law N° 29571.
  </p>

  <!-- Imagen del libro centrado -->
  <div class="mt-2">
    <img src="../assets/img/libro_reclamaciones.png" alt="Libro de Reclamaciones" class="w-24 md:w-32 mx-auto drop-shadow-md" />
  </div>
</section>'''

html = re.sub(old_header_pattern, new_header, html, flags=re.DOTALL)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
