import re
import os

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\about-2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to extract individual team members
# A team member starts with <!-- Team Member --> and ends with the closing of the .team-row div.
# Because the structure is standard, we can just split by <!-- Team Member -->
parts = content.split('<!-- Team Member -->')

pre = parts[0]
blocks = parts[1:]

jordy_block = ""
gloria_block = ""
post_last = ""

for block in blocks:
    if 'Moises Llaqui Llanca' in block:
        pass
    elif 'Cayetano LLaqui' in block:
        pass
    elif 'Anna Ashley' in block:
        # Swap Anna to Gloria
        b = block.replace('Anna Ashley', 'Gloria')
        gloria_block = '<!-- Team Member -->' + b
    elif 'Jordy Leonidas' in block:
        jordy_block = '<!-- Team Member -->' + block
    elif 'Placida Yanca' in block:
        # This is the last block. We need to find where the .team-row ends to grab the rest of the HTML!
        # A .team-row has 2 nested divs (.split-left and .split-right).
        # We can find the end of the split-row by looking for </section> which comes after all team members!
        # Wait, if we just split by <!-- Team Member -->, the last block will contain Placida AND the rest of the page!
        # Let's find </section> inside this block? No, there is a closing </div> for the <div class="cx">
        # Let's just find the last </div>\n          </div> that belongs to the team row.
        # Actually, if we just split the entire content by <!-- Team Member -->, the LAST part contains Placida AND the rest of the HTML.
        # We need to cleanly separate Placida from the rest of the HTML.
        pass

# A better way is to use re.sub with a function!
def replace_team(match):
    block = match.group(0)
    if 'Moises Llaqui Llanca' in block or 'Cayetano LLaqui' in block or 'Placida Yanca' in block:
        return ''
    return block

# The regex matches exactly one team member block.
# We match from <!-- Team Member --> up to the next <!-- Team Member --> or </section>
pattern = re.compile(r'<!-- Team Member -->\s*<div class="split-row team-row.*?(?=<!-- Team Member -->|</section>)', re.DOTALL)

# Let's extract them all:
matches = pattern.findall(content)
for m in matches:
    if 'Jordy Leonidas' in m:
        jordy_block = m
    elif 'Anna Ashley' in m:
        gloria_block = m.replace('Anna Ashley', 'Gloria')

# We can replace the whole section of team members!
all_team_regex = re.compile(r'(<!-- Team Member -->.*?(?=</section>))', re.DOTALL)

new_team_html = jordy_block + '\n' + gloria_block + '\n'

new_content = all_team_regex.sub(new_team_html, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("About Us updated.")
