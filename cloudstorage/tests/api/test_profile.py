from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cloudstorage.models import StorageUser

class ProfileViewTest(APITestCase):

    def setUp(self):
        user = StorageUser()
        user.email = 'test@test.com'
        user.first_name = 'derek'
        user.last_name = 'shephard'
        user.set_password('password')
        user.save()
        self.user = user

    def test_get_profile_not_authenticated(self):
        url = '/api/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile_success(self):
        url = '/api/profile/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'derek')
        self.assertEqual(response.data['last_name'], 'shephard')
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], 'test@test.com')

    def test_put_profile_success(self):
        url = '/api/profile/'
        self.client.force_authenticate(user=self.user)
        data = {'first_name': 'kered', 'last_name': 'drahpehs'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = StorageUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, data['first_name'])
        self.assertEqual(updated_user.last_name, data['last_name'])
