from rest_framework import serializers
from .models import Comment
from apps.blogauth.models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'telephone', 'username', 'is_staff', 'email', 'is_active']


class CommentSerializers(serializers.ModelSerializer):
    author = userSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'pub_time', 'author']
