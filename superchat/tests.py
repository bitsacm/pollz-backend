from django.test import TestCase, Client
from django.urls import reverse
from .views import chat_view, send_message, chat_history

class ChatViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_chat_view_get(self):
        response = self.client.get(reverse('chat_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superchat/chat.html')

    def test_send_message_post(self):
        data = {'message': 'Hello, world!'}
        response = self.client.post(reverse('send_message'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])

    def test_chat_history_get(self):
        response = self.client.get(reverse('chat_history'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])