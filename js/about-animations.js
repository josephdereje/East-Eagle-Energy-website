/**
 * About page — hero slideshow, showcase, timeline, counters, card tilt
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
      el.style.transitionDelay = `${(i % 5) * 0.07}s`;
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
            animateCounter(el, parseInt(el.dataset.count, 10), 1800);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => counterObserver.observe(el));
  }

  /* ── Hero background slideshow ── */
  const heroSlides = document.querySelectorAll('.about-hero-bg-slide');
  let heroIndex = 0;
  let heroTimer;

  function showHeroSlide(index) {
    if (!heroSlides.length) return;
    heroSlides.forEach((s) => s.classList.remove('active'));
    heroSlides[index].classList.add('active');
  }

  function nextHeroSlide() {
    if (!heroSlides.length) return;
    heroIndex = (heroIndex + 1) % heroSlides.length;
    showHeroSlide(heroIndex);
  }

  if (heroSlides.length > 1 && !prefersReduced) {
    heroTimer = setInterval(nextHeroSlide, 6000);
  }

  /* ── Showcase slideshow + dots ── */
  const showcaseSlides = document.querySelectorAll('.about-showcase-slide');
  const dotsWrap = document.getElementById('aboutShowcaseDots');
  let showcaseIndex = 0;
  let showcaseTimer;

  function showShowcase(index) {
    if (!showcaseSlides.length) return;
    showcaseSlides.forEach((s, i) => {
      s.classList.toggle('active', i === index);
    });
    if (dotsWrap) {
      dotsWrap.querySelectorAll('button').forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
      });
    }
  }

  if (showcaseSlides.length && dotsWrap) {
    showcaseSlides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', `Showcase image ${i + 1}`);
      if (i === 0) dot.classList.add('active');
      dot.addEventListener('click', () => {
        showcaseIndex = i;
        showShowcase(showcaseIndex);
        clearInterval(showcaseTimer);
        showcaseTimer = setInterval(() => {
          showcaseIndex = (showcaseIndex + 1) % showcaseSlides.length;
          showShowcase(showcaseIndex);
        }, 5000);
      });
      dotsWrap.appendChild(dot);
    });

    if (!prefersReduced && showcaseSlides.length > 1) {
      showcaseTimer = setInterval(() => {
        showcaseIndex = (showcaseIndex + 1) % showcaseSlides.length;
        showShowcase(showcaseIndex);
      }, 5000);
    }
  }

  /* ── Timeline rail fill on scroll ── */
  const timeline = document.getElementById('aboutTimeline');
  const timelineFill = document.getElementById('aboutTimelineFill');

  if (timeline && timelineFill && !prefersReduced) {
    window.addEventListener(
      'scroll',
      () => {
        const rect = timeline.getBoundingClientRect();
        const viewH = window.innerHeight;
        const start = viewH * 0.85;
        const end = viewH * 0.15;
        const progress = Math.min(Math.max((start - rect.top) / (rect.height + start - end), 0), 1);
        timelineFill.style.height = `${progress * 100}%`;
      },
      { passive: true }
    );
  } else if (timelineFill) {
    timelineFill.style.height = '100%';
  }

  /* ── Value card tilt ── */
  if (!prefersReduced && window.innerWidth > 768) {
    document.querySelectorAll('[data-tilt]').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `translateY(-6px) perspective(700px) rotateX(${-y * 5}deg) rotateY(${x * 5}deg)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }
})();
