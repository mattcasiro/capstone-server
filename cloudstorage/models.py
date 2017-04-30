import mimetypes

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

# User = get_user_model()


class MyUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class StorageUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def save(self, *args, **kwargs):
        # check if user has ID, if not they are a new user and need a root folder
        # created on their account
        is_new_user = False if self.id else True

        super().save(*args, **kwargs)

        # create the root folder
        if is_new_user:
            folder = Folder()
            folder.name = "root"
            folder.owner = self
            folder.save()

    def __str__(self):
        return self.email


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
    original_name = models.CharField(max_length=250)
    size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey(Folder, related_name='files') # get with Folder.files.all()
    file = models.FileField(upload_to=get_file_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def set_mime_type(self):
        mimetype, encoding = mimetypes.guess_type(self.file.name)
        self.mime_type = mimetype

    def set_file_size(self):
        self.size = self.file.size
