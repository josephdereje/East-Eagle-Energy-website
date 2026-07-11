/**
 * Product catalog — browse filters/tabs/pages without full reload.
 */
(function () {
  const root = document.querySelector('.products-page.dyness-layout');
  if (!root) return;

  const sidebarNav = document.getElementById('catalogSidebarNav');
  const titleEl = document.getElementById('catalogPageTitle');
  const countEl = document.getElementById('catalogPageCount');
  const scrollEl = document.getElementById('productGrid');

  let loading = false;

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function ajaxUrl(url) {
    const u = new URL(url, window.location.origin);
    u.searchParams.set('ajax', '1');
    return u.pathname + u.search;
  }

  function withPage(url, page) {
    const u = new URL(url, window.location.origin);
    if (page && page > 1) u.searchParams.set('page', String(page));
    else u.searchParams.delete('page');
    u.searchParams.delete('ajax');
    return u.pathname + u.search;
  }

  function renderSidebar(navGroups, activeFilter) {
    if (!sidebarNav) return;
    sidebarNav.innerHTML = (navGroups || []).map((group) => {
      const items = (group.items || []).map((item) => {
        const active = item.filter_key === activeFilter ? ' active' : '';
        const sub = item.is_sub ? ' dyness-nav-link--sub' : '';
        const count = item.count
          ? `<span class="nav-count">${escapeHtml(item.count)}</span>`
          : '';
        return (
          `<a href="${escapeHtml(item.url)}" class="dyness-nav-link${sub}${active}" data-catalog-nav>` +
          `${escapeHtml(item.label)}${count}</a>`
        );
      }).join('');

      return (
        `<div class="dyness-nav-group">` +
        `<div class="dyness-nav-group-header">` +
        `<i class="fa ${escapeHtml(group.icon || '')}"></i>` +
        `<span>${escapeHtml(group.title)}</span>` +
        `</div>` +
        `<nav class="dyness-nav-items">${items}</nav>` +
        `</div>`
      );
    }).join('');
  }

  function renderProducts(products) {
    if (!products || !products.length) {
      return (
        `<div class="dyness-empty">` +
        `<i class="fa fa-box-open"></i>` +
        `<h3>No products found</h3>` +
        `<p>Try a different category or <a href="/products/search/">search our catalog</a>.</p>` +
        `</div>`
      );
    }

    return products.map((p) => {
      const media = p.image_url
        ? `<img src="${escapeHtml(p.image_url)}" alt="${escapeHtml(p.name)}">`
        : `<div class="dyness-product-placeholder"><i class="fa ${escapeHtml(p.icon)}"></i></div>`;

      let tags = `<span class="dyness-tag ${escapeHtml(p.type_class)}">${escapeHtml(p.type_label)}</span>`;
      if (p.voltage_label) {
        tags += `<span class="dyness-tag">${escapeHtml(p.voltage_label)}</span>`;
      }
      if (p.ess_sub_type_label) {
        tags += `<span class="dyness-tag">${escapeHtml(p.ess_sub_type_label)}</span>`;
      }

      return (
        `<a href="${escapeHtml(p.url)}" class="dyness-product-card">` +
        `<div class="dyness-product-image">${media}</div>` +
        `<div class="dyness-product-info">` +
        `<h3>${escapeHtml(p.name)}</h3>` +
        `<p class="dyness-product-spec">${escapeHtml(p.short_description)}</p>` +
        `<div class="dyness-product-tags">${tags}</div>` +
        `</div>` +
        `<div class="dyness-card-accent"></div>` +
        `</a>`
      );
    }).join('');
  }

  function renderPager(pagination, basePath, totalProducts) {
    if (!pagination || pagination.num_pages <= 1) return '';

    const prev = pagination.has_previous
      ? `<a class="product-pager-btn" href="${escapeHtml(withPage(basePath, pagination.previous_page))}" data-catalog-page aria-label="Previous page"><i class="fa fa-arrow-left"></i></a>`
      : `<span class="product-pager-btn is-disabled" aria-disabled="true"><i class="fa fa-arrow-left"></i></span>`;

    const next = pagination.has_next
      ? `<a class="product-pager-btn" href="${escapeHtml(withPage(basePath, pagination.next_page))}" data-catalog-page aria-label="Next page"><i class="fa fa-arrow-right"></i></a>`
      : `<span class="product-pager-btn is-disabled" aria-disabled="true"><i class="fa fa-arrow-right"></i></span>`;

    const pages = (pagination.page_range || []).map((num) => {
      if (num === pagination.page) {
        return (
          `<span class="product-pager-page is-active" aria-current="page">` +
          `<span class="product-pager-page-label">Page</span>${num}</span>`
        );
      }
      return (
        `<a class="product-pager-page" href="${escapeHtml(withPage(basePath, num))}" data-catalog-page>` +
        `<span class="product-pager-page-label">Page</span>${num}</a>`
      );
    }).join('');

    return (
      `<nav class="product-pager" aria-label="Product pages">` +
      `<div class="product-pager-track">${prev}<div class="product-pager-pages">${pages}</div>${next}</div>` +
      `<p class="product-pager-note">Showing ${escapeHtml(pagination.showing)} of ${escapeHtml(totalProducts)} · 12 per page</p>` +
      `</nav>`
    );
  }

  function updateTabs(activeSection) {
    root.querySelectorAll('.product-section-tabs .section-tab').forEach((tab) => {
      tab.classList.toggle('active', tab.getAttribute('data-section') === activeSection);
    });
  }

  function updateCount(total, pagination) {
    if (!countEl) return;
    if (!total) {
      countEl.textContent = '0 products';
      return;
    }
    let text = `${total} product${total === 1 ? '' : 's'}`;
    if (pagination && pagination.num_pages > 1) {
      text += ` · Page ${pagination.page} / ${pagination.num_pages}`;
    }
    countEl.textContent = text;
  }

  async function loadCatalog(url, { push = true } = {}) {
    if (loading) return;
    loading = true;
    root.classList.add('is-catalog-loading');

    try {
      const response = await fetch(ajaxUrl(url), {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          Accept: 'application/json',
        },
      });
      if (!response.ok) throw new Error('Catalog request failed');
      const data = await response.json();
      if (!data.ok) throw new Error('Invalid catalog response');

      const parsed = new URL(url, window.location.href);
      parsed.searchParams.delete('ajax');
      const publicUrl = parsed.pathname + parsed.search;

      if (titleEl) titleEl.textContent = data.page_title || '';
      updateCount(data.total_products, data.pagination);
      updateTabs(data.active_section);
      renderSidebar(data.nav_groups, data.active_filter);

      if (scrollEl) {
        scrollEl.innerHTML =
          `<div class="dyness-product-grid">${renderProducts(data.products)}</div>` +
          renderPager(data.pagination, publicUrl, data.total_products);
        scrollEl.scrollTop = 0;
      }

      if (data.seo_title) document.title = data.seo_title;
      if (push) history.pushState({ catalog: true }, '', publicUrl);
    } catch (err) {
      window.location.href = url;
      return;
    } finally {
      loading = false;
      root.classList.remove('is-catalog-loading');
    }
  }

  root.addEventListener('click', (event) => {
    const link = event.target.closest(
      'a.section-tab[data-catalog-nav], a.dyness-nav-link[data-catalog-nav], a[data-catalog-page]'
    );
    if (!link || !root.contains(link)) return;
    if (link.target === '_blank' || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }

    const href = link.getAttribute('href');
    if (!href || href.startsWith('#')) return;

    event.preventDefault();
    loadCatalog(href, { push: true });
  });

  window.addEventListener('popstate', () => {
    if (!window.location.pathname.startsWith('/products')) return;
    if (window.location.pathname.includes('/search')) return;
    // Ignore product detail pages
    const parts = window.location.pathname.replace(/\/+$/, '').split('/');
    if (
      parts.length === 3 &&
      !['ess', 'inverters', 'solar-panels', 'ev-chargers', 'category'].includes(parts[2])
    ) {
      return;
    }
    loadCatalog(window.location.pathname + window.location.search, { push: false });
  });
})();
