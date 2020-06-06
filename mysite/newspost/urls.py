from django.urls import path
from . import views

urlpatterns = [
    path('insertNews/', views.insertNews, name='insertNews'),
]