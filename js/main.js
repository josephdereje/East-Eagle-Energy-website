document.getElementById('year').textContent = new Date().getFullYear();

// Mobile menu
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');

if (menuToggle && mainNav) {
  menuToggle.addEventListener('click', () => {
    mainNav.classList.toggle('open');
  });

  mainNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => mainNav.classList.remove('open'));
  });
}

// Hero background carousel + fixed content panel
const bgSlides = document.querySelectorAll('.slide-bg-item');
const dotsContainer = document.querySelector('.carousel-dots');
const prevBtn = document.querySelector('.carousel-btn.prev');
const nextBtn = document.querySelector('.carousel-btn.next');
const heroPanel = document.getElementById('heroContentPanel');
const heroProgress = document.getElementById('heroSlideProgress');
const heroCount = document.getElementById('heroSlideCount');
const heroFlash = document.getElementById('heroSlideFlash');
const heroSection = document.querySelector('.hero--future');
const SLIDE_DURATION = 7500;
let current = 0;
let interval;
let isContentTransitioning = false;

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function padSlideNum(n) {
  return String(n).padStart(2, '0');
}

function resetProgress() {
  if (!heroProgress) return;
  const fill = heroProgress.querySelector('.hero-slide-progress-fill');
  if (!fill) return;
  fill.style.animation = 'none';
  void fill.offsetWidth;
  fill.style.animation = '';
}

function updateSlideCount() {
  if (!heroCount) return;
  const currentEl = heroCount.querySelector('.hero-slide-current');
  const totalEl = heroCount.querySelector('.hero-slide-total');
  if (currentEl) currentEl.textContent = padSlideNum(current + 1);
  if (totalEl) totalEl.textContent = padSlideNum(bgSlides.length);
  heroCount.classList.remove('is-ticking');
  void heroCount.offsetWidth;
  heroCount.classList.add('is-ticking');
}

function applyPanelContent(slide) {
  if (!heroPanel || !slide) return;

  const eyebrow = heroPanel.querySelector('.hero-panel-eyebrow');
  const title = heroPanel.querySelector('.hero-panel-title');
  const subtitle = heroPanel.querySelector('.hero-panel-subtitle');
  const buttons = heroPanel.querySelector('.hero-panel-buttons');

  const setText = (el, value) => {
    if (!el) return;
    if (value) {
      el.textContent = value;
      el.hidden = false;
    } else {
      el.textContent = '';
      el.hidden = true;
    }
  };

  setText(eyebrow, slide.dataset.eyebrow);
  setText(title, slide.dataset.title);
  setText(subtitle, slide.dataset.subtitle);

  if (buttons) {
    buttons.innerHTML = '';
    if (slide.dataset.primaryText) {
      const primary = document.createElement('a');
      primary.href = slide.dataset.primaryUrl || '/products/';
      primary.className = 'btn btn-primary hero-panel-primary';
      primary.textContent = slide.dataset.primaryText;
      buttons.appendChild(primary);
    }
    if (slide.dataset.secondaryText) {
      const isContact = /contact/i.test(slide.dataset.secondaryText)
        || (slide.dataset.secondaryUrl && slide.dataset.secondaryUrl.includes('contact'));
      if (isContact) {
        const secondary = document.createElement('button');
        secondary.type = 'button';
        secondary.className = 'btn btn-outline hero-panel-secondary js-open-contact-slide';
        secondary.textContent = slide.dataset.secondaryText;
        buttons.appendChild(secondary);
      } else {
        const secondary = document.createElement('a');
        secondary.href = slide.dataset.secondaryUrl || '/contact/';
        secondary.className = 'btn btn-outline hero-panel-secondary';
        secondary.textContent = slide.dataset.secondaryText;
        buttons.appendChild(secondary);
      }
    }
  }
}

async function updateHeroPanel(slide) {
  if (!heroPanel || !slide || isContentTransitioning) return;
  isContentTransitioning = true;

  heroPanel.classList.remove('hero-panel--enter');
  heroPanel.classList.add('hero-panel--exit');
  await wait(420);

  applyPanelContent(slide);

  heroPanel.classList.remove('hero-panel--exit');
  heroPanel.classList.add('hero-panel--enter');

  resetProgress();

  document.dispatchEvent(new CustomEvent('heroSlideChange', {
    detail: { slide, index: current },
  }));

  await wait(900);
  heroPanel.classList.remove('hero-panel--enter');
  isContentTransitioning = false;
}

if (bgSlides.length && dotsContainer && prevBtn && nextBtn) {
  bgSlides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goTo(i, i > current ? 'next' : 'prev'));
    dotsContainer.appendChild(dot);
  });

  const dots = dotsContainer.querySelectorAll('button');
  updateSlideCount();

  function triggerSlideFlash() {
    if (!heroFlash) return;
    heroFlash.classList.remove('is-active');
    void heroFlash.offsetWidth;
    heroFlash.classList.add('is-active');
  }

  function setBgSlideState(prevIndex, nextIndex, direction) {
    const leaving = bgSlides[prevIndex];
    const entering = bgSlides[nextIndex];

    leaving.classList.remove('active');
    leaving.classList.add('is-leaving');

    entering.classList.remove('is-leaving', 'from-next', 'from-prev');
    entering.classList.add(direction === 'next' ? 'from-next' : 'from-prev');
    void entering.offsetWidth;
    entering.classList.add('active');
    triggerSlideFlash();

    window.setTimeout(() => {
      leaving.classList.remove('is-leaving');
      entering.classList.remove('from-next', 'from-prev');
    }, 1700);
  }

  async function goTo(index, direction) {
    const nextIndex = (index + bgSlides.length) % bgSlides.length;
    if (nextIndex === current) return;
    const slideDirection = direction || (nextIndex > current ? 'next' : 'prev');
    const prevIndex = current;

    dots[prevIndex].classList.remove('active');
    dots[nextIndex].classList.add('active');
    current = nextIndex;

    setBgSlideState(prevIndex, nextIndex, slideDirection);
    await updateHeroPanel(bgSlides[current]);
    updateSlideCount();
  }

  function next() { goTo(current + 1, 'next'); }
  function prev() { goTo(current - 1, 'prev'); }

  nextBtn.addEventListener('click', () => { next(); resetInterval(); });
  prevBtn.addEventListener('click', () => { prev(); resetInterval(); });

  function resetInterval() {
    clearInterval(interval);
    resetProgress();
    interval = setInterval(next, SLIDE_DURATION);
  }

  resetProgress();
  interval = setInterval(next, SLIDE_DURATION);
}

/* Subtle mouse parallax on hero background */
if (heroSection && bgSlides.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let parallaxRaf = null;
  let targetX = 0;
  let targetY = 0;

  heroSection.addEventListener('mousemove', (e) => {
    const rect = heroSection.getBoundingClientRect();
    targetX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    targetY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

    if (parallaxRaf) return;
    parallaxRaf = requestAnimationFrame(() => {
      const activeImg = heroSection.querySelector('.slide-bg-item.active .slide-bg-image');
      if (activeImg) {
        activeImg.style.transform = `translate(${targetX * -12}px, ${targetY * -8}px) scale(1.02)`;
      }
      parallaxRaf = null;
    });
  });

  heroSection.addEventListener('mouseleave', () => {
    const activeImg = heroSection.querySelector('.slide-bg-item.active .slide-bg-image');
    if (activeImg) activeImg.style.transform = '';
  });
}

// Active nav on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.main-nav a');

window.addEventListener('scroll', () => {
  let currentSection = '';
  sections.forEach(section => {
    const top = section.offsetTop - 120;
    if (window.scrollY >= top) currentSection = section.getAttribute('id');
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${currentSection}`) {
      link.classList.add('active');
    }
  });
});

// Subscribe form
const subscribeForm = document.querySelector('.subscribe-form');
if (subscribeForm) {
  subscribeForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = e.target.querySelector('input');
    if (input.value) {
      alert('Thank you for subscribing! We will keep you updated on solar energy solutions.');
      input.value = '';
    }
  });
}

// Get Quote form — Django handles submission via POST to /contact/submit/
const quoteForm = document.getElementById('quote-form');

if (quoteForm && quoteForm.method.toLowerCase() === 'post') {
  quoteForm.addEventListener('submit', (e) => {
    const fields = quoteForm.querySelectorAll('input, textarea');
    let valid = true;

    fields.forEach(field => {
      field.classList.remove('invalid');
      if (!field.value.trim()) {
        field.classList.add('invalid');
        valid = false;
      }
    });

    const email = quoteForm.querySelector('#quote-email');
    if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.classList.add('invalid');
      valid = false;
    }

    if (!valid) e.preventDefault();
  });
}
