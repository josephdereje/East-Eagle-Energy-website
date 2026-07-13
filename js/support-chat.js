/**
 * East Eagle Energy — corner support chat (email login + tech team messages).
 */
(function () {
  const STORAGE_KEY = 'eee_support_chat_session';
  const STORAGE_EMAIL = 'eee_support_chat_email';
  const STORAGE_NAME = 'eee_support_chat_name';

  const panel = document.getElementById('supportChatPanel');
  const fab = document.getElementById('supportChatFab');
  const closeBtn = document.getElementById('supportChatClose');
  const loginWrap = document.getElementById('supportChatLogin');
  const loginForm = document.getElementById('supportChatLoginForm');
  const bodyWrap = document.getElementById('supportChatBody');
  const messagesEl = document.getElementById('supportChatMessages');
  const composeForm = document.getElementById('supportChatComposeForm');
  const inputEl = document.getElementById('supportChatInput');
  const statusEl = document.getElementById('supportChatStatus');
  const userLabel = document.getElementById('supportChatUserLabel');
  const signOutBtn = document.getElementById('supportChatSignOut');

  if (!panel || !fab) return;

  let sessionId = localStorage.getItem(STORAGE_KEY) || '';
  let isOpen = false;
  let isSending = false;

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : '';
  }

  function setStatus(text, isError) {
    if (!statusEl) return;
    statusEl.textContent = text || '';
    statusEl.classList.toggle('is-error', Boolean(isError));
  }

  function formatTime(iso) {
    try {
      const d = new Date(iso);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return '';
    }
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
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
    loginWrap.hidden = false;
    bodyWrap.hidden = true;
    setStatus('');
  }

  function showChatView(email, name) {
    loginWrap.hidden = true;
    bodyWrap.hidden = false;
    const label = name ? `${name} · ${email}` : email;
    if (userLabel) userLabel.textContent = label;
  }

  function openPanel() {
    isOpen = true;
    panel.classList.add('is-open');
    panel.setAttribute('aria-hidden', 'false');
    fab.setAttribute('aria-expanded', 'true');
    fab.classList.add('is-active');
    if (loginWrap.hidden === false) {
      const emailInput = loginForm?.querySelector('[name="email"]');
      emailInput?.focus();
    } else {
      inputEl?.focus();
    }
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('is-open');
    panel.setAttribute('aria-hidden', 'true');
    fab.setAttribute('aria-expanded', 'false');
    fab.classList.remove('is-active');
    setStatus('');
  }

  async function apiPost(url, data) {
    const body = new URLSearchParams(data);
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: body.toString(),
      credentials: 'same-origin',
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !payload.ok) {
      const err = payload.errors ? JSON.stringify(payload.errors) : 'Request failed';
      throw new Error(err);
    }
    return payload;
  }

  async function apiGet(url) {
    const response = await fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      credentials: 'same-origin',
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || !payload.ok) {
      throw new Error('Could not load chat history');
    }
    return payload;
  }

  async function startSession(email, name) {
    const payload = await apiPost('/contact/chat/start/', {
      email,
      name: name || '',
      page_url: window.location.href,
    });
    sessionId = payload.session_id;
    localStorage.setItem(STORAGE_KEY, sessionId);
    localStorage.setItem(STORAGE_EMAIL, email);
    localStorage.setItem(STORAGE_NAME, name || '');
    showChatView(email, name);
    renderMessages(payload.messages);
    setStatus('');
  }

  async function loadSession() {
    const email = localStorage.getItem(STORAGE_EMAIL) || '';
    const name = localStorage.getItem(STORAGE_NAME) || '';
    if (!sessionId) {
      showLoginView();
      if (email && loginForm) {
        loginForm.email.value = email;
        if (name) loginForm.name.value = name;
      }
      return;
    }

    try {
      const payload = await apiGet(`/contact/chat/history/${sessionId}/`);
      sessionId = payload.session_id;
      showChatView(payload.email, payload.name);
      renderMessages(payload.messages);
    } catch (e) {
      sessionId = '';
      localStorage.removeItem(STORAGE_KEY);
      showLoginView();
    }
  }

  async function sendMessage(text) {
    if (!sessionId || isSending) return;
    isSending = true;
    setStatus('Sending...');
    composeForm?.classList.add('is-sending');

    try {
      const payload = await apiPost('/contact/chat/send/', {
        session_id: sessionId,
        message: text,
      });
      const existing = messagesEl?.querySelectorAll('.support-chat-bubble').length || 0;
      const history = await apiGet(`/contact/chat/history/${sessionId}/`);
      renderMessages(history.messages);
      if (!payload.email_sent) {
        setStatus('Message saved. Email notification may be delayed.', true);
      } else {
        setStatus('');
      }
      if (inputEl) inputEl.value = '';
    } catch (e) {
      setStatus('Could not send. Please try again.', true);
    } finally {
      isSending = false;
      composeForm?.classList.remove('is-sending');
    }
  }

  fab.addEventListener('click', () => {
    if (isOpen) closePanel();
    else openPanel();
  });

  closeBtn?.addEventListener('click', closePanel);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isOpen) closePanel();
  });

  loginForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = loginForm.email.value.trim();
    const name = loginForm.name.value.trim();
    if (!email) {
      setStatus('Please enter your email.', true);
      return;
    }
    setStatus('Starting chat...');
    try {
      await startSession(email, name);
      openPanel();
    } catch (e) {
      setStatus('Could not start chat. Please try again.', true);
    }
  });

  composeForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = inputEl?.value.trim();
    if (!text) return;
    await sendMessage(text);
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
    showLoginView();
    if (messagesEl) messagesEl.innerHTML = '';
    setStatus('');
  });

  loadSession();
})();
