import re

path = r'g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\about-2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the alt attribute for Gloria
content = content.replace(
    "alt='Anna, co-founder, on the way to the jungle'",
    "alt='Gloria, on the way to the jungle'"
)

# Replace the text paragraph
old_p = r"<p>“Anna caught the travel bug from a young age, intrigued by different cultures and languages.  She\s*visited Peru for the first time while traveling for work, and decided to stay a while to really know the\s*culture. As a traveler, she’s visited over 30 countries and always seeks out unique, local experiences.\s*She’s created Manu Jungle Forever for travelers like her, who want to have a fun, relaxed genuine\s*experience in a different country.”</p>"
new_p = r"<p>“Gloria is a passionate advocate for sustainable tourism and jungle conservation. Born and raised with a deep love for nature, she joined the Manu Jungle Forever family to ensure that every traveler experiences the true magic of the Peruvian Amazon. With her exceptional organizational skills and warm hospitality, she coordinates unforgettable adventures while working closely with local communities to preserve their cultural heritage. Gloria believes that every journey should be an authentic connection between the traveler and the wild.”</p>"

content = re.sub(old_p, new_p, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Gloria's biography.")
