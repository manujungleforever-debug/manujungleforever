import os, re

base = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com"

# Read the 5-day page as template
template = open(os.path.join(base, "5-day-rainforest-road-trip", "index.html"), encoding='utf-8').read()

# Adapt it for the 4-day version
content = template

# Update title and description
content = content.replace(
    '<title>Cusco Jungle &amp; Manu National Park Tours | Manu Jungle Forever</title>',
    '<title>4-Day Rainforest Road Trip from Cusco | Manu Jungle Forever</title>'
)
content = content.replace(
    '<meta name="description" content="Explore Cusco Jungle &amp; Manu National Park tours with Manu Jungle Forever. Immerse yourself in wildlife — book your Peruvian Amazon adventure now!">',
    '<meta name="description" content="Experience a 4-Day Rainforest Road Trip from Cusco to the Manu National Park with Manu Jungle Forever. Local guides, wildlife, and authentic Amazon adventures.">'
)

# Update canonical
content = content.replace(
    '<link rel="canonical" href="https://www.manujungleforever.com/">',
    '<link rel="canonical" href="https://www.manujungleforever.com/4-day-rainforest-road-trip/">'
)

# Update hero section
content = content.replace(
    '<span class="ey" style="color:var(--a);">Jungle Tour</span>\n      <h1 class="h1" style="font-size:clamp(2.5rem,5vw,4.5rem); margin-bottom: 20px;">5-Day Rainforest Road Trip</h1>\n      <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">\n        <span style="background:rgba(255,255,255,0.1); padding:6px 16px; border-radius:20px; font-size:0.85rem;"><i class="far fa-clock"></i> 5 Days</span>',
    '<span class="ey" style="color:var(--a);">Jungle Tour</span>\n      <h1 class="h1" style="font-size:clamp(2.5rem,5vw,4.5rem); margin-bottom: 20px;">4-Day Rainforest Road Trip</h1>\n      <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">\n        <span style="background:rgba(255,255,255,0.1); padding:6px 16px; border-radius:20px; font-size:0.85rem;"><i class="far fa-clock"></i> 4 Days</span>'
)

# Update overview text
content = content.replace(
    '<h2 class="h2" style="font-size: 2rem;">Overview</h2>\n          <p style="font-size: 1.05rem; color:rgba(255,255,255,0.7); line-height: 1.8; margin-bottom: 30px;">\n            This tour is a completely blank canvas ready for your custom itinerary. Embark on a spectacular journey into the Amazon with Jordy and the team. Navigate winding rivers, hike ancient trails, and discover unparalleled biodiversity. This page has been completely stripped of the old Elementor structure to ensure incredible speed and a fresh start.\n          </p>',
    '<h2 class="h2" style="font-size: 2rem;">Overview</h2>\n          <p style="font-size: 1.05rem; color:rgba(255,255,255,0.7); line-height: 1.8; margin-bottom: 30px;">\n            The 4-Day Rainforest Road Trip is the perfect compact adventure for those who want to experience the magic of the Peruvian Amazon. Departing from Cusco, you\'ll travel along the spectacular Manu Road, descending from Andean highlands to the lush Amazon basin. Spot extraordinary wildlife, explore pristine rainforest trails with local expert guides, and stay in comfortable jungle lodges.\n          </p>'
)

# Update itinerary days
content = content.replace(
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 1: Into the Wild</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 1 itinerary. Insert your custom description here.)</p>',
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 1: Cusco to Cloud Forest</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">Depart Cusco by 4WD vehicle along the spectacular Manu Road. Ascend through Andean highlands, then descend through cloud forest — keep watch for spectacled bears and mountain tapirs. Arrive at the cloud forest lodge for dinner and overnight stay.</p>'
)

content = content.replace(
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 2: River Exploration</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 2 itinerary. Insert your custom description here.)</p>',
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 2: Amazon Rainforest Entrance</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">Continue down to the Amazon lowland rainforest. Take a guided nature walk and boat trip along the Madre de Dios River. Look for giant otters, caimans, kingfishers, and hundreds of bird species. Overnight at the jungle lodge.</p>'
)

content = content.replace(
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 3: Return to Cusco</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">(Placeholder text for Day 3 itinerary. Insert your custom description here.)</p>',
    '<h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 3: Wildlife & River Activities</h3>\n             <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">Full day of wildlife exploration. Visit a clay lick where parrots and macaws gather each morning, hike jungle trails with your guide, and enjoy an evening boat ride for nocturnal wildlife spotting.</p>'
)

# Add Day 4 before the closing div of the itinerary section
content = content.replace(
    '</div>\n\n        </div>\n\n        <!-- Right Sidebar -->',
    '</div>\n\n          <div style="background:var(--f); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px; margin-bottom:16px;">\n            <h3 style="color:var(--a); font-size:1.2rem; margin-bottom:12px;">Day 4: Return to Cusco</h3>\n            <p style="color:rgba(255,255,255,0.6); font-size:0.95rem;">Morning wildlife walk before boarding your 4WD for the scenic return journey to Cusco. Arrive in the afternoon with unforgettable memories of the Peruvian Amazon.</p>\n          </div>\n\n        </div>\n\n        <!-- Right Sidebar -->'
)

# Update Tour Details duration
content = content.replace(
    '<i class="fas fa-check-circle" style="color:var(--a);"></i> All Meals Included',
    '<i class="fas fa-check-circle" style="color:var(--a);"></i> 4 Days / 3 Nights'
)

# Update the active nav link to indicate Guided Tours is active
content = content.replace(
    '<a href="../guided-tours/index.html" class="on">Guided Tours',
    '<a href="../guided-tours/index.html" class="on">Guided Tours'
)

out_path = os.path.join(base, "4-day-rainforest-road-trip", "index.html")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created 4-day-rainforest-road-trip/index.html")
