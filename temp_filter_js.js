  // Header scroll
  const N=document.getElementById('N');
  window.addEventListener('scroll',()=>N.classList.toggle('s',scrollY>60),{passive:true});
  // Burger
  const bg=document.getElementById('bg'),mo=document.getElementById('mo');
  bg.addEventListener('click',()=>{const o=mo.classList.toggle('o');bg.classList.toggle('o',o);bg.setAttribute('aria-expanded',o);mo.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';});
  document.getElementById('mbt').addEventListener('click',()=>document.getElementById('mdd').classList.toggle('o'));
  // Reveal on scroll
  const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('v');obs.unobserve(e.target);}}),{threshold:.08});
  document.querySelectorAll('.r,.rl,.rr').forEach(el=>obs.observe(el));
})();

// ── Category Filter ──────────────────────────────────────────
(function(){
  const buttons = document.querySelectorAll('.cat-btn');
  const cards   = document.querySelectorAll('.tour-card');
  const noRes   = document.getElementById('no-results');
  const intro   = document.getElementById('cat-intro');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.cat;

      // Active state
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Do not hide intro cards, keep them visible for continuous filtering
      // intro.style.display = (cat === 'all') ? 'grid' : 'none';

      // Filter cards with animation
      let visible = 0;
      cards.forEach(card => {
        const match = cat === 'all' || card.dataset.cat === cat;
        if (match) {
          card.style.display = 'flex';
          card.style.animation = 'fadeInUp .35s ease both';
          visible++;
        } else {
          card.style.display = 'none';
          card.style.animation = '';
        }
      });

      noRes.style.display = visible === 0 ? 'block' : 'none';
    });
  });
})();