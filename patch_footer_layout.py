import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'www.hiddenjunglecusco.com'

def get_new_footer(rel):
    return f"""<footer class="ft">
<style>
  @media (min-width: 992px) {{
    .fg {{ grid-template-columns: 2fr 1fr 1.3fr 1fr 1.2fr !important; gap: 24px !important; }}
  }}
  .libro-box:hover {{ border-color: #39ff6a !important; transform: translateY(-3px); }}
</style>
<div class="cx">
  <div class="fg">
    <div>
      <a href="{rel}index.html"><img src="{rel}wp-content/uploads/2018/01/HiddenJungleCusco_Logo_TextSeal_3Color.png" alt="Hidden Jungle Cusco" class="fl" loading="lazy"></a>
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
        <li><a href="{rel}3-day-wildlife-quest-machu-wasi/index.html">3-Day Wildlife - Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-machu-wasi/index.html">4-Day Wildlife – Machu Wasi</a></li>
        <li><a href="{rel}4-day-wildlife-quest-nuevo-eden/index.html">4-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel}5-day-wildlife-quest-nuevo-eden/index.html">5-Day Wildlife – Nuevo Eden</a></li>
        <li><a href="{rel}6-day-wildlife-quest-blanquillo/index.html">6-Day Wildlife – Blanquillo</a></li>
        <li><a href="{rel}6-day-wildlife-quest-reserved-zone/index.html">Manu Reserved Zone – 6 Days</a></li>
        <li><a href="{rel}5-day-amazon-expedition/index.html">5-Day Amazon Expedition</a></li>
      </ul>
    </div>

    <div>
      <a href="{rel}libro-de-reclamaciones/index.html" style="text-decoration:none; display:block; height:100%;">
        <div class="libro-box" style="background:rgba(255,255,255,0.02); border:1px solid rgba(201,168,76,0.3); border-radius:12px; padding:24px 20px; text-align:center; transition:0.3s; height:100%; box-sizing:border-box;">
          <div style="background:#fff; border-radius:8px; padding:16px; display:inline-flex; flex-direction:column; align-items:center; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
            <div style="color:#0a1a0f; font-weight:800; font-size:1rem; line-height:1.2; font-family:Arial,sans-serif; text-align:center; text-transform:uppercase; letter-spacing:0.5px;">Complaints<br>Book</div>
            <i class="fas fa-book-open" style="color:#c9a84c; font-size:2.2rem; margin-top:10px;"></i>
          </div>
          <p style="font-size:0.75rem; color:rgba(255,255,255,0.6); line-height:1.5; margin:0;">In accordance with the Consumer Protection Code, we have a Virtual Complaints Book available.</p>
        </div>
      </a>
    </div>
  </div>
  <div class="fb"><div class="fbi"><span>Copyright &copy; 2026 Hidden Jungle Cusco. All rights reserved.</span><span>Site design: kemmesik</span></div></div>
</div></footer>"""

updated = 0

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
        
        # We need to replace the entire <footer class="ft">...</footer> block
        # Previously we had <div class="fg-legal">...</div> inside it.
        # We'll use regex to match from <footer class="ft"> to </footer>
        
        new_footer = get_new_footer(rel)
        
        new_c = re.sub(r'<footer class="ft">.*?</footer>', new_footer, c, flags=re.DOTALL)
        
        # Also clean up the old CSS we injected earlier
        new_c = re.sub(r'/\* ── Legal Footer Section ── \*/.*?(?=\n</style>)', '', new_c, flags=re.DOTALL)
        
        if new_c != c:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_c)
            updated += 1
            
print(f"Updated {updated} files with the new organized 5-column footer.")
