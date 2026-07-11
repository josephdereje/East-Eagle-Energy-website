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

// Carousel
const slides = document.querySelectorAll('.slide');
const dotsContainer = document.querySelector('.carousel-dots');
const prevBtn = document.querySelector('.carousel-btn.prev');
const nextBtn = document.querySelector('.carousel-btn.next');
let current = 0;
let interval;

if (slides.length && dotsContainer && prevBtn && nextBtn) {
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goTo(i));
    dotsContainer.appendChild(dot);
  });

  const dots = dotsContainer.querySelectorAll('button');

  function goTo(index) {
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current].classList.add('active');
    document.dispatchEvent(new CustomEvent('heroSlideChange', {
      detail: { slide: slides[current], index: current },
    }));
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  nextBtn.addEventListener('click', () => { next(); resetInterval(); });
  prevBtn.addEventListener('click', () => { prev(); resetInterval(); });

  function resetInterval() {
    clearInterval(interval);
    interval = setInterval(next, 6000);
  }

  interval = setInterval(next, 6000);
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
// Client-side validation only for empty fields before submit
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
