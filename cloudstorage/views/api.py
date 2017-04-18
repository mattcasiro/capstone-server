# from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, mixins

# Serializers define the API representation.
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cloudstorage.models import File, Folder, StorageUser
from cloudstorage.serializers import FolderSerializer, FileSerializer, UserSerializer, UserProfileSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = StorageUser.objects.all()
    serializer_class = UserSerializer


class ProfileView(APIView):

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class FolderAPIView(GenericAPIView):
    """
    Base folder API class so we don't have to repeat ourselves
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self):
        """
        Filter queryset by owner = requesting user (eg. adds 'where' clause to query)
        Now you can only see your own folders :)
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class FolderListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, FolderAPIView):
    """
    URL eg. /api/folders/
    GET: Displays a list of folders for the requesting user
    POST: Creates a new folder for the requesting user
    """
    def get(self, request):
        return self.list(request=request)

    def post(self, request):
        return self.create(request=request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FolderDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, FolderAPIView):
    """
    URL eg. /api/folders/:id/
    GET: Displays a single folder's details
    PUT: Updates a folder's details
    DELETE: Deletes a folder 
    """
    lookup_field = 'id'
    lookup_url_kwarg = 'folder_id'

    def get(self, request, folder_id):
        return self.retrieve(request=request, folder_id=folder_id)

    def put(self, request, folder_id):
        return self.update(request=request, folder_id=folder_id)

    def delete(self, request, folder_id):
        return self.destroy(request=request, folder_id=folder_id)


class FileAPIView(GenericAPIView):
    """
    Base file API class so we don't have to repeat ourselves
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        """
        Filter queryset by folder
        """
        folder = self.get_folder()
        queryset = super().get_queryset()
        queryset = queryset.filter(folder=folder)
        return queryset

    def get_folder(self):
        """
        Returns and instance of a folder with a given id, owned by the requesting user.
        If the folder doesn't exist, raises a Http404 error
        """
        queryset = Folder.objects.all()
        return get_object_or_404(queryset, owner=self.request.user,
                                 id=self.kwargs['folder_id'])


class FileListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, FileAPIView):
    """
    URL eg. /api/folders/:id/files/
    GET: Displays a list of files in the specified folder for the requesting user
    POST: Creates a new file in the specified folder owned by the requesting user
    """
    def get(self, request, folder_id):
        return self.list(request=request, folder_id=folder_id)

    def post(self, request, folder_id):
        return self.create(request=request, folder_id=folder_id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, folder=self.get_folder())


class FileDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,FileAPIView):
    """
    URL eg. /api/folders/:id/files/:id/
    GET: Displays a single file's details
    PUT: Updates a file's details
    DELETE: Deletes a file 
    """

    lookup_field = 'id'
    lookup_url_kwarg = 'file_id'

    def get(self, request, folder_id, file_id):
        return self.retrieve(request=request, folder_id=folder_id, file_id=file_id)

    def put(self, request, folder_id, file_id):
        # raise NotImplementedError("Implement me")
        return self.update(request=request, folder_id=folder_id, file_id=file_id)

    def delete(self, request, folder_id, file_id):
        return self.destroy(request=request, folder_id=folder_id, file_id=file_id)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
