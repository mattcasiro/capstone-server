from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from cloudstorage.models import StorageUser, Folder, File


class FileRedirectTests(APITestCase):

    def setUp(self):
        user = StorageUser()
        user.email = 'test@test.com'
        user.first_name = 'derek'
        user.last_name = 'shephard'
        user.set_password('password')
        user.save()
        self.user = user

        folder = Folder()
        folder.name = "test"
        folder.owner = user
        folder.save()
        self.folder = folder

        file = File()
        file.name = "boop.jpg"
        file.original_name = "boop.jpg"
        file.size = 123
        file.mime_type = "img/jpg"
        file.folder = folder
        file.owner = user
        file.file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        file.save()
        self.file = file

    def test_get_file_redirect(self):
        url = '/api/folders/{}/files/{}/file/'.format(self.folder.id, self.file.id)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.file.file.url)

    def test_not_authenticated_file_redirect(self):
        url = '/api/folders/{}/files/{}/file/'.format(self.folder.id, self.file.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
