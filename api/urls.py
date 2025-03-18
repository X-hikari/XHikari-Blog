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
    path('about/', views.AboutDetail.as_view(), name='about'),
    path('searcharticles/', views.SearchArticles.as_view(), name='search-articles'),
    path('login/', views.Login.as_view(), name='login'),
    path('check_login/', views.check_login, name='check_login'),  # 检查登录状态的 API 路由
]
