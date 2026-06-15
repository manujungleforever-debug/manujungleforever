import os
import re

template_path = r"G:\Git\HiddenJungleCusco\www.hiddenjunglecusco.com\amazon-rainforest-tour-to-manu-national-park-from-cusco\index.html"
with open(template_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Target directory
out_dir = r"G:\Git\HiddenJungleCusco\www.hiddenjunglecusco.com\discovering-the-mysteries-of-the-peruvian-amazon"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "index.html")

# Replacements
html = html.replace("Amazon Rainforest Tour to Manu National Park from Cusco", "Discovering the Mysteries of the Peruvian Amazon")
html = html.replace("amazon-rainforest-tour-to-manu-national-park-from-cusco", "discovering-the-mysteries-of-the-peruvian-amazon")

# Replace the article meta
html = re.sub(r'May 15, 2026', 'June 15, 2026', html)

# Replace the article content
new_content = """
<img src="../media/2026/05/Avatar-3.jpg" alt="Green Amazon jungle landscape" loading="lazy">
<h1>Discovering the Mysteries of the Peruvian Amazon</h1>
<p>The Peruvian Amazon hides mysteries that only the most intrepid adventurers get to know. At <strong>Hidden Jungle Cusco</strong>, we specialize in guiding you through these natural wonders.</p>

<h2>🐒 The Biodiversity of the Reserve</h2>
<p>As you venture into the heart of Manu, you will find yourself surrounded by a vibrant ecosystem. This place is not just a destination; it's an immersive experience.</p>

<h3>Species you might spot:</h3>
<ul>
<li><strong>Exotic birds:</strong> Such as the iconic Andean Cock-of-the-rock and colorful macaws.</li>
<li><strong>Mammals:</strong> Different species of monkeys and, with luck, jaguars.</li>
<li><strong>Giant flora:</strong> Millennial trees like the Ceiba that reach over 50 meters in height.</li>
</ul>

<blockquote>"The jungle is not visited, it is felt. Every sound, every leaf, every river tells the story of mother earth."</blockquote>

<h2>🛶 What to pack for your adventure?</h2>
<p>To make your experience comfortable and safe, we recommend packing light but smart:</p>
<ol>
<li>Light-colored, long-sleeved cotton clothing.</li>
<li>Insect repellent (preferably eco-friendly).</li>
<li>Water-resistant hiking boots.</li>
<li>Headlamp with extra batteries.</li>
</ol>

<p>If you have any questions about our itinerary or want to know more technical details, contact our team of specialized guides. We await you in the jungle!</p>
"""

html = re.sub(r'(<div class="article-body">).*?(</div>\s*<!-- Comments)', r'\1\n' + new_content + r'\n    \2', html, flags=re.DOTALL)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated HTML for discovering-the-mysteries-of-the-peruvian-amazon")
