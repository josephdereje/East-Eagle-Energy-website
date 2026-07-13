from unittest.mock import patch

from django.test import Client, TestCase

from contact.models import SupportChatMessage, SupportChatSession


class SupportChatTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def _csrf(self):
        response = self.client.get('/')
        token = response.cookies.get('csrftoken')
        self.assertIsNotNone(token)
        return token.value

    @patch('contact.views.send_support_chat_email')
    def test_chat_start_and_send(self, mock_email):
        csrf = self._csrf()
        start = self.client.post(
            '/contact/chat/start/',
            {
                'email': 'visitor@example.com',
                'name': 'Test User',
                'page_url': 'https://example.com/products/',
            },
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(start.status_code, 200)
        payload = start.json()
        self.assertTrue(payload['ok'])
        session_id = payload['session_id']
        self.assertEqual(SupportChatSession.objects.count(), 1)
        self.assertEqual(SupportChatMessage.objects.filter(role='bot').count(), 1)

        send = self.client.post(
            '/contact/chat/send/',
            {
                'session_id': session_id,
                'message': 'Do you have 5kW inverters?',
            },
            HTTP_X_CSRFTOKEN=csrf,
        )
        self.assertEqual(send.status_code, 200)
        send_payload = send.json()
        self.assertTrue(send_payload['ok'])
        self.assertTrue(send_payload['email_sent'])
        mock_email.assert_called_once()
        self.assertEqual(
            SupportChatMessage.objects.filter(session_id=session_id, role='user').count(),
            1,
        )

    def test_chat_history(self):
        session = SupportChatSession.objects.create(
            email='history@example.com',
            name='History',
        )
        SupportChatMessage.objects.create(
            session=session,
            role=SupportChatMessage.ROLE_BOT,
            body='Welcome',
        )
        response = self.client.get(f'/contact/chat/history/{session.pk}/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['ok'])
        self.assertEqual(len(payload['messages']), 1)
