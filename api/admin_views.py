from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from rest_framework import status
from django.db.models import Q
from django.conf import settings
from .models import *
from .admin_serializers import *
import os
import pytz

class Pagination(PageNumberPagination):
    page_size = 6  # 每页显示7条数据
    page_size_query_param = 'page_size'  # 可以通过查询参数调整每页的数量
    max_page_size = 100  # 最大页数限制

class ArticleList(APIView):
    def get(self, request):
        categoryName = request.GET.get('categoryName')  # 获取分类名称
        title = request.GET.get('title')  # 获取标题
        status = request.GET.get('status')  # 获取状态

        # 使用 Q 对象动态构造查询条件
        query = Q()
        
        if categoryName:
            try:
                category = Category.objects.get(name=categoryName)
                query &= Q(category_id=category.id)
            except Category.DoesNotExist:
                return Response({"error": "分类不存在"}, status=404)

        if title:
            query &= Q(title__icontains=title)  # 标题模糊查询
        if status:
            query &= Q(status=status)  # 状态过滤

        articles = Article.objects.filter(query).order_by('id')

        # 分页
        paginator = Pagination()
        result_page = paginator.paginate_queryset(articles, request)
        
        # 序列化数据并返回分页响应，包含 count 等分页信息
        serializer = ArticleAllSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ArticleContentView(APIView):
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

class CategoryWithArticlesView(APIView):
    def get(self, request):
        # 获取所有存在文章的分类名称
        categories_with_articles = CategoryExistSerializer.get_categories_with_articles()
        return Response(categories_with_articles)

class CategoriesOutSubView(APIView):
    def get(self, request):
        categories_without_subcategory = CategoryAllNameMinSerializer.get_categories_without_subcategories()
        return Response(categories_without_subcategory)
    
UPLOAD_ARTICLE_DIR = ".\\fronted\\public\\uploads"

class UploadImage(APIView):
    def post(self,request):
        if request.method == 'POST' and request.FILES.get('file'):
            uploadPath = UPLOAD_ARTICLE_DIR
            if request.POST.get('address'):
                uploadPath = request.POST.get('address')
            file = request.FILES['file']
            file_name = file.name  # 使用上传的文件名，不进行修改

            file_path = os.path.join(uploadPath, file_name)
            # print(file_path)

            # 创建目录，如果没有的话
            os.makedirs(uploadPath, exist_ok=True)

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

        # print(title)
        # print(content)
        # print(status)

        # 检查是否有 title 和 content 参数
        if not title or not content or not status:
            return Response(
                {"error": "Title and content and status are required."}, 
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
            status=status  # 默认状态
        )

        # 保存文章
        article.save()

        # 使用序列化器返回文章的详细信息
        serializer = ArticleSerializer(article)

        # 返回创建的文章信息
        return Response(serializer.data)
    
class DeleteArticles(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No article IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        Article.objects.filter(id__in=ids).delete()
        return Response({"detail": "Articles deleted successfully."}, status=status.HTTP_200_OK)

class UpdateArticleContent(APIView):
    def post(self, request):
        # 从请求中获取 article_id 和 content 参数
        article_id = request.data.get('id')
        title = request.data.get('title')
        content = request.data.get('content')

        # 检查必要参数是否存在
        if not article_id or not content:
            return Response(
                {"error": "ID and content are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 获取对应的文章对象
            article = Article.objects.get(id=article_id)

            # 更新文章的内容
            article.title = title
            article.content = content
            article.updated_at = timezone.now()

            # 保存更新后的文章
            article.save()

            # 使用序列化器返回更新后的文章信息
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Article.DoesNotExist:
            return Response(
                {"error": "Article not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class UpdateArticleBase(APIView):
    def post(self, request):
        article_id = request.data.get('id')
        bannar_id = request.data.get('bannar_id')
        summary = request.data.get('summary')
        categoryName = request.data.get('categoryName')
        article_status = request.data.get('status')
        
        # 获取对应的文章对象
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))

        # 更新文章的属性
        if bannar_id != "null":
            media_instance = Media.objects.get(id=bannar_id)
            article.bannar_id = media_instance 
        else:
            article.bannar_id = None
        if categoryName != "未分类":
            category_instance = Category.objects.get(name=categoryName)
            article.category_id = category_instance
        else:
            article.category_id = None
        article.summary = summary
        article.status = article_status
        article.updated_at = current_time

        # 保存更新后的文章对象
        article.save()

        return Response({"message": "Article updated successfully"}, status=status.HTTP_200_OK)

class AddMedia(APIView):
    def post(self, request):
        # 获取传入的参数
        file = request.data.get('file')
        file_type = request.data.get('fileType')
        file_size = request.data.get('fileSize')

        if not file or not file_type or not file_size:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))

        # 检查是否已存在相同文件（通过哈希值，或者可以通过其他字段如file_type和file_size）
        try:
            existing_media = Media.objects.get(file_size=file_size, file_type=file_type, file=file)
            return Response({"id": existing_media.id, "message": "File already exists."}, status=status.HTTP_200_OK)
        except Media.DoesNotExist:
            # 如果文件不存在，则保存新文件
            media_instance = Media.objects.create(
                file=file,
                file_type=file_type,
                file_size=file_size,
                uploaded_at = current_time
            )
            return Response({"id": media_instance.id, "message": "File uploaded successfully."}, status=status.HTTP_201_CREATED)

class CategoryList(APIView):
    def get(self, request):
        parentName = request.GET.get('parent')

        query = Q()
        if parentName:
            try:
                # 获取指定的父分类
                category = Category.objects.get(name=parentName)
                
                # 获取所有后代分类 ID
                def get_descendants(category):
                    descendants = []
                    children = category.subcategories.all()
                    for child in children:
                        descendants.append(child.id)
                        descendants.extend(get_descendants(child))
                    return descendants
                
                # 获取当前分类及其所有后代分类
                descendant_ids = get_descendants(category)
                descendant_ids.append(category.id)  # 包含自身 ID
                query &= Q(id__in=descendant_ids)
            except Category.DoesNotExist:
                return Response({"error": "分类不存在"}, status=404)
        
        categories = Category.objects.filter(query).order_by('id')

        # 分页逻辑
        paginator = Pagination()
        result_page = paginator.paginate_queryset(categories, request)

        # 序列化数据并返回分页响应，包含 count 等分页信息
        serializer = CategoryAllSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CategoryName(APIView):
    def get(self, request):
        category_names = Category.objects.all().order_by('id').values_list('name', flat=True)
        return Response(list(category_names), status=status.HTTP_200_OK)

class AddCategory(APIView):
    def post(self, request):
        category_id = request.data.get('id')
        name = request.data.get('name')
        bannar_id = request.data.get('bannar_id')
        description = request.data.get('description')
        parentName = request.data.get('parent')

        print(category_id)
    
        if not name:
            return Response(
                {"error": "Name are required."}, 
            )

        # 获取父分类的 ID
        parent_category = None
        if parentName:
            try:
                parent_category = Category.objects.get(name=parentName)
            except Category.DoesNotExist:
                return Response(
                    {"error": f"Parent category '{parentName}' does not exist."},
                    status=400
                )
        
        media_instance = None
        if bannar_id and bannar_id != "null":
            media_instance = Media.objects.get(id=bannar_id)

        # 获取当前时间
        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))

        category = Category(
            name = name,
            description = description,
            created_at=current_time,
            updated_at=current_time,
            bannar_id = media_instance,
            parent = parent_category
        )

        category.save()

        return Response({"message": "Category created successfully"}, status=201)

class UpdateCategory(APIView):
    def post(self, request):
        category_id = request.data.get('id')
        name = request.data.get('name')
        bannar_id = request.data.get('bannar_id')
        description = request.data.get('description')
        parentName = request.data.get('parent')

        if not name:
            return Response(
                {"error": "Name are required."}, 
            )
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.name = name
        category.description = description

        # 获取父分类的 ID
        parent_category = None
        if parentName:
            try:
                parent_category = Category.objects.get(name=parentName)
            except Category.DoesNotExist:
                return Response(
                    {"error": f"Parent category '{parentName}' does not exist."},
                    status=400
                )
        category.parent = parent_category
        
        media_instance = None
        if bannar_id and bannar_id != "null":
            media_instance = Media.objects.get(id=bannar_id)
        category.bannar_id = media_instance

        # 获取当前时间
        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))
        category.updated_at = current_time

        category.save()
        
        return Response({"message": "Category updated successfully"}, status=200)

class DeleteCategories(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No category IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        Category.objects.filter(id__in=ids).delete()
        return Response({"detail": "Categories deleted successfully."}, status=status.HTTP_200_OK)
    

class UploadPhoto(APIView):
    def post(self, request):
        file = request.FILES.get('file')  # 获取上传的文件
        file_type = request.data.get('fileType')  # 获取文件类型
        file_size = request.data.get('fileSize')  # 获取文件大小
        album_name = request.data.get('albumName')  # 获取相册名
        
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 直接使用 Django FileField 处理上传文件
        album = Album.objects.get(name=album_name) if album_name else None

        media_instance = AlbumPhoto.objects.create(
            file=file,  # 直接赋值给 FileField，Django 会自动存储到 `media/uploads/`
            file_type=file_type,
            file_size=file_size,
            album_name=album
        )

        return Response({
            "message": "File uploaded successfully",
            "id": media_instance.id,
            "file_url": media_instance.file.url  # Django 自动生成 URL
        }, status=status.HTTP_201_CREATED)
    

class AlbumPhotoList(APIView):
    def get(self, request):
        album_name = request.GET.get('album')

        if album_name:
            photos = AlbumPhoto.objects.filter(album_name__name=album_name)  # 按相册筛选
        else:
            photos = AlbumPhoto.objects.all()  # 获取所有图片
        
        # 初始化分页器
        paginator = Pagination()
        paginated_photos = paginator.paginate_queryset(photos, request)

        # 序列化分页后的数据
        serializer = AlbumPhotoSerializer(paginated_photos, many=True)

        print(settings.BASE_DIR)

        # 返回分页后的响应
        return paginator.get_paginated_response(serializer.data)
