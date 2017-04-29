from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cloudstorage.models import StorageUser, Folder


class FolderAPITests(APITestCase):

    def setUp(self):
        user_1 = StorageUser()
        user_1.email = 'test_1@test.com'
        user_1.first_name = 'derek'
        user_1.last_name = 'shephard'
        user_1.set_password('password')
        user_1.save()
        self.user_1 = user_1

        user_2 = StorageUser()
        user_2.email = 'test_2@test.com'
        user_2.first_name = 'richard'
        user_2.last_name = 'jones'
        user_2.set_password('password')
        user_2.save()
        self.user_2 = user_2

        folder_root_1 = Folder()
        folder_root_1.name = 'user_1_root'
        folder_root_1.owner = user_1
        folder_root_1.save()
        self.folder_root_1 = folder_root_1

        folder_1 = Folder()
        folder_1.name = 'test_folder_1'
        folder_1.parent = folder_root_1
        folder_1.owner = user_1
        folder_1.save()
        self.folder_1 = folder_1

        folder_2 = Folder()
        folder_2.name = 'test_folder_2'
        folder_2.owner = user_2
        folder_2.save()
        self.folder_2 = folder_2

    def test_get_folder_list_not_authenticated(self):
        url = '/api/folders/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_folder_list_succcess(self):
        url = '/api/folders/'
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'user_1_root')
        self.assertEqual(response.data[0]['parent'], None)
        self.assertEqual(response.data[1]['name'], 'test_folder_1')
        self.assertEqual(response.data[1]['parent'], self.folder_root_1.id)

    def test_post_folder_list_not_authenticated(self):
        url = '/api/folders/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_folder_list_invalid_data(self):
        url = '/api/folders/'
        data = {'name': 'folder_3',
                'parent': 999}
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_folder_list_success(self):
        url = '/api/folders/'
        data = {'name': 'folder_3',
                'parent': self.folder_root_1.id,}
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'folder_3')
        self.assertEqual(response.data['parent'], self.folder_root_1.id)
        self.assertEqual(response.data['owner'], self.user_1.id)

