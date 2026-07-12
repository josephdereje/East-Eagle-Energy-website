/**
 * Product detail — multi-image gallery, thumbnails, slides, and lightbox
 */
(function () {
  const root = document.getElementById('productGalleryRoot');
  const gallery = document.getElementById('productGallery');
  const slides = root ? Array.from(root.querySelectorAll('.gallery-slide')) : [];
  const thumbs = root ? Array.from(root.querySelectorAll('.gallery-thumb')) : [];
  const prevBtn = document.getElementById('galleryPrevBtn');
  const nextBtn = document.getElementById('galleryNextBtn');
  const slideLabel = document.getElementById('gallerySlideLabel');
  const slideCounter = document.getElementById('gallerySlideCounter');
  const zoomBtn = document.getElementById('galleryZoomBtn');
  const lightbox = document.getElementById('productLightbox');
  const lightboxImg = document.getElementById('lightboxImage');
  const lightboxClose = document.getElementById('lightboxClose');
  const lightboxPrevBtn = document.getElementById('lightboxPrevBtn');
  const lightboxNextBtn = document.getElementById('lightboxNextBtn');
  const lightboxCounter = document.getElementById('lightboxCounter');

  if (!gallery || slides.length === 0) return;

  let currentIndex = slides.findIndex((slide) => slide.classList.contains('is-active'));
  if (currentIndex < 0) currentIndex = 0;

  function getActiveImage() {
    const activeSlide = slides[currentIndex];
    return activeSlide ? activeSlide.querySelector('.product-gallery-img') : null;
  }

  function updateGallery(index, options) {
    const opts = options || {};
    const total = slides.length;
    if (total === 0) return;

    currentIndex = ((index % total) + total) % total;

    slides.forEach((slide, i) => {
      slide.classList.toggle('is-active', i === currentIndex);
    });

    thumbs.forEach((thumb, i) => {
      const isActive = i === currentIndex;
      thumb.classList.toggle('is-active', isActive);
      thumb.setAttribute('aria-current', isActive ? 'true' : 'false');
    });

    const activeImg = getActiveImage();
    if (activeImg) {
      activeImg.style.transform = 'scale(1)';
      activeImg.style.transformOrigin = 'center center';
    }

    const activeThumb = thumbs[currentIndex];
    if (activeThumb && opts.scrollThumb !== false) {
      activeThumb.scrollIntoView({
        behavior: opts.instant ? 'auto' : 'smooth',
        block: 'nearest',
        inline: 'nearest',
      });
    }

    if (slideLabel && activeThumb) {
      slideLabel.textContent = activeThumb.getAttribute('aria-label') || '';
    }

    if (slideCounter) {
      slideCounter.textContent = `${currentIndex + 1} / ${total}`;
    }

    if (lightbox && lightbox.classList.contains('active')) {
      syncLightbox();
    }
  }

  function syncLightbox() {
    const activeImg = getActiveImage();
    if (!activeImg || !lightboxImg) return;
    lightboxImg.src = activeImg.src;
    lightboxImg.alt = activeImg.alt;
    if (lightboxCounter) {
      lightboxCounter.textContent = `${currentIndex + 1} / ${slides.length}`;
    }
  }

  function openLightbox() {
    if (!lightbox || !lightboxImg) return;
    syncLightbox();
    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('active');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function stepGallery(delta) {
    updateGallery(currentIndex + delta);
  }

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', () => {
      const index = Number(thumb.dataset.galleryIndex);
      if (!Number.isNaN(index)) updateGallery(index);
    });
  });

  if (prevBtn) prevBtn.addEventListener('click', (e) => { e.stopPropagation(); stepGallery(-1); });
  if (nextBtn) nextBtn.addEventListener('click', (e) => { e.stopPropagation(); stepGallery(1); });
  if (lightboxPrevBtn) lightboxPrevBtn.addEventListener('click', (e) => { e.stopPropagation(); stepGallery(-1); });
  if (lightboxNextBtn) lightboxNextBtn.addEventListener('click', (e) => { e.stopPropagation(); stepGallery(1); });

  gallery.addEventListener('mousemove', (e) => {
    const activeImg = getActiveImage();
    if (!activeImg) return;
    const rect = gallery.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    activeImg.style.transformOrigin = `${x}% ${y}%`;
    activeImg.style.transform = 'scale(1.5)';
  });

  gallery.addEventListener('mouseleave', () => {
    const activeImg = getActiveImage();
    if (activeImg) activeImg.style.transform = 'scale(1)';
  });

  if (zoomBtn) {
    zoomBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openLightbox();
    });
  }

  gallery.addEventListener('click', (e) => {
    if (e.target.closest('.gallery-nav')) return;
    openLightbox();
  });

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (!lightbox || !lightbox.classList.contains('active')) {
      if (e.key === 'ArrowLeft' && slides.length > 1) stepGallery(-1);
      if (e.key === 'ArrowRight' && slides.length > 1) stepGallery(1);
      return;
    }

    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') stepGallery(-1);
    if (e.key === 'ArrowRight') stepGallery(1);
  });

  let touchStartX = 0;
  gallery.addEventListener('touchstart', (e) => {
    if (slides.length <= 1 || !e.changedTouches[0]) return;
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });

  gallery.addEventListener('touchend', (e) => {
    if (slides.length <= 1 || !e.changedTouches[0]) return;
    const deltaX = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(deltaX) < 40) return;
    stepGallery(deltaX < 0 ? 1 : -1);
  }, { passive: true });

  updateGallery(currentIndex, { instant: true, scrollThumb: false });
})();
