from rest_framework import serializers

from cloudstorage.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'parent', 'id', 'owner', 'created', 'modified', 'tree_id')
        read_only_fields = ('id', 'owner', 'created', 'modified', 'tree_id')

    def validate_parent(self, value):
        """
        Check that parent is valid and is owned by requesting user.
        Refer to http://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        """
        request = self.context['request']

        # handle case for root folder
        if not value:
            return value

        # ensure new parent is owned by requesting user
        if value.owner != request.user:
            raise serializers.ValidationError('Not your folder')
        return value

    def create(self, validated_data):
        """
        Create folder using validated data (validated by serializer)
        """
        folder = Folder()
        folder.name = validated_data['name']
        folder.parent = validated_data['parent']
        folder.owner = validated_data['user']
        folder.save()
        return folder

    def update(self, instance, validated_data):
        """
        Update existing folder with validated data
        """
        if 'name' in validated_data:
            instance.name = validated_data['name']

        # Move folder to new parent folder
        if 'parent' in validated_data:
            instance.move_to(validated_data['parent'])

        instance.save()
        return instance
