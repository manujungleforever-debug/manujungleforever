/* ===================================================
   main.js – Manu Jungle Forever
   =================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Sticky header ─────────────────────────────── */
  const header = document.getElementById('site-header');
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── Mobile menu toggle ────────────────────────── */
  const toggle   = document.querySelector('.nav-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  toggle?.addEventListener('click', () => {
    const open = mobileMenu.classList.toggle('open');
    toggle.classList.toggle('open', open);
    mobileMenu.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  });

  /* ── Mobile dropdowns ──────────────────────────── */
  document.querySelectorAll('.mobile-dropdown-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const dd = btn.nextElementSibling;
      dd?.classList.toggle('open');
      btn.querySelector('i')?.classList.toggle('fa-rotate-180');
    });
  });

  /* ── Close mobile menu on outside click ────────── */
  document.addEventListener('click', e => {
    if (mobileMenu?.classList.contains('open') &&
        !mobileMenu.contains(e.target) &&
        !toggle.contains(e.target)) {
      mobileMenu.classList.remove('open');
      toggle.classList.remove('open');
      document.body.style.overflow = '';
    }
  });

  /* ── Scroll-reveal (IntersectionObserver) ───────── */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('visible'));
  }

  /* ── Contact form AJAX ─────────────────────────── */
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = contactForm.querySelector('[type="submit"]');
      const msg = document.getElementById('contact-msg');
      btn.disabled = true;
      btn.textContent = 'Sending…';
      try {
        const res  = await fetch('handlers/send-contact.php', {
          method: 'POST', body: new FormData(contactForm)
        });
        const data = await res.json();
        msg.className = data.ok ? 'form-msg success' : 'form-msg error';
        msg.textContent = data.message;
        if (data.ok) contactForm.reset();
      } catch {
        msg.className = 'form-msg error';
        msg.textContent = 'Something went wrong. Please try again.';
      } finally {
        btn.disabled = false;
        btn.textContent = 'Send Message';
      }
    });
  }

  /* ── Booking modal ─────────────────────────────── */
  const openBtns  = document.querySelectorAll('[data-modal]');
  const modals    = document.querySelectorAll('.modal-overlay');

  openBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.modal;
      document.getElementById(id)?.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  modals.forEach(m => {
    m.addEventListener('click', e => {
      if (e.target === m || e.target.classList.contains('modal-close')) {
        m.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
    // Booking form AJAX inside modal
    const bForm = m.querySelector('.booking-form');
    if (bForm) {
      bForm.addEventListener('submit', async e => {
        e.preventDefault();
        const btn = bForm.querySelector('[type="submit"]');
        const msg = bForm.querySelector('.form-msg');
        btn.disabled = true;
        btn.textContent = 'Sending…';
        try {
          const res  = await fetch('handlers/send-booking.php', {
            method: 'POST', body: new FormData(bForm)
          });
          const data = await res.json();
          msg.className = data.ok ? 'form-msg success' : 'form-msg error';
          msg.textContent = data.message;
          if (data.ok) bForm.reset();
        } catch {
          msg.className = 'form-msg error';
          msg.textContent = 'Something went wrong. Please try again.';
        } finally {
          btn.disabled = false;
          btn.textContent = 'Send Enquiry';
        }
      });
    }
  });

  /* ── Keyboard close modal (ESC) ─────────────────── */
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.open').forEach(m => {
        m.classList.remove('open');
        document.body.style.overflow = '';
      });
    }
  });
});
