import os

file_path = r"g:\Git\MANUJUNGLEFOREVER\www.manujungleforever.com\guided-tours\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

js_to_inject = """// Tour Category Filter
document.addEventListener('DOMContentLoaded', function() {
  const btns = document.querySelectorAll('.cat-btn');
  const cards = document.querySelectorAll('.tour-card');
  const intro = document.getElementById('cat-intro');
  
  if(btns.length === 0 || cards.length === 0) return;

  function filterTours(cat) {
    btns.forEach(b => b.classList.toggle('active', b.dataset.cat === cat));
    
    // Animate cards
    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.pointerEvents = 'none';
      
      setTimeout(() => {
        if (cat === 'all' || card.dataset.cat === cat) {
          card.style.display = 'block';
          // trigger reflow
          void card.offsetWidth;
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
          card.style.pointerEvents = 'auto';
        } else {
          card.style.display = 'none';
        }
      }, 300);
    });
    
    if (intro) {
      if (cat === 'all') {
         intro.style.display = 'grid';
      } else {
         intro.style.display = 'none';
      }
    }
  }

  btns.forEach(btn => {
    btn.addEventListener('click', () => filterTours(btn.dataset.cat));
  });
});
"""

if 'Tour Category Filter' not in content:
    content = content.replace('// Modal\n', js_to_inject + '\n// Modal\n')
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected Tour Category Filter JS.")
else:
    print("JS already exists.")
