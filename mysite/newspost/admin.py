from django.contrib import admin
from .models import (
    NewsPost,
    Comment,
    UserInfo,
)
# Register your models here.

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('postId', 'author', 'datePosted', 'title', 'url', 'upvotes', 'commentCount', 'isDeleted')

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    def postTitle(self, obj):
        return obj.post.title

    list_display = ('commentId', 'author', 'comment', 'commentTime', 'postTitle')

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userName', 'userEmail', 'password')