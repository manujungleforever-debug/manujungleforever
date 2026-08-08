import re

file_path = "www.manujungleforever.com/index.php"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace About Section
content = re.sub(
    r'<span class="ey">Why Choose Us</span>.*?<div class="chips">',
    '''<span class="ey">The Manu Experience</span>
    <h2 class="h2">Unearth the Amazon with True Local Experts</h2>
    <p>Embarking on a journey into the world's most biodiverse ecosystem is a life-changing milestone. We specialize in curating breathtaking, raw, and authentic expeditions from Cusco deep into the untamed wilderness of the Manu Biosphere Reserve.</p>
    <p>Our operations are deeply rooted in the heart of the jungle. Founded by indigenous experts who have spent their entire lives navigating these complex river systems, we offer an unparalleled and immersive dive into nature.</p>
    <p>Whether you're an avid wildlife photographer tracking the elusive jaguar or a traveler seeking a profound cultural connection, we provide premium, sustainable adventures that respect and protect the Amazon.</p>
    <div class="chips">''',
    content,
    flags=re.DOTALL
)

# Replace Tours Intro
content = re.sub(
    r'<h2 class="h2">Our Tours: Something for Everyone</h2>\s*<p class="ld">We have thoughtfully created.*?</p>',
    '''<h2 class="h2">Curated Jungle Expeditions</h2>
    <p class="ld">Our itineraries are meticulously designed to cater to true nature enthusiasts. From deep-forest survival treks for the intrepid explorer, to focused wildlife spotting cruises along the riverbanks, our routes guarantee a transformative encounter with the wild.</p>''',
    content,
    flags=re.DOTALL
)

# Replace Unique Content
content = re.sub(
    r'<h2 style="background:#0078d4;[^>]+>WHAT MAKES US UNIQUE\?</h2>\s*</div>\s*<p style="[^>]+>We are a family-run.*?</p>',
    '''<h2 style="background:#22d3ee; color:#070B14; display:inline-block; padding:6px 16px; font-family:'Syne',sans-serif; font-size:1.4rem; letter-spacing:0.05em; font-weight:800; text-transform:uppercase">A LEGACY OF CONSERVATION</h2>
    </div>
    <p style="font-size:1.05rem;color:rgba(255,255,255,.75);line-height:1.85">Our deep connection to the land sets us apart. We don't just visit the Amazon; we protect it. By choosing our expeditions, you directly contribute to anti-logging efforts and the empowerment of local indigenous communities. We believe responsible eco-tourism is the most powerful tool against deforestation. Join us, and become part of a legacy that ensures the jungle thrives forever.</p>''',
    content,
    flags=re.DOTALL
)

# Replace Wildlife Text
content = re.sub(
    r'<p class="lead" style="[^>]+>The Manu National Park is the best place to see wildlife in Peru.*?elusive jaguar\.</p>',
    '''<p class="lead" style="color:rgba(255,255,255,.7)">The Manu Biosphere is globally recognized as an unparalleled haven for biodiversity. Navigating its ancient tributaries, you will witness a thriving, complex ecosystem completely untouched by modern civilization. Our expert trackers will guide you through hidden trails, revealing a spectacular array of exotic species in their pure, natural habitats.</p>''',
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
