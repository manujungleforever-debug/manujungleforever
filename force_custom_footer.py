import os
import glob
import re

base_dir = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

perfect_footer_base = """<footer class="ft">
<style>
  @media (max-width: 991px) {
    .ft .fg { grid-template-columns: 1fr; gap: 30px; }
  }
  .libro-box:hover { border-color: rgba(255,255,255,0.3) !important; transform: translateY(-3px); }
  .fa { font-family: 'Syne', sans-serif; font-size: 0.85rem; line-height: 1.6; color: rgba(255,255,255,0.7); text-transform: uppercase; margin-bottom: 25px; margin-top: 15px; display: block; }
  .fc p { margin-bottom: 10px; display: flex; align-items: flex-start; gap: 10px; font-size: 0.85rem; color: rgba(255,255,255,0.6); }
  .fc a { color: rgba(255,255,255,0.6); text-decoration: none; transition: color 0.3s ease; }
  .fc a:hover { color: var(--a); }
  .fc i { color: var(--a); width: 16px; text-align: center; margin-top: 3px; }
  .f-col h3 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5); margin-bottom: 20px; font-weight: 800; }
  .f-col ul { list-style: none; padding: 0; margin: 0; }
  .f-col li { margin-bottom: 12px; }
  .f-col a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.85rem; display: flex; align-items: center; gap: 8px; transition: color 0.3s ease; }
  .f-col a i { color: var(--a); font-size: 0.7rem; transition: transform 0.3s ease; }
  .f-col a:hover { color: var(--a); }
  .f-col a:hover i { transform: translateX(3px); }
</style>
<div class="cx">
  <div class="fg" style="display: grid; grid-template-columns: 1.8fr 1fr 1.2fr 1.5fr; gap: 40px; align-items: start;">
    
    <!-- COLUMN 1: Logo & Contact -->
    <div>
      <a href="index.html"><img src="assets/img/logo.png" alt="Manu Jungle Forever" class="fl" loading="lazy" style="max-width: 250px;"></a>
      <span class="fa">GUIDED JUNGLE TOURS FROM CUSCO TO THE MANU NATIONAL PARK &amp; THE PERUVIAN AMAZON. LOCAL, WILD, AND AUTHENTIC.</span>
      <address class="fc">
        <p><i class="fas fa-map-marker-alt"></i><a href="https://goo.gl/maps/B8NjhLZizA6YKwKD6" target="_blank" rel="noopener">Nuevo Eden, Manu National Park, Peru</a></p>
        <p><i class="fas fa-phone"></i><a href="tel:+51901525679">+51 901 525 679</a></p>
        <p><i class="fas fa-envelope"></i><a href="mailto:discover@manujungleforever.com">discover@manujungleforever.com</a></p>
      </address>
      <div class="so" style="margin-top: 25px;">
        <a href="https://www.facebook.com/manujungleforever" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/manujungleforever/?hl=en" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="custom-tripadvisor-icon"></i></a>
        <a href="https://abnb.me/Ri8XQWoA19" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fab fa-airbnb"></i></a>
        <a href="https://wa.me/51901525679" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.tiktok.com/@hidden.jungle.cus" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
      </div>
    </div>

    <!-- COLUMN 2: Explore -->
    <div class="f-col">
      <h3>Explore</h3>
      <ul style="margin-bottom: 30px;">
        <li><a href="index.html"><i class="fas fa-arrow-right"></i> Home</a></li>
        <li><a href="about-2/index.html"><i class="fas fa-arrow-right"></i> About Us</a></li>
        <li><a href="departures/index.html"><i class="fas fa-arrow-right"></i> Departures</a></li>
        <li><a href="news-and-gallery/index.html"><i class="fas fa-arrow-right"></i> Gallery</a></li>
        <li><a href="blog/index.html"><i class="fas fa-arrow-right"></i> Blog</a></li>
        <li><a href="guided-tours/index.html"><i class="fas fa-arrow-right"></i> Guided Jungle Tours</a></li>
        <li><a href="contact/index.html"><i class="fas fa-arrow-right"></i> Contact</a></li>
      </ul>

      <!-- Libro de reclamaciones -->
      <a href="libro-de-reclamaciones/index.html" style="text-decoration:none; display:block; max-width: 250px;">
        <div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px 12px; text-align:center; transition:0.3s; box-sizing:border-box;">
          <div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
            <div style="color:#002e24; font-weight:800; font-size:0.8rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Complaints<br>Book</div>
            <img src="assets/img/libro_reclamaciones.png" alt="Complaints Book" style="max-width:40px; margin-top:8px;">
          </div>
          <div style="color:rgba(255,255,255,0.6); font-size:0.7rem; line-height:1.4;">In accordance with the Consumer Protection and Defense Code, we have a Virtual Complaints Book.</div>
        </div>
      </a>
    </div>

    <!-- COLUMN 3: Wildlife Tours -->
    <div class="f-col">
      <h3>Wildlife Tours</h3>
      <ul>
        <li><a href="3-day-wildlife-quest-machu-wasi/index.html"><i class="fas fa-arrow-right"></i> 3-Day Wildlife Tour</a></li>
        <li><a href="4-day-wildlife-quest-machu-wasi/index.html"><i class="fas fa-arrow-right"></i> 4-Day Wildlife &ndash; Machu Wasi</a></li>
        <li><a href="4-day-wildlife-quest-nuevo-eden/index.html"><i class="fas fa-arrow-right"></i> 4-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="5-day-wildlife-quest-nuevo-eden/index.html"><i class="fas fa-arrow-right"></i> 5-Day Wildlife &ndash; Nuevo Eden</a></li>
        <li><a href="6-day-wildlife-quest-blanquillo/index.html"><i class="fas fa-arrow-right"></i> 6-Day Wildlife &ndash; Blanquillo</a></li>
        <li><a href="6-day-wildlife-quest-reserved-zone/index.html"><i class="fas fa-arrow-right"></i> Manu Reserved Zone &ndash; 6 Days</a></li>
        <li><a href="8-day-wildlife-photography-tour/index.html"><i class="fas fa-arrow-right"></i> Wildlife Photography &ndash; 8 Days</a></li>
      </ul>
    </div>

    <!-- COLUMN 4: Expeditions -->
    <div class="f-col">
      <h3>Expeditions</h3>
      <ul>
        <li><a href="5-day-amazon-expedition/index.html"><i class="fas fa-arrow-right"></i> 5-Day Amazon Expedition</a></li>
        <li><a href="6-day-amazon-expedition/index.html"><i class="fas fa-arrow-right"></i> 6-Day Amazon Expedition</a></li>
        <li><a href="2-day-rainforest-road-trip/index.html"><i class="fas fa-arrow-right"></i> 2-Day Road Trip</a></li>
        <li><a href="5-day-rainforest-road-trip/index.html"><i class="fas fa-arrow-right"></i> 5-Day Road Trip</a></li>
        <li><a href="rainforest-road-trip-from-cusco/index.html"><i class="fas fa-arrow-right"></i> Rainforest Road Trip</a></li>
      </ul>
    </div>

  </div>
</div>
</footer>"""

html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

def get_adapted_footer(depth):
    if depth == 0:
        return perfect_footer_base
    else:
        prefix = "../" * depth
        adapted = perfect_footer_base.replace('src="assets', f'src="{prefix}assets')
        adapted = adapted.replace('href="index.html', f'href="{prefix}index.html')
        adapted = adapted.replace('href="about-2', f'href="{prefix}about-2')
        adapted = adapted.replace('href="departures', f'href="{prefix}departures')
        adapted = adapted.replace('href="news-and-gallery', f'href="{prefix}news-and-gallery')
        adapted = adapted.replace('href="blog', f'href="{prefix}blog')
        adapted = adapted.replace('href="guided-tours', f'href="{prefix}guided-tours')
        adapted = adapted.replace('href="contact', f'href="{prefix}contact')
        adapted = adapted.replace('href="libro-de-reclamaciones', f'href="{prefix}libro-de-reclamaciones')
        
        # Wildlife
        adapted = adapted.replace('href="3-day-', f'href="{prefix}3-day-')
        adapted = adapted.replace('href="4-day-', f'href="{prefix}4-day-')
        adapted = adapted.replace('href="5-day-', f'href="{prefix}5-day-')
        adapted = adapted.replace('href="6-day-', f'href="{prefix}6-day-')
        adapted = adapted.replace('href="8-day-', f'href="{prefix}8-day-')
        
        # Expeditions
        adapted = adapted.replace('href="2-day-', f'href="{prefix}2-day-')
        adapted = adapted.replace('href="rainforest-road-trip', f'href="{prefix}rainforest-road-trip')
        
        return adapted

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, base_dir)
    depth = rel_path.count(os.sep)
    
    current_footer = get_adapted_footer(depth)
    
    if '<footer class="ft">' in content:
        new_content = re.sub(r'<footer class="ft">.*?</footer>', current_footer, content, flags=re.DOTALL)
    elif '</footer>' in content:
        new_content = re.sub(r'</main>.*?</footer>', f'</main>\n{current_footer}', content, flags=re.DOTALL)
    else:
        new_content = content.replace('</body>', f'{current_footer}\n</body>')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Force restored custom 4-column footer in {count} HTML files.")
