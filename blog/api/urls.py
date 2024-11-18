from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('categorys/', views.CategoryList.as_view(), name='category-list'),
    path('article/', views.ArticleDetailView.as_view(), name='article_detail'),
]