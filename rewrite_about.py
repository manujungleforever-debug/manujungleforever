import re

file_path = "www.manujungleforever.com/about-2/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Intro Section
content = re.sub(
    r'<div class="elementor-widget-container">\s*<p>If you.*?</div>',
    '''<div class="elementor-widget-container">
    <p>Journeying into the Amazon is an expedition that requires absolute expertise. As indigenous natives of this lush wilderness, our mission is to guide you safely and authentically through one of the most biodiverse regions on Earth.</p>
    <p>From the high-altitude cloud forests near Cusco down to the deep river basin of Manu, every step with us is a masterclass in nature. Our expeditions bypass the standard tourist trails, taking you directly into the raw, unfiltered heart of the jungle.</p>
    <p>We are a dedicated local family, committed to preserving our ancestral lands by sharing their beauty with the world. Through sustainable, low-impact tourism, we protect the habitats of the jaguar, the giant otter, and countless other species while offering you the adventure of a lifetime.</p>
    </div>''',
    content,
    flags=re.DOTALL
)

# Replace Operator text
content = re.sub(
    r"<h3 class='h3'[^>]*>Local, Professional Tour Operator</h3>.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Indigenous Experts at the Helm</h3>
    <h3 class='h3' style='margin-bottom:12px;'>Guardians of the Rainforest</h3>
    <div class='tour-rich-text'>
    <p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;">Our guides are born and raised in the jungle. They possess an intimate, generational knowledge of the flora, fauna, and shifting river currents, ensuring your expedition is both thrilling and completely safe.</p>
    <p style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;">We operate with a strict eco-friendly mandate. Every tour directly funds local conservation initiatives and provides sustainable income for remote communities, acting as a bulwark against deforestation.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

# Replace Ground Transport
content = re.sub(
    r"<h3 class='h3'[^>]*>Ground Transport</h3>.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Overland Journey</h3>
    <span class='ey' style='display:block; margin-bottom:8px;'>Expert Navigation</span>
    <div class='tour-rich-text'>
    <p>The descent from the Andes into the Amazon basin is spectacular. We utilize a fleet of rigorously maintained, private 4x4 vehicles. Our veteran drivers navigate the winding mountain passes with absolute precision, stopping at key viewpoints in the cloud forest.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

# Replace River Transport
content = re.sub(
    r"<h3 class='h3'[^>]*>River Transport</h3>.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>River Navigation</h3>
    <div class='tour-rich-text'>
    <p>The rivers are the highways of the Amazon. You will cruise the Madre de Dios in our robust, motorized longboats, designed for stability and maximum visibility. This is your first real opportunity to spot river turtles, caimans, and exotic birds along the banks.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

# Replace Lodging text generally using regex for all lodging sections
content = re.sub(
    r"<h3 class='h3'[^>]*>Lodging: Bambu Lodge \(Patria\)</h3>.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Eco-Lodge Stays</h3>
    <div class='tour-rich-text'>
    <p>Our network of partner lodges provides a comfortable sanctuary amidst the wild. Built from sustainable materials, they blend into the canopy. You will sleep under protective mosquito netting, with access to essential amenities and basic running water.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"<h3 class='h3'[^>]*>Lodging: Avatar Lodge.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Jungle Bungalows</h3>
    <div class='tour-rich-text'>
    <p>Deep in the reserve, these rustic bungalows serve as our strategic basecamp. Surrounded by the cacophony of nocturnal insects and distant howler monkeys, you will experience true immersion without sacrificing safety or basic comforts.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"<h3 class='h3'[^>]*>Lodging: Nuevo Eden.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Our Private Outpost</h3>
    <div class='tour-rich-text'>
    <p>Located on our ancestral lands, this exclusive outpost offers an intimate look into native life. Far removed from standard tourist routes, it features traditional architecture and direct access to pristine, unexplored trail systems.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"<h3 class='h3'[^>]*>Lodging: Camouflage.*?</div>\s*</div>\s*</div>",
    '''<h3 class='h3' style='margin-bottom:12px;'>Canopy Camping</h3>
    <div class='tour-rich-text'>
    <p>For the ultimate adventurer, we offer open-air sleeping platforms deep in the forest. Elevated off the ground and fully netted, you can safely watch the stars and listen to the breathing of the jungle around you.</p>
    </div>
    </div>
    </div>''',
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
