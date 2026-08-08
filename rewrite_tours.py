import re

file_path = "www.manujungleforever.com/guided-tours/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace category descriptions
content = re.sub(
    r'<div class="ci-title">Wildlife Quest</div>\s*<div class="ci-sub">.*?</div>',
    '''<div class="ci-title">Wildlife Tracking</div>
    <div class="ci-sub">Navigate the waterways with expert indigenous trackers to locate giant river otters, macaws, and apex predators like the jaguar.</div>''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'<div class="ci-title">Amazon Expedition</div>\s*<div class="ci-sub">.*?</div>',
    '''<div class="ci-title">Deep Survival</div>
    <div class="ci-sub">Venture entirely off the grid. Master jungle survival techniques, sleep under the canopy, and experience absolute isolation.</div>''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'<div class="ci-title">Rainforest Road Trip</div>\s*<div class="ci-sub">.*?</div>',
    '''<div class="ci-title">Cloud Forest Ascent</div>
    <div class="ci-sub">A cultural and ecological journey from the high Andes down into the Amazon basin, engaging with remote communities.</div>''',
    content,
    flags=re.DOTALL
)

# Replace all tc-desc descriptions generically
def replace_tc_desc(match):
    return '<p class="tc-desc">An unforgettable journey curated for those seeking authentic adventure. Explore hidden trails, navigate ancient rivers, and immerse yourself in the world\'s most vibrant ecosystem with our expert native guides.</p>'

content = re.sub(
    r'<p class="tc-desc">.*?</p>',
    replace_tc_desc,
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
