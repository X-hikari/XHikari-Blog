from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
from django.utils import timezone
from .models import *
from .serializers import *
from datetime import datetime
from django.conf import settings
from rest_framework import status
from django.core.cache import cache
from api.utils import record_visit
import os
import pytz

class VisitWeb(APIView):
    def post(self, request):
        record_visit(request)
        return JsonResponse({"message": "Visit recorded"}, status=200)
    
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
        record_visit(request, article_id)
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
    
class EmotionList(APIView):
    def get(self, request):
        date = request.GET.get('date')

        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            # 获取该日期的起始和结束时间
            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

            # 查找在这个日期范围内的说说
            emotions = Emotion.objects.filter(
                status=1,
                created_at__gte=start_of_day,
                created_at__lte=end_of_day
            ).order_by('-id')
        else:
            emotions = Emotion.objects.filter(status=1).order_by('-id')

        serializer = EmotionSerializer(emotions, many=True)
        return Response({"data": serializer.data})

class MessageList(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        
        return Response({"results": serializer.data})

class AddMessage(APIView):
    def post(self, request):
        content = request.data.get('content')
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(UID = user_id)
        except:
            return Response( {"error": "User are not founded."} )

        message = Message(content=content, user=user)
        message.save()

        return Response({"message": "Message created successfully"}, status=201)

class AboutDetail(APIView):
    def get(self, request):
        # 读取 about.md 文件
        file_path = os.path.join(settings.BASE_DIR, "content", "about.md")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            return Response({"title": "关于", "content": md_content}, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "about.md not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SearchArticles(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            # 使用 SearchQuerySet 进行全文搜索
            results = SearchQuerySet().filter(content=query)
            # print(f"Search Results: {results}")

            # 获取与搜索结果匹配的所有文章
            articles = Article.objects.filter(id__in=[result.pk for result in results])
            serializer = ArticleAllSerializer(articles, many=True)
            
            return Response({'results': serializer.data, 'query': query})
        else:
            return Response({'results': [], 'query': query}, status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Django 记录 Session
            
            # 手动更新 last_login
            user.last_login = timezone.now()
            user.save()
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

@login_required
def check_login(request):
    return JsonResponse({"status": "logged_in"})