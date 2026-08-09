import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\about-2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Gloria is currently the second person. Let's find the exact block for Gloria.
match = re.search(r'(<h3 class=\'h3\' style=\'margin-bottom:4px;\'>Gloria</h3>.*?<div class=\'tour-rich-text\' style=\'font-size:0.95rem;\'>\s*)<p>.*?</p>', content, re.DOTALL)
if match:
    new_text = "Gloria is a passionate advocate for sustainable tourism and jungle conservation. Born and raised with a deep love for nature, she joined the Manu Jungle Forever family to ensure that every traveler experiences the true magic of the Peruvian Amazon. With her exceptional organizational skills and warm hospitality, she coordinates unforgettable adventures while working closely with local communities to preserve their cultural heritage. Gloria believes that every journey should be an authentic connection between the traveler and the wild."
    
    new_block = match.group(1) + "<p>" + new_text + "</p>"
    content = content[:match.start()] + new_block + content[match.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Could not find Gloria's block.")
