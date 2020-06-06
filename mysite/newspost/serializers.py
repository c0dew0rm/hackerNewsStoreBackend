from rest_framework import serializers
from .models import NewsPost

class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ['postId', 'author', 'datePosted', 'title', 'url', 'upvotes', 'commentCount', 'isDeleted']