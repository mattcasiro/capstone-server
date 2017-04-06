from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Folder(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self', null=True,
                            blank=True, related_name='children',
                            db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


def get_file_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class File(models.Model):
    name = models.CharField(max_length=250)
    size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Folder, related_name='files') # get with Folder.files.all()
    file = models.FileField(upload_to=get_file_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name