from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer

class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()  # 获取所有文章
        serializer = ArticleSerializer(articles, many=True)  # 序列化数据
        return Response(serializer.data)