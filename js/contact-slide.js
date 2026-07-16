/**
 * Slide-in contact panel
 */
(function () {
  const slide = document.getElementById('contactSlide');
  const backdrop = document.getElementById('contactSlideBackdrop');
  const closeBtn = document.getElementById('contactSlideClose');
  const panel = slide && slide.querySelector('.contact-slide-panel');

  if (!slide || !panel) return;

  function openContactSlide() {
    slide.classList.add('is-open');
    slide.setAttribute('aria-hidden', 'false');
    document.body.classList.add('contact-slide-open');
    slide.querySelectorAll('.contact-slide-field').forEach((el, i) => {
      el.style.animationDelay = `${0.08 + i * 0.07}s`;
    });
    const submit = slide.querySelector('.contact-slide-submit');
    if (submit) submit.style.animationDelay = '0.36s';
    const firstInput = slide.querySelector('#slide-contact-name');
    if (firstInput) window.setTimeout(() => firstInput.focus(), 420);
  }

  function closeContactSlide() {
    slide.classList.remove('is-open');
    slide.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('contact-slide-open');
  }

  document.querySelectorAll('.js-open-contact-slide').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      openContactSlide();
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeContactSlide);
  if (backdrop) backdrop.addEventListener('click', closeContactSlide);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && slide.classList.contains('is-open')) {
      closeContactSlide();
    }
  });

  window.openContactSlide = openContactSlide;
})();
