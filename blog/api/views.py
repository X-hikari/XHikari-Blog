from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone
from .models import *
from .serializers import *
import os
import pytz

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

UPLOAD_DIR = ".\\fronted\\public\\uploads"

class UploadImage(APIView):
    def post(self,request):
        if request.method == 'POST' and request.FILES.get('file'):
            file = request.FILES['file']
            file_name = file.name  # 使用上传的文件名，不进行修改

            file_path = os.path.join(UPLOAD_DIR, file_name)

            # 创建目录，如果没有的话
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file.read())

            # 返回成功响应，返回文件的存储路径
            return Response({'status': 'success', 'path': f'/uploads/{file_name}'})

        # 如果没有文件上传，则返回错误响应
        return Response({'status': 'error', 'message': 'No file uploaded'}, status=400)

class AddArticle(APIView):
    def post(self, request):
        # 从请求中获取 title 和 content 参数
        title = request.data.get('title')
        content = request.data.get('content')
        status = request.data.get('status')

        print(title)
        print(content)
        print(status)

        # 检查是否有 title 和 content 参数
        if not title or not content or not status:
            return Response(
                {"error": "Title and content are required."}, 
            )

        # 获取当前时间
        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))

        # 创建 Article 实例，使用默认值填充其他字段
        article = Article(
            title=title,
            content=content,
            created_at=current_time,
            updated_at=current_time,
            user_id=User.objects.get(UID=10000000),  # 默认用户ID
            status='published'  # 默认状态
        )

        # 保存文章
        article.save()

        # 使用序列化器返回文章的详细信息
        serializer = ArticleSerializer(article)

        # 返回创建的文章信息
        return Response(serializer.data)