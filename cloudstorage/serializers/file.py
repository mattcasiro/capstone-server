from rest_framework import serializers
from django.core import exceptions
from cloudstorage.models import File


class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = File
        fields = ('id', 'name', 'original_name', 'size', 'mime_type', 'created', 'modified', 'folder', 'file', 'owner')
        read_only_fields = ('id', 'original_name', 'size', 'mime_type', 'created', 'modified', 'folder', 'owner')

    #TODO: get file size
    def create(self, validated_data):
        if 'folder' not in validated_data:
            raise ValueError('Must pass folder to validated_data')
        if 'owner' not in validated_data:
            raise ValueError('Must pass owner to validated_data')

        file = File()
        file.name = validated_data['name']
        file.original_name = validated_data['name']
        file.size = 1234
        file.folder = validated_data['folder']
        file.file = validated_data['file']
        file.owner = validated_data['owner']
        file.set_mime_type()
        file.save()
        return file

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.folder = validated_data.get('folder', instance.folder)
        #set 'modified' date?
        instance.save()
        return instance
