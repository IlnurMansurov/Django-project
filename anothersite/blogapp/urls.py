from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
      ArticlesListView,
      ArticleDetailView,
      LatestArticlesField,
)
app_name = 'blogapp'
urlpatterns = [
    path('articles/', ArticlesListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticlesField(), name='articles-feed'),
]