from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, mixins

# Serializers define the API representation.
from rest_framework.generics import GenericAPIView, get_object_or_404

from cloudstorage.models import File, Folder


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'parent', 'id', 'owner', 'created', 'modified', 'tree_id')
        read_only_fields = ('id', 'owner', 'created', 'modified', 'tree_id')

    def validate_parent(self, value):
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError('Not your folder')
        return value

    def create(self, validated_data):
        folder = Folder()
        folder.name = validated_data['name']
        folder.parent = validated_data['parent']
        folder.owner = validated_data['user']
        folder.save()
        return folder

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.name = validated_data['name']

        if 'parent' in validated_data:
            instance.parent = validated_data['parent']

        instance.save()
        return instance


class FolderAPIView(GenericAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FolderListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, FolderAPIView):

    def get(self, request):
        return self.list(request=request)

    def post(self, request):
        return self.create(request=request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FolderDetailAPIView(mixins.RetrieveModelMixin, FolderAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'folder_id'

    def get(self, request, folder_id):
        return self.retrieve(request=request, folder_id=folder_id)


class FileAPIView(GenericAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        folder = self.get_folder()
        queryset = super().get_queryset()
        queryset = queryset.filter(location=folder)
        return queryset

    def get_folder(self):
        queryset = Folder.objects.all()
        return get_object_or_404(queryset, owner=self.request.user,
                                 id=self.kwargs['folder_id'])


class FileListAPIView(mixins.ListModelMixin, FileAPIView):

    def get(self, request, folder_id):
        return self.list(request=request, folder_id=folder_id)


class FileDetailAPIView(mixins.RetrieveModelMixin, FileAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'file_id'

    def get(self, request, folder_id, file_id):
        return self.retrieve(request=request, folder_id=folder_id, file_id=file_id)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
