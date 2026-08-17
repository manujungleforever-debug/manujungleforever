import codecs
import re

# 1. Read contact.html to get HEAD, HEADER, FOOTER
contact_path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\contact\index.html'
with codecs.open(contact_path, 'r', 'utf-8') as f:
    contact_html = f.read()

# Extract from start to <main id="main">
match_top = re.search(r'^(.*?)<main id="main">', contact_html, re.DOTALL | re.IGNORECASE)
top_part = match_top.group(1) if match_top else ''

# Extract footer
match_footer = re.search(r'(<footer class="ft">.*)$', contact_html, re.DOTALL | re.IGNORECASE)
footer_part = match_footer.group(1) if match_footer else ''

# 2. Read current libro.html to get the form blocks
libro_path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\libro-de-reclamaciones\index.html'
with codecs.open(libro_path, 'r', 'utf-8') as f:
    libro_html = f.read()

# Extract from the first contact-info-card to the end of <main>
# We'll just grab the inner content that holds the form
match_cards = re.search(r'(<div class="contact-info-card".*?)</main>', libro_html, re.DOTALL)
cards_content = match_cards.group(1) if match_cards else ''

# Clean up any trailing </section> or extra wrappers from the extraction
cards_content = re.sub(r'</section>\s*$', '', cards_content, flags=re.DOTALL)

# 3. Construct the new HTML
hero_html = '''
<main id="main" class="max-w-3xl mx-auto flex flex-col items-center" style="max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; padding: 0 20px;">
  <section class="relative pt-32 pb-12 flex flex-col items-center justify-center text-center bg-transparent" style="width: 100%; padding-top: 140px; padding-bottom: 40px;">
    <!-- Tag superior verde esmeralda -->
    <span class="text-[#10b981] font-semibold tracking-widest text-xs uppercase mb-2" style="color: #10b981; font-weight: 600; letter-spacing: 0.1em; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 8px;">
      — MANU JUNGLE FOREVER
    </span>

    <!-- Título principal en Blanco Puro -->
    <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight mb-3" style="color: #ffffff; font-weight: 800; font-size: clamp(2.5rem, 6vw, 4rem); letter-spacing: -0.02em; margin-bottom: 12px; font-family: 'Montserrat', sans-serif;">
      Complaints Book
    </h1>

    <!-- Subtítulo en Gris Claro Legible -->
    <p class="text-[#94a3b8] text-sm md:text-base max-w-xl mx-auto px-4 mb-6" style="color: #94a3b8; font-size: 0.875rem; max-width: 600px; margin: 0 auto 24px auto; line-height: 1.5;">
      In accordance with the Consumer Protection Code, Law N° 29571.
    </p>

    <!-- Imagen del libro centrado -->
    <div class="mt-2" style="display: flex; justify-content: center; width: 100%;">
      <img src="../assets/img/libro_reclamaciones.png" alt="Libro de Reclamaciones" class="w-24 md:w-32 mx-auto drop-shadow-md" style="display: block; position: static; max-width: 180px; width: 100%; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));" />
    </div>
  </section>

  <div style="width: 100%; display: flex; flex-direction: column; gap: 24px; padding-bottom: 80px;">
'''

# The final HTML string
final_html = top_part + hero_html + cards_content + '\n  </div>\n</main>\n\n' + footer_part

# Write the final HTML
with codecs.open(libro_path, 'w', 'utf-8') as f:
    f.write(final_html)

print("HTML Reconstruido.")
