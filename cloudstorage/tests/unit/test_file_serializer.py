from django.test import TestCase
from cloudstorage.serializers.file import FileSerializer
from cloudstorage.models import File, StorageUser, Folder
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
import mimetypes

class TestFileSerializer(TestCase):

    def setUp(self):

        self.sample_time = models.DateTimeField(auto_now=True)

        test_user = StorageUser()
        test_user.first_name = 'John'
        test_user.last_name = 'Doe'
        test_user.email = 'wat@no.way'
        test_user.is_active = True
        test_user.is_superuser = False
        test_user.save()
        self.test_user = test_user

        self.test_file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")

        test_folder = Folder()
        test_folder.name = 'home_folder'
        test_folder.owner = self.test_user
        test_folder.save()
        self.test_folder = test_folder


    def test_file_serializer(self):

        data = {'name': 'file.jpg', 'file': self.test_file } # 'folder': self.test_folder, 'owner': self.test_user}
        serializer = FileSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save(folder=self.test_folder, owner=self.test_user)

        saved_file = File.objects.all()[0]

        self.assertEqual(saved_file.name, 'file.jpg')

    def test_file_serializer_missing_folder(self):

        data = {'name': 'file.jpg', 'file': self.test_file }
        serializer = FileSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValueError):
            serializer.save(owner=self.test_user)

    def test_file_serializer_missing_owner(self):

        data = {'name': 'file.jpg', 'file': self.test_file }
        serializer = FileSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValueError):
            serializer.save(folder=self.test_folder)
