from django.urls import path
from . import admin_views

urlpatterns = [
    path('searchArticle/', admin_views.ArticleList.as_view(), name='search-article'),
    path('articleContent/', admin_views.ArticleContentView.as_view(), name='article-content'),
    path('categoryWithArticles/', admin_views.CategoryWithArticlesView.as_view(), name='category-articles'),
    path('categoriesoutsub/', admin_views.CategoriesOutSubView.as_view(), name='category-without-sub'),
    path('upload/', admin_views.UploadImage.as_view(), name='upload-image'),
    path('addArticle/', admin_views.AddArticle.as_view(), name='add-article'),
    path('deleteArticles/', admin_views.DeleteArticles.as_view(), name='delete-article'),
    path('updateArticleContent/', admin_views.UpdateArticleContent.as_view(), name='update-article-content'),
    path('updateArticleBase/', admin_views.UpdateArticleBase.as_view(), name = 'update-article-base'),
    path('addMedia/', admin_views.AddMedia.as_view(), name='add-media'),
    path('serachCategory/', admin_views.CategoryList.as_view(), name='serach-category'),
    path('categoryName/', admin_views.CategoryName.as_view(), name='category-name'),
    path('addCategory/', admin_views.AddCategory.as_view(), name='add-category'),
    path('deleteCategories/', admin_views.DeleteCategories.as_view(), name='delete-category'),
    path('updateCategory/', admin_views.UpdateCategory.as_view(), name='update-category')
]