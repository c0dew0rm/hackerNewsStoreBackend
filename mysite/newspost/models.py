from django.db import models

# Create your models here.
class NewsPost(models.Model):
    author = models.CharField(null=True, max_length=500)   
    postId = models.IntegerField(primary_key=True)
    upvotes = models.IntegerField(default=0)
    datePosted = models.DateTimeField('date published')
    title = models.CharField(null=True, max_length=500)
    url = models.CharField(max_length=500, null=True, unique=True, default=None)
    commentCount = models.IntegerField(default=0, null=True)
    isDeleted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.postId)

class Comment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    author = models.CharField(null=True, max_length=500)
    commentId = models.IntegerField(primary_key=True)
    comment = models.TextField(null=True)
    commentTime = models.DateTimeField('date commented')

    def __str__(self):
        return str(self.commentId)

class UserInfo(models.Model):
    userName = models.CharField(null=False, max_length=20)
    userEmail = models.CharField(null=False, max_length=50)
    password = models.CharField(null=False, max_length=50)

    def __str__(self):
        return self.userName