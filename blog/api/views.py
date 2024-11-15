from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()  # 获取所有文章
        serializer = ArticleAllSerializer(articles, many=True)  # 序列化数据
        return Response(serializer.data)
    
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        serializer = CategoryAllSerializer(categories, many=True)
        return Response(serializer.data)
