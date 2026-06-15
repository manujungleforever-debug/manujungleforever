import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'www.hiddenjunglecusco.com'

def get_new_footer(rel):
    return f"""<footer class="ft">
<style>
  @media (min-width: 992px) {{
    .fg {{ grid-template-columns: 1.8fr 0.9fr 1.1fr 0.8fr 1.6fr !important; gap: 40px !important; align-items: start !important; }}
  }}
  .libro-box:hover {{ border-color: #39ff6a !important; transform: translateY(-3px); }}
</style>
<div class="cx">
  <div class="fg">
    <div>
      <a href="{rel}index.html"><img src="{rel}wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png" alt="Hidden Jungle Cusco" class="fl" loading="lazy" style="max-width: 150px; margin-bottom: 20px;"></a>
      <p class="fa">Guided jungle tours from Cusco to the Manu National Park &amp; the Peruvian Amazon. Local. Wild. Authentic.</p>
      <address class="fc">
        <p><i class="fas fa-map-marker-alt"></i><a href="https://goo.gl/maps/B8NjhLZizA6YKwKD6" target="_blank" rel="noopener">Hidden Jungle Cusco – La Casa Escondida 17800, Nuevo Eden, Peru</a></p>
        <p><i class="fas fa-phone"></i><a href="tel:+51979808013">+51 979 808 013</a> / <a href="tel:+51923289231">+51 923 289 231</a></p>
        <p><i class="fas fa-envelope"></i><a href="mailto:discover@hiddenjunglecusco.com">discover@hiddenjunglecusco.com</a></p>
      </address>
      <div class="so">
        <a href="https://www.facebook.com/hiddenjunglecusco" class="sc" target="_blank" rel="noopener" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="https://www.instagram.com/hiddenjunglecusco/?hl=en" class="sc" target="_blank" rel="noopener" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.tripadvisor.com/Attraction_Review-g294314-d17476586-Reviews-Hidden_Jungle_Cusco-Cusco_Cusco_Region.html?m=19905" class="sc" target="_blank" rel="noopener" aria-label="TripAdvisor"><i class="fab fa-tripadvisor"></i></a>
        <a href="https://abnb.me/Ri8XQWoA19" class="sc" target="_blank" rel="noopener" aria-label="Airbnb"><i class="fab fa-airbnb"></i></a>
        <a href="https://wa.me/51923289231" class="sc" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.tiktok.com/@hidden.jungle.cus" class="sc" target="_blank" rel="noopener" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
      </div>
    </div>
    
    <div>
      <p class="fh">Support &amp; Legal</p>
      <ul class="fli">
        <li><a href="{rel}contact/index.html">Contact Us</a></li>
        <li><a href="{rel}faq/index.html">FAQs</a></li>
        <li><a href="{rel}terms-and-conditions/index.html">Terms &amp; Conditions</a></li>
        <li><a href="{rel}privacy-policy/index.html">Privacy Policy</a></li>
        <li><a href="{rel}cookies-policy/index.html">Cookie Policy</a></li>
      </ul>
    </div>

    <div>
      <a href="{rel}libro-de-reclamaciones/index.html" style="text-decoration:none; display:block;">
        <div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(201,168,76,0.3); border-radius:12px; padding:16px 12px; text-align:center; transition:0.3s; box-sizing:border-box;">
          <div style="background:#fff; border-radius:8px; padding:12px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:12px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
            <div style="color:#0a1a0f; font-weight:800; font-size:0.8rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Complaints<br>Book</div>
            <i class="fas fa-book-open" style="color:#c9a84c; font-size:1.5rem; margin-top:8px;"></i>
          </div>
          <p style="font-size:0.65rem; color:rgba(255,255,255,0.6); line-height:1.4; margin:0;">In accordance with the Consumer Protection Code, we have a Virtual Complaints Book available.</p>
        </div>
      </a>
    </div>
    
    <div>
      <p class="fh">Explore</p>
      <ul class="fli">
        <li><a href="{rel}index.html">Home</a></li>
        <li><a href="{rel}about-2/index.html">About Us</a></li>
        <li><a href="{rel}guided-tours/index.html">Guided Jungle Tours</a></li>
        <li><a href="{rel}departures/index.html">Departures</a></li>
        <li><a href="{rel}news-and-gallery/index.html">Gallery</a></li>
        <li><a href="{rel}blog/index.html">Blog</a></li>
      </ul>
    </div>
    
    <div>
      <p class="fh">Tours</p>
      <ul class="fli">
        <li><a href="{rel}wildlife-tours-from-cusco/index.html">Wildlife Tours From Cusco</a></li>
        <li><a href="{rel}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{rel}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{rel}8-day-wildlife-photography-tour/index.html">Wildlife Photography – 8 Days</a></li>
        <li><a href="{rel}rainforest-road-trip-from-cusco/index.html">Rainforest Road Trip</a></li>
        <li><a href="{rel}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
        <li><a href="{rel}6-day-amazon-expedition/index.html">6-Day Amazon Expedition</a></li>
      </ul>
    </div>
  </div>
  <div class="fb"><div class="fbi"><span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span><span>Site design: Meyer Consulting and Management</span></div></div>
</div></footer>"""

updated_footer = 0
updated_nav = 0

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('https_', 'wp-includes', 'wp-admin', 'hts-cache')]
    for fname in files:
        if not fname.endswith('.html') or fname == 'original_raw.html': continue
        
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            c = f.read()
            
        rel = '../' * (len(os.path.relpath(fpath, ROOT).split(os.sep)) - 1)
        if rel == '': rel = './'
        if rel == './' and dirpath == ROOT: rel = ''
        
        folder_name = os.path.basename(dirpath)
        if dirpath == ROOT: folder_name = 'home'
        
        changed = False

        # 1. Update Footer
        new_footer = get_new_footer(rel)
        new_c = re.sub(r'<footer class="ft">.*?</footer>', new_footer, c, flags=re.DOTALL)
        if new_c != c:
            changed = True
            c = new_c
            updated_footer += 1

        # 2. Update Nav Active State
        nav_match = re.search(r'<nav class="nm"[^>]*>.*?</nav>', c, re.DOTALL)
        if nav_match:
            nav_html = nav_match.group(0)
            orig_nav_html = nav_html

            # Step 1: Remove 'on' from every class attribute cleanly
            def strip_on_from_class(m):
                classes = m.group(1).split()
                classes = [cl for cl in classes if cl != 'on']
                val = ' '.join(classes)
                if val:
                    return f'class="{val}"'
                else:
                    return ''
            nav_html = re.sub(r'class="([^"]*)"', strip_on_from_class, nav_html)

            # Map folder names to href targets
            active_map = {
                'home': 'index.html',
                'www.hiddenjunglecusco.com': 'index.html',
                'about-2': 'about-2/index.html',
                'guided-tours': 'guided-tours/index.html',
                'departures': 'departures/index.html',
                'news-and-gallery': 'news-and-gallery/index.html',
                'blog': 'blog/index.html',
                'contact': 'contact/index.html'
            }

            def add_on(tag):
                if 'class="' in tag:
                    return re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} on"', tag)
                return tag.replace('<a ', '<a class="on" ')

            # Check if this folder has a direct nav item
            if folder_name in active_map:
                target_href = active_map[folder_name]
                pattern = rf'<a\s[^>]*href="(?:(?:\.\.\/)+|(?:\.\/)?){re.escape(target_href)}"[^>]*>'
                nav_html = re.sub(pattern, lambda m: add_on(m.group(0)), nav_html)

            # Tour pages → highlight "Guided Tours"
            elif any(k in folder_name for k in ('tour', 'day', 'expedition', 'road-trip', 'wildlife', 'amazon', 'rainforest', 'photography', 'machu-wasi', 'nuevo-eden', 'blanquillo', 'reserved-zone')):
                pattern = rf'<a\s[^>]*href="(?:(?:\.\.\/)+|(?:\.\/)?){re.escape("guided-tours/index.html")}"[^>]*>'
                nav_html = re.sub(pattern, lambda m: add_on(m.group(0)), nav_html)

            if nav_html != orig_nav_html:
                c = c.replace(orig_nav_html, nav_html)
                changed = True
                updated_nav += 1

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)

print(f"Updated footer in {updated_footer} files.")
print(f"Fixed active navigation state in {updated_nav} files.")
