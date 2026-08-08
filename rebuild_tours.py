import os
import re

base_dir = "www.manujungleforever.com"
index_php_path = os.path.join(base_dir, "index.php")

# 1. Extract header and footer from index.php
with open(index_php_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Replace any ../ or assets/ paths in header/footer to be relative correctly for subdirs
# In index.php they are "assets/..." but from a subdir they need to be "../assets/..."
# Wait, let's just make it absolute or use ../
# Let's split first.
match = re.search(r'(.*?)<main id="main">.*?</main>(.*)', index_content, flags=re.DOTALL)
if not match:
    print("Could not parse index.php")
    exit(1)

header_part = match.group(1) + '<main id="main">'
footer_part = '</main>' + match.group(2)

# Fix paths in header/footer for subdirectories
header_part = header_part.replace('href="assets/', 'href="../assets/')
header_part = header_part.replace('src="assets/', 'src="../assets/')
header_part = header_part.replace('href="index.html"', 'href="../index.html"')
header_part = header_part.replace('href="guided-tours/', 'href="../guided-tours/')
header_part = header_part.replace('href="about-2/', 'href="../about-2/')
header_part = header_part.replace('href="departures/', 'href="../departures/')
header_part = header_part.replace('href="contact/', 'href="../contact/')
header_part = header_part.replace('href="news-and-gallery/', 'href="../news-and-gallery/')
header_part = header_part.replace('href="blog/', 'href="../blog/')

# Same for all tour links
tour_dirs = [
    "wildlife-tours-from-cusco",
    "3-day-wildlife-quest-machu-wasi",
    "4-day-wildlife-quest-machu-wasi",
    "4-day-wildlife-quest-nuevo-eden",
    "5-day-wildlife-quest-nuevo-eden",
    "6-day-wildlife-quest-blanquillo",
    "6-day-wildlife-quest-reserved-zone",
    "8-day-wildlife-photography-tour",
    "rainforest-road-trip-from-cusco",
    "2-day-rainforest-road-trip",
    "5-day-rainforest-road-trip",
    "5-day-amazon-expedition",
    "6-day-amazon-expedition"
]

for t in tour_dirs:
    header_part = header_part.replace(f'href="{t}/', f'href="../{t}/')
    footer_part = footer_part.replace(f'href="{t}/', f'href="../{t}/')

footer_part = footer_part.replace('href="assets/', 'href="../assets/')
footer_part = footer_part.replace('src="assets/', 'src="../assets/')
footer_part = footer_part.replace('href="index.html"', 'href="../index.html"')

def generate_tour_html(title, duration):
    body = f"""
  <!-- New Hero -->
  <section class="in-hero" style="background-image:url('../assets/img/hero.png'); padding: 180px 0 100px;">
    <div class="cx">
      <span class="ey" style="color:var(--a);">Jungle Tour</span>
      <h1 class="h1" style="font-size:clamp(2.5rem,5vw,4.5rem); margin-bottom: 20px;">{title}</h1>
      <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
        <span style="background:rgba(255,255,255,0.1); padding:6px 16px; border-radius:20px; font-size:0.85rem;"><i class="far fa-clock"></i> {duration}</span>
        <span style="background:rgba(255,255,255,0.1); padding:6px 16px; border-radius:20px; font-size:0.85rem;"><i class="fas fa-users"></i> Small Groups</span>
      </div>
    </div>
  </section>

  <section class="sec" style="background:var(--k);">
    <div class="cx">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 50px;">
        
        <!-- Left Content -->
        <div>
          <h2 class="h2" style="font-size: 2rem;">Overview</h2>
          <p style="font-size: 1.05rem; color:rgba(255,255,255,0.7); line-height: 1.8; margin-bottom: 30px;">
            This tour is a completely blank canvas ready for your custom itinerary. Embark on a spectacular journey into the Amazon with Jordy and the team. Navigate winding rivers, hike ancient trails, and discover unparalleled biodiversity. This page has been completely stripped of the old Elementor structure to ensure incredible speed and a fresh start.
          </p>
          
          <h2 class="h2" style="font-size: 2rem; margin-top: 50px;">Itinerary</h2>
          
          <div style="background:var(--f); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px; margin-bottom:16px;">
            <h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 1: Into the Wild</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 1 itinerary. Insert your custom description here.)</p>
          </div>
          
          <div style="background:var(--f); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px; margin-bottom:16px;">
            <h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 2: River Exploration</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 2 itinerary. Insert your custom description here.)</p>
          </div>

          <div style="background:var(--f); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px; margin-bottom:16px;">
            <h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 3: Return to Cusco</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 3 itinerary. Insert your custom description here.)</p>
          </div>

        </div>

        <!-- Right Sidebar -->
        <div style="align-self: start; background:var(--f); border:1px solid rgba(34,211,238,0.25); border-radius:20px; padding:32px;">
          <h3 style="font-size:1.4rem; margin-bottom:24px;">Tour Details</h3>
          <ul style="display:flex; flex-direction:column; gap:16px; margin-bottom: 32px; padding:0;">
            <li style="display:flex; align-items:center; gap:12px; color:rgba(255,255,255,0.8);"><i class="fas fa-check-circle" style="color:var(--a);"></i> All Meals Included</li>
            <li style="display:flex; align-items:center; gap:12px; color:rgba(255,255,255,0.8);"><i class="fas fa-check-circle" style="color:var(--a);"></i> Private Transport</li>
            <li style="display:flex; align-items:center; gap:12px; color:rgba(255,255,255,0.8);"><i class="fas fa-check-circle" style="color:var(--a);"></i> Lodge Accommodation</li>
            <li style="display:flex; align-items:center; gap:12px; color:rgba(255,255,255,0.8);"><i class="fas fa-check-circle" style="color:var(--a);"></i> Local Expert Guide</li>
          </ul>
          <button class="btn ba" style="width:100%; justify-content:center; padding:18px; border:none; border-radius:30px; font-size:1rem; font-weight:700;">Book This Tour</button>
        </div>
      </div>
    </div>
  </section>
"""
    return header_part + body + footer_part

# Map of directory to title and duration
tour_details = {
    "wildlife-tours-from-cusco": ("Wildlife Tours", "Multiple Options"),
    "3-day-wildlife-quest-machu-wasi": ("3-Day Wildlife Quest: Machu Wasi", "3 Days"),
    "4-day-wildlife-quest-machu-wasi": ("4-Day Wildlife Quest: Machu Wasi", "4 Days"),
    "4-day-wildlife-quest-nuevo-eden": ("4-Day Wildlife Quest: Nuevo Eden", "4 Days"),
    "5-day-wildlife-quest-nuevo-eden": ("5-Day Wildlife Quest: Nuevo Eden", "5 Days"),
    "6-day-wildlife-quest-blanquillo": ("6-Day Wildlife Quest: Blanquillo", "6 Days"),
    "6-day-wildlife-quest-reserved-zone": ("Manu Reserved Zone", "6 Days"),
    "8-day-wildlife-photography-tour": ("Wildlife Photography Tour", "8 Days"),
    "rainforest-road-trip-from-cusco": ("Rainforest Road Trip", "Multiple Options"),
    "2-day-rainforest-road-trip": ("2-Day Rainforest Road Trip", "2 Days"),
    "5-day-rainforest-road-trip": ("5-Day Rainforest Road Trip", "5 Days"),
    "5-day-amazon-expedition": ("5-Day Amazon Expedition", "5 Days"),
    "6-day-amazon-expedition": ("6-Day Amazon Expedition", "6 Days")
}

for tour_dir, (title, duration) in tour_details.items():
    full_path = os.path.join(base_dir, tour_dir, "index.html")
    if os.path.exists(os.path.dirname(full_path)):
        html = generate_tour_html(title, duration)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Rebuilt {tour_dir}")
