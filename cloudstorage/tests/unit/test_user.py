from django.test import TestCase
from cloudstorage.models import StorageUser, Folder
from django.core.files.uploadedfile import SimpleUploadedFile
import mimetypes


class TestUser(TestCase):

    # test when they create a new user that they have a root folder
    # test when they save again they don't get another root folder

    def test_user_root_folder_created_on_first_save(self):
        user = StorageUser()
        user.email = 'test@test.com'
        user.first_name = 'derek'
        user.last_name = 'shephard'
        user.set_password('password')
        user.save()

        folder = Folder.objects.get(owner=user, parent=None)
        self.assertEqual(folder.name, 'root')

        user.save()
        self.assertEqual(Folder.objects.count(), 1)
