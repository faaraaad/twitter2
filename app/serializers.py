from rest_framework import serializers
from .models import Post, CustomUser


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ['body']#, 'author']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]