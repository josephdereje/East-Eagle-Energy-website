/**
 * Homepage animations — energy storage themed
 * Respects prefers-reduced-motion
 */
(function () {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Hero text stagger on load & slide change ── */
  function animateHeroSlide(slide) {
    if (!slide || prefersReduced) return;
    const items = slide.querySelectorAll('.hero-animate');
    items.forEach((el, i) => {
      el.style.animation = 'none';
      el.offsetHeight; // reflow
      el.style.animation = '';
      el.style.animationDelay = `${0.15 + i * 0.12}s`;
    });
  }

  const activeSlide = document.querySelector('.slide.active');
  if (activeSlide) animateHeroSlide(activeSlide);

  // Hook into carousel via custom event from main.js
  document.addEventListener('heroSlideChange', (e) => {
    animateHeroSlide(e.detail.slide);
  });

  /* ── Scroll reveal ── */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && !prefersReduced) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach((el, i) => {
      el.style.transitionDelay = `${(i % 4) * 0.08}s`;
      revealObserver.observe(el);
    });
  } else {
    revealEls.forEach((el) => el.classList.add('revealed'));
  }

  /* ── Counter animation ── */
  function animateCounter(el, target, duration) {
    if (prefersReduced) {
      el.textContent = target;
      return;
    }
    const start = performance.now();
    const isYear = target > 2000;

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(eased * target);
      el.textContent = isYear ? current : current.toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.dataset.count, 10);
            animateCounter(el, target, 1800);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => counterObserver.observe(el));
  }

  /* ── Service card tilt (subtle, desktop only) ── */
  if (!prefersReduced && window.innerWidth > 768) {
    document.querySelectorAll('.service-card').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `translateY(-6px) perspective(600px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }
})();
