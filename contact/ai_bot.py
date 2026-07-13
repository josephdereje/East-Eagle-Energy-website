"""
Optional AI service bot — OpenAI-compatible APIs (OpenRouter free Nemotron, NVIDIA NIM).

Set in .env when ready:
  CHAT_AI_ENABLED=True
  CHAT_AI_API_KEY=your-key
  CHAT_AI_BASE_URL=https://openrouter.ai/api/v1
  CHAT_AI_MODEL=nvidia/nemotron-3-super-120b-a12b:free

Or NVIDIA NIM:
  CHAT_AI_BASE_URL=https://integrate.api.nvidia.com/v1
  CHAT_AI_MODEL=nvidia/nemotron-3-super-120b-a12b
"""
import json
import logging
import os
import urllib.error
import urllib.request

from django.conf import settings

from .chat_utils import bot_reply_for_message

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    'You are the East Eagle Energy service bot. Help visitors with solar inverters, '
    'LiFePO4 batteries, ESS systems, solar panels, EV chargers, quotes, and installation. '
    'Be concise (2-4 sentences). Company phone: +251 93 321 9802. '
    'Email: info@easteagleenergy.com. Addis Ababa, Ethiopia. '
    'If unsure, say the technical team will follow up by email.'
)


def ai_enabled():
    return os.getenv('CHAT_AI_ENABLED', 'False').lower() == 'true'


def ai_configured():
    return bool(os.getenv('CHAT_AI_API_KEY', '').strip())


def get_bot_reply(session, user_text):
    """Return bot message — AI when configured, else keyword fallback."""
    if ai_enabled() and ai_configured():
        reply = _ai_reply(session, user_text)
        if reply:
            return reply
    return bot_reply_for_message(user_text)


def _ai_reply(session, user_text):
    api_key = os.getenv('CHAT_AI_API_KEY', '').strip()
    base_url = os.getenv(
        'CHAT_AI_BASE_URL',
        'https://openrouter.ai/api/v1',
    ).rstrip('/')
    model = os.getenv(
        'CHAT_AI_MODEL',
        'nvidia/nemotron-3-super-120b-a12b:free',
    )

    history = list(session.messages.order_by('created_at')[:12])
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    for msg in history:
        role = 'assistant' if msg.role == 'bot' else 'user'
        messages.append({'role': role, 'content': msg.body})
    messages.append({'role': 'user', 'content': user_text})

    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': int(os.getenv('CHAT_AI_MAX_TOKENS', '400')),
        'temperature': float(os.getenv('CHAT_AI_TEMPERATURE', '0.4')),
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    site_url = getattr(settings, 'ALLOWED_HOSTS', [''])[0]
    if site_url and site_url not in ('*', 'localhost', '127.0.0.1'):
        headers['HTTP-Referer'] = f'https://{site_url}'
        headers['X-Title'] = 'East Eagle Energy Support'

    request = urllib.request.Request(
        f'{base_url}/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode('utf-8'))
        content = data['choices'][0]['message']['content'].strip()
        return content[:2000] if content else None
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError, TimeoutError) as exc:
        logger.warning('Chat AI request failed: %s', exc)
        return None
