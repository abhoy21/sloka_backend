from rest_framework import serializers
from .models import User, Document


from rest_framework import serializers
from .models import User  # Assuming User is the model you're using

class UserSerializer(serializers.ModelSerializer):
    imageURL = serializers.URLField(allow_blank=True)  # Add imageURL field to the serializer

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'imageURL']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user




class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user', 'viewedit']
        extra_kwargs = {
            'content': {'allow_blank': True},
        }
        read_only_fields = ['created_at', 'updated_at', 'user' ]