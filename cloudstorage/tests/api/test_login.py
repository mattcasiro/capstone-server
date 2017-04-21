from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cloudstorage.models import StorageUser


class LoginAPITests(APITestCase):

    def setUp(self):
        user = StorageUser()
        user.email = 'test@test.com'
        user.first_name = 'derek'
        user.last_name = 'shephard'
        user.set_password('password')
        user.save()
        self.user = user

    def test_login_success(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'email': 'test@test.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

    def test_login_cycles_token(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'email': 'test@test.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

        # LOGIN again to cycle token
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['token'], token.key)

    def test_wrong_password(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'email': 'test@test.com', 'password': 'incorrect'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_email(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'email': 'incorrect@test.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_password(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_credentials(self):
        """
        Ensure we can login
        """
        url = '/api/login/'
        data = {'boop': 'plumbus'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

