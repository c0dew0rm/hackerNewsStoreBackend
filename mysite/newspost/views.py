from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Comment, NewsPost
import requests
import json
import time, datetime, pytz

from rest_framework import viewsets
from .serializers import NewsPostSerializer

# Create your views here.

def insertNews(request):
    payload = {}
    headers= {}
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.request("GET", url, headers=headers, data = payload)
    responseText = response.text[2:len(response.text)-2]
    newsPostList = responseText.split(', ')
    count = 0
    postList = []
    commentsPerPost = {}
    # Fething all the NewsPost's.
    # NewsPost.objects.all().delete()
    # Comment.objects.all().delete()
    for item in newsPostList:
        if(count<90):
            try:
                existingPost = NewsPost.objects.get(postId=item)
                fetchNewsApiUrl = "https://hacker-news.firebaseio.com/v0/item/"+item+".json?print=pretty"
                fetchNewsApiRes = requests.request("GET", fetchNewsApiUrl, headers=headers, data = payload)
                fetchNewsApiResJson = json.loads(fetchNewsApiRes.text)
                commentList = fetchNewsApiResJson['kids'] if fetchNewsApiResJson.get('kids') else []
                existingPost.upvotes = fetchNewsApiResJson.get('score')
                existingPost.commentCount = len(commentList)
                existingPost.save()
                print("updated post = ",item)
                # Update Logic
            except:
                # Insertion logic for new post.
                print("New Post = ",item)
                fetchNewsApiUrl = "https://hacker-news.firebaseio.com/v0/item/"+item+".json?print=pretty"
                fetchNewsApiRes = requests.request("GET", fetchNewsApiUrl, headers=headers, data = payload)
                fetchNewsApiResJson = json.loads(fetchNewsApiRes.text)
                dateTime = datetime.datetime.fromtimestamp(fetchNewsApiResJson.get('time'))
                dateTime = timezone.now()
                commentList = fetchNewsApiResJson['kids'] if fetchNewsApiResJson.get('kids') else []
                post = NewsPost(
                    author=fetchNewsApiResJson.get('by'),
                    postId=fetchNewsApiResJson.get('id'),
                    upvotes=fetchNewsApiResJson.get('score'),
                    datePosted=dateTime,
                    title=fetchNewsApiResJson.get('title'),
                    url=fetchNewsApiResJson.get('url'),
                    commentCount = len(commentList)
                )
                try:
                    post.save()
                except:
                    print("some error")
                # postList.append(post)
                commentsPerPost[fetchNewsApiResJson.get('id')] = fetchNewsApiResJson.get('kids')
            print(count)
            count+=1
        else :
            break
    # NewsPost.objects.bulk_create(postList)
    print("All News Inserted.")

    # commentList = []
    # # Fetching and storing related comments.
    # for postid,postComments in commentsPerPost.items():
    #     for commentId in postComments:
    #         print("postid -->>",postid,"commentid -->>",commentId)
    #         fetchCommentApiUrl = "https://hacker-news.firebaseio.com/v0/item/"+str(commentId)+".json?print=pretty"
    #         fetchCommentApiRes = requests.request("GET", fetchCommentApiUrl, headers=headers, data = payload)
    #         fetchCommentApiResJson = json.loads(fetchCommentApiRes.text)
    #         dateTime = datetime.datetime.fromtimestamp(fetchCommentApiResJson.get('time'))
    #         dateTime = timezone.now()
    #         # print(fetchCommentApiResJson)
    #         # print("\n\n\n\n")
    #         post = NewsPost.objects.get(postId=postid)
    #         comment = Comment(
    #             post = post,
    #             author = fetchCommentApiResJson.get('by'),
    #             commentId = fetchCommentApiResJson.get('id'),
    #             comment = fetchCommentApiResJson.get('text'),
    #             commentTime = dateTime,
    #         )
    #         commentList.append(comment)
    # Comment.objects.bulk_create(commentList)
    # print("Comments Inserted")
    return HttpResponse(status=204)

class NewsPostViewSet(viewsets.ModelViewSet):
    queryset = NewsPost.objects.all().order_by('-datePosted')
    serializer_class = NewsPostSerializer
