/**
 * Recommended Products — classy, dynamic crossfade showcase
 */
(function () {
  const root = document.getElementById('recShowcase');
  if (!root) return;

  const slides = Array.from(root.querySelectorAll('[data-rec-slide]'));
  const dots = Array.from(root.querySelectorAll('[data-rec-goto]'));
  const prev = root.querySelector('.rec-prev');
  const next = root.querySelector('.rec-next');
  const counter = document.getElementById('recCounter');
  const stage = root.querySelector('.rec-stage');

  if (slides.length < 1) return;

  let index = 0;
  let timer = null;
  let paused = false;
  let animating = false;
  const DURATION = 5500;

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function goTo(nextIndex, direction) {
    if (!slides.length || animating) return;
    const total = slides.length;
    const incoming = ((nextIndex % total) + total) % total;
    if (incoming === index && slides[index].classList.contains('is-active')) {
      restartProgress();
      return;
    }

    const dir = direction || (incoming > index || (index === total - 1 && incoming === 0) ? 1 : -1);
    const current = slides[index];
    const nextSlideEl = slides[incoming];

    animating = true;
    current.classList.remove('is-active', 'is-enter-left', 'is-enter-right');
    current.classList.add(dir > 0 ? 'is-exit-left' : 'is-exit-right');
    current.setAttribute('aria-hidden', 'true');

    nextSlideEl.classList.remove('is-exit-left', 'is-exit-right');
    nextSlideEl.classList.add(dir > 0 ? 'is-enter-right' : 'is-enter-left');
    nextSlideEl.setAttribute('aria-hidden', 'false');

    // Next frame: activate for CSS transition
    requestAnimationFrame(() => {
      nextSlideEl.classList.add('is-active');
      nextSlideEl.classList.remove('is-enter-left', 'is-enter-right');
    });

    window.setTimeout(() => {
      current.classList.remove('is-exit-left', 'is-exit-right');
      animating = false;
    }, 780);

    index = incoming;

    dots.forEach((dot, i) => {
      dot.classList.toggle('is-active', i === index);
    });

    if (counter) {
      counter.textContent = pad(index + 1) + ' / ' + pad(total);
    }

    restartProgress();
  }

  function restartProgress() {
    dots.forEach((dot) => {
      const fill = dot.querySelector('.rec-progress-fill');
      if (!fill) return;
      fill.style.animation = 'none';
      void fill.offsetWidth;
      if (dot.classList.contains('is-active') && !paused) {
        fill.style.animation = 'recProgress ' + DURATION + 'ms linear forwards';
      }
    });
  }

  function nextSlide() {
    goTo(index + 1, 1);
  }

  function prevSlide() {
    goTo(index - 1, -1);
  }

  function startAuto() {
    stopAuto();
    if (slides.length < 2 || paused) return;
    timer = window.setInterval(() => {
      if (!paused && !animating) nextSlide();
    }, DURATION);
    restartProgress();
  }

  function stopAuto() {
    if (timer) {
      window.clearInterval(timer);
      timer = null;
    }
  }

  if (prev) prev.addEventListener('click', () => { prevSlide(); startAuto(); });
  if (next) next.addEventListener('click', () => { nextSlide(); startAuto(); });

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const i = Number(dot.getAttribute('data-rec-goto'));
      if (!Number.isNaN(i)) {
        goTo(i, i > index ? 1 : -1);
        startAuto();
      }
    });
  });

  // Touch swipe
  let touchX = null;
  if (stage) {
    stage.addEventListener('touchstart', (e) => {
      touchX = e.changedTouches[0].screenX;
    }, { passive: true });
    stage.addEventListener('touchend', (e) => {
      if (touchX == null) return;
      const dx = e.changedTouches[0].screenX - touchX;
      touchX = null;
      if (Math.abs(dx) < 40) return;
      if (dx < 0) nextSlide();
      else prevSlide();
      startAuto();
    }, { passive: true });

    stage.addEventListener('mouseenter', () => {
      paused = true;
      stopAuto();
      dots.forEach((dot) => {
        const fill = dot.querySelector('.rec-progress-fill');
        if (fill) fill.style.animationPlayState = 'paused';
      });
    });
    stage.addEventListener('mouseleave', () => {
      paused = false;
      startAuto();
    });
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopAuto();
    else if (!paused) startAuto();
  });

  // initial state
  slides.forEach((slide, i) => {
    slide.classList.toggle('is-active', i === 0);
    slide.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');
  });
  startAuto();
})();
