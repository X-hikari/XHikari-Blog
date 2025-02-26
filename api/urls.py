from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('categorys/', views.CategoryList.as_view(), name='category-list'),
    path('article/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('category/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('albums/', views.AlbumList.as_view(), name='album-list')
]
