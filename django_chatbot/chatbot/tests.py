from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from .models import Chat

class ChatbotResponseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chatbot_url = reverse('chatbot_response')

    @patch('app.utils.generate_rag_response', return_value='Mocked Response')
    def test_chatbot_post_success(self, mock_generate_rag_response):
        """Test chatbot response with valid input"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.chatbot_url, {'messages': 'Hello'}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Hello', 'response': 'Mocked Response'})
        self.assertTrue(Chat.objects.filter(user=self.user, message='Hello').exists())

    def test_chatbot_post_unauthenticated(self):
        """Test chatbot response for unauthenticated user"""
        response = self.client.post(self.chatbot_url, {'messages': 'Hello'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Should still process since login is commented out
    
    def test_chatbot_post_no_message(self):
        """Test chatbot response when no message is sent"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.chatbot_url, {'messages': ''}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': '', 'response': 'Mocked Response'})
        
    def test_chatbot_get_request(self):
        """Test chatbot response on a GET request"""
        response = self.client.get(self.chatbot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbot.html')
    
    @patch('app.utils.generate_rag_response', side_effect=Exception("Mocked Error"))
    def test_chatbot_exception_handling(self, mock_generate_rag_response):
        """Test chatbot response when an exception occurs"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.chatbot_url, {'messages': 'Hello'}, follow=True)
        
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {'error': 'Something went wrong'})
