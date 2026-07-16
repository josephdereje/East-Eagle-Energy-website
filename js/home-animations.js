/**
 * Homepage animations — scroll reveals + service cards
 * Hero panel animations handled in main.js + premium.css
 */
(function () {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  /* ── Energy flow stations: sequential spotlight ── */
  const flowStage = document.querySelector('.flow-stage');
  if (flowStage && !prefersReduced) {
    const stations = Array.from(flowStage.querySelectorAll('.flow-station'));
    let activeIndex = 0;

    const flowObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          flowObserver.unobserve(entry.target);
          stations.forEach((s, i) => {
            s.style.transitionDelay = `${i * 0.12}s`;
            s.classList.add('flow-station--live');
          });
          setInterval(() => {
            stations.forEach((s) => s.classList.remove('flow-station--active'));
            stations[activeIndex].classList.add('flow-station--active');
            activeIndex = (activeIndex + 1) % stations.length;
          }, 2200);
        });
      },
      { threshold: 0.25 }
    );
    flowObserver.observe(flowStage);
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

  /* ── Soft parallax on energy-flow grid ── */
  const flowBg = document.querySelector('.energy-flow-grid-bg');
  if (flowBg && !prefersReduced && window.innerWidth > 768) {
    window.addEventListener(
      'scroll',
      () => {
        const rect = flowBg.parentElement.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > window.innerHeight) return;
        const offset = (window.innerHeight / 2 - (rect.top + rect.height / 2)) * 0.04;
        flowBg.style.transform = `translateY(${offset}px)`;
      },
      { passive: true }
    );
  }
})();
