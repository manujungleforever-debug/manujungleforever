import os

path = r'www.hiddenjunglecusco.com/blog/index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

card = '''      <a href="../discovering-the-mysteries-of-the-peruvian-amazon/index.html" class="blog-card r" style="text-decoration:none" aria-label="Discovering the Mysteries of the Peruvian Amazon">
        <div class="blog-img">
          <img src="../media/2026/05/Avatar-3.jpg" alt="Green Amazon jungle landscape" loading="lazy">
        </div>
        <div class="blog-desc">
          <span class="blog-meta">Wildlife</span>
          <h2>Discovering the Mysteries of the Peruvian Amazon</h2>
          <p>A deep journey into the heart of Manu. Discover what species inhabit the reserve and how to prepare...</p>
          <span class="blog-read"><i class="fas fa-arrow-right"></i> Read Article</span>
        </div>
      </a>
'''

html = html.replace('<div class="blog-grid" id="blog-grid">\n', '<div class="blog-grid" id="blog-grid">\n' + card)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Added card to blog index')
