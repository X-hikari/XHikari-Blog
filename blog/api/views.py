from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import *
from .serializers import *

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