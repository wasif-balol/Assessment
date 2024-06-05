from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='passw123', first_name='Test',
                                             last_name='User')
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')

    def test_register_user(self):
        data = {'username': 'newuser', 'password': 'passw123', 'first_name': 'New', 'last_name': 'User'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'passw123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_token(self):
        data = {'username': 'testuser', 'password': 'passw123'}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_token(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
