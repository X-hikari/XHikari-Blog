from django.urls import path
from . import views

urlpatterns = [
    path('homenumber/', views.HomeNumberList.as_view(), name='home-number'),
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('categorys/', views.CategoryList.as_view(), name='category-list'),
    path('article/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('category/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('albums/', views.AlbumList.as_view(), name='album-list'),
    path('albumPhotos/', views.AlbumDetailView.as_view(), name='album-photo'),
    path('emotions/', views.EmotionList.as_view(), name='emotion-list'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('addmessage/', views.AddMessage.as_view(), name='add-message'),
    path('about/', views.AboutDetail.as_view(), name='about')
]
