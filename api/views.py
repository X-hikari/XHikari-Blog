from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone
from .models import *
from .serializers import *
import os
import pytz

class HomeNumberList(APIView):
    def get(self, request):
        try:
            # 获取各模型的数量统计
            album_count = Album.objects.all().count()
            category_count = Category.objects.all().count()
            article_count = Article.objects.all().count()

            response_data = {
                "album_count": album_count,
                "category_count": category_count,
                "article_count": article_count
            }

            return Response(response_data)

        except Exception as e:
            # 异常处理（可根据需要自定义错误响应）
            return Response(
                {"error": f"获取数据时发生错误: {str(e)}"},
                status=500
            )

class ArticleList(APIView):
    def get(self, request):
        category_id = request.GET.get('id')
        if category_id and category_id.isdigit():
            articles = Article.objects.filter(category_id=category_id)
        else:
            articles = Article.objects.all()
        serializer = ArticleAllSerializer(articles, many=True)  # 序列化数据
        return Response(serializer.data)
    
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        serializer = CategoryAllSerializer(categories, many=True)
        return Response(serializer.data)
    
class ArticleDetailView(APIView):
    def get(self, request):
        article_id = request.GET.get('id')
        if not article_id or not article_id.isdigit():
            return Response({"error": "A valid ID is required"}, status=400)
        
        try:
            article = Article.objects.get(id=article_id)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            raise NotFound("Article not found")
        
class CategoryDetailView(APIView):
    def get(self, request):
        category_id = request.GET.get('id')
        if not category_id or not category_id.isdigit():
            return Response({"error": "A valid ID is required"}, status=400)
        
        try:
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise NotFound("Category not found")
        
class AlbumList(APIView):
    def get(self, request):
        albums = Album.objects.all().order_by('id')
        serializer = AlbumSerializer(albums, many=True)  # 序列化数据
        return Response(serializer.data)
    
class AlbumDetailView(APIView):
    def get(self, request):
        album_id = request.GET.get('albumId')

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"error": "Album not found"}, status=404)

        album_photos = AlbumPhoto.objects.filter(album_id=album_id).order_by('-id')
        
        photo_serializer = AlbumPhotoSerializer(album_photos, many=True)

        return Response({
            "albumName": album.name,
            "photos": photo_serializer.data
        })