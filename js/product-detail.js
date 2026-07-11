/**
 * Product detail — image zoom and lightbox
 */
(function () {
  const gallery = document.getElementById('productGallery');
  const mainImg = document.getElementById('productMainImage');
  const zoomBtn = document.getElementById('galleryZoomBtn');
  const lightbox = document.getElementById('productLightbox');
  const lightboxImg = document.getElementById('lightboxImage');
  const lightboxClose = document.getElementById('lightboxClose');

  if (!gallery || !mainImg) return;

  function openLightbox() {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = mainImg.src;
    lightboxImg.alt = mainImg.alt;
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

  gallery.addEventListener('mousemove', (e) => {
    const rect = gallery.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    mainImg.style.transformOrigin = `${x}% ${y}%`;
    mainImg.style.transform = 'scale(1.5)';
  });

  gallery.addEventListener('mouseleave', () => {
    mainImg.style.transform = 'scale(1)';
  });

  if (zoomBtn) zoomBtn.addEventListener('click', openLightbox);
  gallery.addEventListener('click', openLightbox);

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
})();
