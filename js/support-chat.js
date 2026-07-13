/**
 * East Eagle Energy — simple email login → service bot chat.
 */
(function () {
  const STORAGE_KEY = 'eee_support_chat_session';
  const STORAGE_EMAIL = 'eee_support_chat_email';

  const panel = document.getElementById('supportChatPanel');
  const backdrop = document.getElementById('supportChatBackdrop');
  const fab = document.getElementById('supportChatFab');
  const closeBtn = document.getElementById('supportChatClose');
  const loginView = document.getElementById('supportChatLogin');
  const loginForm = document.getElementById('supportChatLoginForm');
  const emailInput = document.getElementById('supportChatEmail');
  const emailError = document.getElementById('supportChatEmailError');
  const chatView = document.getElementById('supportChatBody');
  const messagesEl = document.getElementById('supportChatMessages');
  const composeForm = document.getElementById('supportChatComposeForm');
  const inputEl = document.getElementById('supportChatInput');
  const statusEl = document.getElementById('supportChatStatus');
  const subtitleEl = document.getElementById('supportChatSubtitle');
  const signOutBtn = document.getElementById('supportChatSignOut');
  const startBtn = document.getElementById('supportChatStartBtn');

  if (!panel || !fab) return;

  let sessionId = localStorage.getItem(STORAGE_KEY) || '';
  let isOpen = false;
  let isSending = false;
  let chatScrollY = 0;

  function isMobileChat() {
    return window.matchMedia('(max-width: 991px)').matches;
  }

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : '';
  }

  function setStatus(text, isError) {
    if (!statusEl) return;
    statusEl.textContent = text || '';
    statusEl.classList.toggle('is-error', Boolean(isError));
  }

  function setEmailError(text) {
    if (emailError) emailError.textContent = text || '';
  }

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatTime(iso) {
    try {
      return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return '';
    }
  }

  function renderMessages(messages) {
    if (!messagesEl) return;
    messagesEl.innerHTML = (messages || []).map((msg) => {
      const roleClass = msg.role === 'user' ? 'is-user' : 'is-bot';
      return (
        `<div class="support-chat-bubble ${roleClass}">` +
        `<p>${escapeHtml(msg.body)}</p>` +
        `<time datetime="${escapeHtml(msg.created_at)}">${formatTime(msg.created_at)}</time>` +
        `</div>`
      );
    }).join('');
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function showLoginView() {
    loginView.hidden = false;
    loginView.classList.add('is-active');
    chatView.hidden = true;
    chatView.classList.remove('is-active');
    if (subtitleEl) subtitleEl.textContent = 'East Eagle Energy · Technical help';
    setStatus('');
    setEmailError('');
  }

  function showChatView(email) {
    loginView.hidden = true;
    loginView.classList.remove('is-active');
    chatView.hidden = false;
    chatView.classList.add('is-active');
    if (subtitleEl) subtitleEl.textContent = email;
    setStatus('');
    setEmailError('');
  }

  function lockBodyScroll() {
    if (!isMobileChat()) return;
    chatScrollY = window.scrollY || 0;
    document.body.style.top = `-${chatScrollY}px`;
    document.body.classList.add('support-chat-open');
  }

  function unlockBodyScroll() {
    if (!document.body.classList.contains('support-chat-open')) return;
    document.body.classList.remove('support-chat-open');
    document.body.style.top = '';
    window.scrollTo(0, chatScrollY);
  }

  function openPanel() {
    isOpen = true;
    panel.classList.add('is-open');
    panel.setAttribute('aria-hidden', 'false');
    fab.setAttribute('aria-expanded', 'true');
    fab.classList.add('is-active');
    backdrop?.setAttribute('aria-hidden', 'false');
    lockBodyScroll();
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('is-open');
    panel.setAttribute('aria-hidden', 'true');
    fab.setAttribute('aria-expanded', 'false');
    fab.classList.remove('is-active');
    backdrop?.setAttribute('aria-hidden', 'true');
    unlockBodyScroll();
    setStatus('');
    setEmailError('');
  }

  async function apiPost(url, data) {
    const csrf = getCookie('csrftoken');
    if (!csrf) throw new Error('Please refresh the page and try again.');

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrf,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: new URLSearchParams(data).toString(),
      credentials: 'same-origin',
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !payload.ok) throw new Error('Request failed');
    return payload;
  }

  async function apiGet(url) {
    const response = await fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      credentials: 'same-origin',
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !payload.ok) throw new Error('Could not load chat');
    return payload;
  }

  async function startSession(email) {
    const payload = await apiPost('/contact/chat/start/', {
      email,
      page_url: window.location.href,
    });
    sessionId = payload.session_id;
    localStorage.setItem(STORAGE_KEY, sessionId);
    localStorage.setItem(STORAGE_EMAIL, email);
    showChatView(email);
    renderMessages(payload.messages);
    setStatus('');
    if (inputEl) inputEl.focus();
  }

  async function loadSession() {
    const savedEmail = localStorage.getItem(STORAGE_EMAIL) || '';

    if (!sessionId) {
      showLoginView();
      if (savedEmail && emailInput) emailInput.value = savedEmail;
      return;
    }

    try {
      const payload = await apiGet(`/contact/chat/history/${sessionId}/`);
      sessionId = payload.session_id;
      showChatView(payload.email);
      renderMessages(payload.messages);
    } catch (e) {
      sessionId = '';
      localStorage.removeItem(STORAGE_KEY);
      showLoginView();
      if (savedEmail && emailInput) emailInput.value = savedEmail;
    }
  }

  async function sendMessage(text) {
    if (!sessionId) {
      showLoginView();
      setStatus('Enter your email to start chatting.', true);
      return;
    }
    if (isSending) return;

    isSending = true;
    composeForm?.classList.add('is-sending');

    try {
      const payload = await apiPost('/contact/chat/send/', {
        session_id: sessionId,
        message: text,
      });
      const history = await apiGet(`/contact/chat/history/${sessionId}/`);
      renderMessages(history.messages);
      if (inputEl) inputEl.value = '';
      if (!payload.email_sent) {
        setStatus('Saved — team email may be delayed.', true);
      } else {
        setStatus('');
      }
    } catch (e) {
      setStatus('Could not send. Try again.', true);
    } finally {
      isSending = false;
      composeForm?.classList.remove('is-sending');
    }
  }

  fab.addEventListener('click', () => {
    if (isOpen) {
      closePanel();
      return;
    }
    openPanel();
    if (!sessionId) {
      showLoginView();
      setTimeout(() => emailInput?.focus(), 200);
    } else {
      showChatView(localStorage.getItem(STORAGE_EMAIL) || '');
    }
  });

  closeBtn?.addEventListener('click', closePanel);
  backdrop?.addEventListener('click', closePanel);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isOpen) closePanel();
  });

  window.addEventListener('resize', () => {
    if (!isMobileChat()) unlockBodyScroll();
  });

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', () => {
      if (isOpen && isMobileChat()) {
        panel.style.setProperty('--chat-vv-height', `${window.visualViewport.height}px`);
      }
    });
  }

  loginForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = (emailInput?.value || '').trim();
    setEmailError('');

    if (!email) {
      setEmailError('Email is required.');
      return;
    }
    if (!isValidEmail(email)) {
      setEmailError('Please enter a valid email.');
      return;
    }

    startBtn?.setAttribute('disabled', 'disabled');
    setStatus('Starting chat...');

    try {
      await startSession(email);
    } catch (e) {
      setStatus('Could not start chat. Refresh and try again.', true);
    } finally {
      startBtn?.removeAttribute('disabled');
    }
  });

  composeForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = inputEl?.value.trim();
    if (text) await sendMessage(text);
  });

  inputEl?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      composeForm?.requestSubmit();
    }
  });

  signOutBtn?.addEventListener('click', () => {
    sessionId = '';
    localStorage.removeItem(STORAGE_KEY);
    const email = localStorage.getItem(STORAGE_EMAIL) || '';
    if (messagesEl) messagesEl.innerHTML = '';
    showLoginView();
    if (emailInput) emailInput.value = email;
  });

  loadSession();
})();
