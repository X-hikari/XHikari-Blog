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
    path('searchMedias/', admin_views.MediaList.as_view(), name='search-media'),
    path('addMedia/', admin_views.AddMedia.as_view(), name='add-media'),
    path('updateMedia/', admin_views.UpdateMedia.as_view(), name='update-media'),
    path('deleteMedias/', admin_views.DeleteMedias.as_view(), name='delete-medias'),
    path('searchCategory/', admin_views.CategoryList.as_view(), name='search-category'),
    path('categoryName/', admin_views.CategoryName.as_view(), name='category-name'),
    path('addCategory/', admin_views.AddCategory.as_view(), name='add-category'),
    path('deleteCategories/', admin_views.DeleteCategories.as_view(), name='delete-category'),
    path('updateCategory/', admin_views.UpdateCategory.as_view(), name='update-category'),
    path('uploadAlbumPhoto/', admin_views.UploadPhoto.as_view(), name='upload-album'),
    path('searchAlbumPhotos/', admin_views.AlbumPhotoList.as_view(), name='album-photo'),
    path('updateAlbumPhoto/', admin_views.UpdateAlbumPhoto.as_view(), name='update-album-photo'),
    path('deleteAlbumPhotos/', admin_views.DeleteAlbumPhotos.as_view(), name='delete-album-photos'),
    path('searchAlbum/', admin_views.AlbumList.as_view(), name='search-album'),
    path('addAlbum/', admin_views.AddAlbum.as_view(), name='add-album'),
    path('updateAlbum/', admin_views.UpdateAlbum.as_view(), name='update-album'),
    path('deleteAlbums/', admin_views.DeleteAlbum.as_view(), name='delete-album'),
    path('searchEmotion/', admin_views.EmotionList.as_view(), name='search-emotion'),
    path('addEmotion/', admin_views.AddEmotion.as_view(), name='add-emotion'),
    path('deleteEmotions/', admin_views.DeleteEmotions.as_view(), name='delete-emotions'),
    path('addEmotionMedia/', admin_views.AddEmotionMedia.as_view(), name='add-emotion-media'),
    path('emotionDetail/', admin_views.EmotionDetail.as_view(), name='emotion-detail'),
    path('updateEmotion/', admin_views.UpdateEmotion.as_view(), name='update-emotion')
]