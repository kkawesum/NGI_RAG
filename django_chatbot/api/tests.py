from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from chatbot.models import Chat
from django.utils import timezone

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.csrf_url = reverse('get_csrf_token')
        self.hello_world_url = reverse('hello_world')

    def test_get_csrf_token(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrfToken', response.json())

    @patch('chatbot.utils.generate_rag_response')
    def test_hello_world_post(self, mock_generate_response):
        self.client.login(username='testuser', password='password')
        mock_generate_response.return_value = 'Mocked Response'
        response = self.client.post(self.hello_world_url, {'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response'], 'Mocked Response')
        self.assertTrue(Chat.objects.filter(user=self.user, message='Hello').exists())

    def test_hello_world_get(self):
        response = self.client.get(self.hello_world_url)
        self.assertEqual(response.status_code, 200)
