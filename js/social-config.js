/**
 * East Eagle Energy — Social Media Links
 * Update these URLs with your real profile links.
 * Leave empty ('') to hide an icon automatically.
 */
const SOCIAL_LINKS = [
  {
    name: 'Facebook',
    icon: 'fab fa-facebook-f',
    url: 'https://www.facebook.com/'
  },
  {
    name: 'Instagram',
    icon: 'fab fa-instagram',
    url: 'https://www.instagram.com/'
  },
  {
    name: 'LinkedIn',
    icon: 'fab fa-linkedin-in',
    url: 'https://www.linkedin.com/'
  },
  {
    name: 'X (Twitter)',
    icon: 'fab fa-x-twitter',
    url: 'https://x.com/'
  },
  {
    name: 'YouTube',
    icon: 'fab fa-youtube',
    url: 'https://www.youtube.com/'
  },
  {
    name: 'WhatsApp',
    icon: 'fab fa-whatsapp',
    url: 'https://wa.me/251933219802'
  }
];

function renderSocialLinks(container) {
  if (!container) return;

  const links = SOCIAL_LINKS.filter(item => item.url && item.url.trim() !== '');

  container.innerHTML = links.map(item => `
    <a href="${item.url}"
       target="_blank"
       rel="noopener noreferrer"
       aria-label="${item.name}"
       title="${item.name}">
      <i class="${item.icon}"></i>
    </a>
  `).join('');
}

document.querySelectorAll('[data-social-links]').forEach(renderSocialLinks);
