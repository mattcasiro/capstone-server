from rest_framework import serializers

from cloudstorage.models import File


class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = File
        fields = ('id', 'name', 'original_name', 'size', 'mime_type', 'created', 'modified', 'folder', 'file', 'owner')
        read_only_fields = ('id', 'original_name', 'size', 'mime_type', 'created', 'modified', 'folder', 'owner')

    def create(self, validated_data):
        file = File()
        file.name = validated_data['name']
        file.original_name = validated_data['name']
        file.size = 1234
        file.mime_type = 'image/jpeg'
        file.folder = validated_data['folder']
        file.file = validated_data['file']
        file.owner = validated_data['owner']
        file.save()
        return file

    #TODO: implement this - maybe name & folder
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.folder = validated_data.get('folder', instance.folder)
        instance.save()
        return instance
