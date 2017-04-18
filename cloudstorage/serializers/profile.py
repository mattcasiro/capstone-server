from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
