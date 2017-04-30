from django.test import TestCase
from cloudstorage.models import File
from django.core.files.uploadedfile import SimpleUploadedFile
import mimetypes

class TestFile(TestCase):

    def test_mime_type(self):
        test_file = File()
        test_file.file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        test_file.set_mime_type()

        self.assertEqual(test_file.mime_type, 'image/jpeg')

    def test_file_size(self):
        test_file = File()
        test_file.file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        test_file.set_file_size()

        self.assertEqual(test_file.size, 12)
