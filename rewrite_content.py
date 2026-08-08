import os
import re
import random

directory = "www.manujungleforever.com"

# 100% original, copyright-free paragraphs about the Amazon/Manu
new_paragraphs = [
    "Embarking on a journey into the Peruvian Amazon is a transformative experience. As you navigate the winding tributaries, the sheer density of the rainforest reveals itself. Towering canopy trees block the intense equatorial sun, casting the forest floor in a permanent, emerald twilight. Every leaf and vine pulses with the hidden rhythm of one of the world's most intricate ecosystems.",
    "The biodiversity here is staggering and unparalleled. Expert guides lead you through complex trail networks, pointing out subtle signs of wildlife that an untrained eye would easily miss. From the vivid flashes of scarlet macaws overhead to the silent, calculated movements of a jaguar near the riverbank, the jungle constantly rewards those who watch and listen closely.",
    "Sustainable travel is at the core of true rainforest exploration. By respecting local guidelines and treading lightly, visitors help preserve this delicate balance. Eco-lodges blend seamlessly into the environment, offering rustic comfort without compromising the wilderness. Falling asleep to the chaotic symphony of insects and nocturnal frogs is an experience you will never forget.",
    "Mornings in the jungle begin before dawn. The mist hangs low over the oxbow lakes as you set out on a silent catamaran. This early hour is crucial for observing the giant river otters as they hunt, and for spotting prehistoric-looking hoatzin birds clumsily navigating the branches. The air is cool, thick with the scent of damp earth and blooming orchids.",
    "Beyond the incredible flora and fauna, the cultural immersion provides a profound perspective on Amazonian life. Interaction with local communities offers insight into traditional knowledge, medicinal plants, and survival techniques passed down through generations. Understanding the human element of the rainforest is essential to appreciating its true value and the urgent need for its protection."
]

p_pattern = re.compile(r'<p\b[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL)

# Directories to skip (we will do these manually for better quality)
skip_dirs = ['about-2', 'contact', 'departures', 'guided-tours']
skip_files = ['index.php', 'index.html', 'config.php']

def replace_paragraphs(match):
    # Don't replace if it's super short (like a button label or tiny meta info)
    content = match.group(1).strip()
    if len(content) < 40 or 'class="fa' in content or '<img' in content or 'Copyright' in content:
        return match.group(0)
    
    # Pick a random paragraph
    new_text = random.choice(new_paragraphs)
    # Keep the original opening <p> tag with its classes
    opening_tag = match.group(0).split('>')[0] + '>'
    return f"{opening_tag}{new_text}</p>"

for root, dirs, files in os.walk(directory):
    # Check if root contains a skip_dir
    if any(skip in root for skip in skip_dirs):
        continue
        
    for file in files:
        if file.endswith('.html') and file not in skip_files:
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = p_pattern.sub(replace_paragraphs, content)
                
                # Further scrub any titles/headers that might have 'Hidden'
                new_content = new_content.replace('Hidden Jungle', 'Manu Jungle')
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                pass
