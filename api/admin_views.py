from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
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

class MediaList(APIView):
    def get(self, request):
        filetype = request.GET.get('type')
        fileused = request.GET.get('used')

        # 初始查询
        queryset = Media.objects.all()

        if filetype:
            queryset = queryset.filter(file_type=filetype)

        # 根据 fileused 过滤是否被引用
        if fileused == '1':  # 查询被引用的媒体
            filter_condition = Q()

            # 只考虑 Article 和 Category 这两个模型
            for model_class in [Article, Category]:
                for field in model_class._meta.get_fields():
                    if isinstance(field, models.ForeignKey) and field.related_model == Media:
                        # 动态生成查询条件，检查该外键字段是否引用了 Media
                        related_field_name = field.name
                        filter_condition |= Q(**{f'{related_field_name}__in': queryset.values('id')})

            # 使用合并的过滤条件来查询 Media
            queryset = queryset.filter(filter_condition)

        # 分页
        paginator = Pagination()
        result_page = paginator.paginate_queryset(queryset, request)
        
        # 序列化数据并返回分页响应，包含 count 等分页信息
        serializer = MediaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
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

class UpdateMedia(APIView):
    def post(self, request):
        media_id = request.data.get('id')
        media_name = request.data.get('name')

        if not media_name:
            return Response(
                {"error": "Name are required."}, 
            )
        
        try:
            media = Media.objects.get(id=media_id)
        except media.DoesNotExist:
            return Response({"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取原始文件路径，并替换文件名部分
        if media.file:  # 如果photo.file有值
            old_file_path = media.file.path

            # 获取文件名和扩展名
            file_name = os.path.basename(old_file_path)  # 获取文件名（包括扩展名）
            file_dir = os.path.dirname(old_file_path)    # 获取文件所在的目录
            file_name_without_extension, file_extension = os.path.splitext(file_name)  # 分离文件名和扩展名

            # 创建新的文件名
            new_file_name = f"{media_name}{file_extension}"
            # print(f"New file name: {new_file_name}")

            # 拼接新的完整路径
            new_file_path = os.path.join(file_dir, new_file_name)
            # print(f"New file path: {new_file_path}")

            try:
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                # print(f"File renamed to {new_file_path}")
            except Exception as e:
                # 捕获异常并返回详细错误信息
                print(f"Error renaming file: {str(e)}")
                return Response(
                    {"error": f"Failed to rename file: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 更新photo.file
            media.file.name = f"images/{new_file_name}"

        media.save()

        return Response({"message": "media updated successfully"}, status=200)
    
class DeleteMedias(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No media IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取要删除的相片记录
        medias_to_delete = Media.objects.filter(id__in=ids).order_by('id')
        
        # 遍历并删除每个相片的文件
        for media in medias_to_delete:
            media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
            if os.path.exists(media_file_path):
                os.remove(media_file_path)
        
        # 删除数据库中的记录
        medias_to_delete.delete()
        return Response({"detail": "Categories deleted successfully."}, status=status.HTTP_200_OK)

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

        # print(category_id)
    
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
        
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        media_instance = AlbumPhoto.objects.create(
            file=file,  # 直接赋值给 FileField，Django 会自动存储到 `media/uploads/`
            file_type=file_type,
            file_size=file_size,
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
            album = Album.objects.filter(name=album_name).first()
            photos = AlbumPhoto.objects.filter(album_id=album)  # 按相册筛选
        else:
            photos = AlbumPhoto.objects.all()  # 获取所有图片
        
        # 初始化分页器
        paginator = Pagination()
        paginated_photos = paginator.paginate_queryset(photos, request)

        # 序列化分页后的数据
        serializer = AlbumPhotoSerializer(paginated_photos, many=True)

        # 返回分页后的响应
        return paginator.get_paginated_response(serializer.data)

class UpdateAlbumPhoto(APIView):
    def post(self, request):
        photo_id = request.data.get('id')
        photo_name = request.data.get('name')
        album_name = request.data.get('album')

        if not photo_name:
            return Response(
                {"error": "Name are required."}, 
            )
        
        try:
            photo = AlbumPhoto.objects.get(id=photo_id)
        except photo.DoesNotExist:
            return Response({"error": "photo not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 获取原始文件路径，并替换文件名部分
        if photo.file:  # 如果photo.file有值
            old_file_path = photo.file.path

            # 获取文件名和扩展名
            file_name = os.path.basename(old_file_path)  # 获取文件名（包括扩展名）
            file_dir = os.path.dirname(old_file_path)    # 获取文件所在的目录
            file_name_without_extension, file_extension = os.path.splitext(file_name)  # 分离文件名和扩展名

            # 创建新的文件名
            new_file_name = f"{photo_name}{file_extension}"
            # print(f"New file name: {new_file_name}")

            # 拼接新的完整路径
            new_file_path = os.path.join(file_dir, new_file_name)
            # print(f"New file path: {new_file_path}")

            try:
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                # print(f"File renamed to {new_file_path}")
            except Exception as e:
                # 捕获异常并返回详细错误信息
                print(f"Error renaming file: {str(e)}")
                return Response(
                    {"error": f"Failed to rename file: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 更新photo.file
            photo.file.name = f"uploads/{new_file_name}"

        if album_name:
            album = Album.objects.filter(name=album_name).first()
            if album:
                photo.album_id = album
        else:
            photo.album_id = None
        photo.save()

        return Response({"message": "photo updated successfully"}, status=200)

class DeleteAlbumPhotos(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No category IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取要删除的相片记录
        photos_to_delete = AlbumPhoto.objects.filter(id__in=ids).order_by('id')
        
        # 遍历并删除每个相片的文件
        for photo in photos_to_delete:
            photo_file_path = os.path.join(settings.MEDIA_ROOT, photo.file.name)
            if os.path.exists(photo_file_path):
                os.remove(photo_file_path)
        
        # 删除数据库中的记录
        photos_to_delete.delete()
        return Response({"detail": "Categories deleted successfully."}, status=status.HTTP_200_OK)

class AlbumList(APIView):
    def get(self, request):
        albums = Album.objects.all().order_by('id')

        # 仅在请求中有分页参数时才进行分页
        if 'page' in request.query_params:
            paginator = Pagination()
            paginated_albums = paginator.paginate_queryset(albums, request)
            serializer = AlbumSerializer(paginated_albums, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # 否则返回完整数据
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    
class AddAlbum(APIView):
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        current_time = timezone.now()
        current_time = current_time.astimezone(pytz.timezone('Asia/Shanghai'))

        try:
            existing_album = Album.objects.get(name=name)
            return Response({"id": existing_album.id, "message": "Album already exists."}, status=status.HTTP_200_OK)
        except Album.DoesNotExist:
            # 如果文件不存在，则保存新文件
            album_instance = Album.objects.create(
                name=name,
                description=description,
                created_at=current_time,
                updated_at = current_time
            )
            return Response({"id": album_instance.id, "message": "Album added successfully."}, status=status.HTTP_201_CREATED)

class UpdateAlbum(APIView):
    def post(self, request):
        album_id = request.data.get('id')
        name = request.data.get('name')
        description = request.data.get('description')
        current_time = timezone.now()

        if not name:
            return Response(
                {"error": "Name are required."}, 
            )
        
        try:
            album = Album.objects.get(id=album_id)
        except album.DoesNotExist:
            return Response({"error": "Album not found"}, status=status.HTTP_404_NOT_FOUND)
        
        album.name = name
        album.description = description
        album.updated_at = current_time
        album.save()

        return Response({"message": "photo updated successfully"}, status=200)
    
class DeleteAlbum(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No category IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        Album.objects.filter(id__in=ids).delete()
        return Response({"detail": "Categories deleted successfully."}, status=status.HTTP_200_OK)

class EmotionList(APIView):
    def get(self, request):
        limit = request.GET.get('limit')
        if limit:
            emotions = Emotion.objects.filter(status=limit)
        else:
            emotions = Emotion.objects.all()
        
        paginator = Pagination()
        paginated_emotions = paginator.paginate_queryset(emotions, request)
        serializer = EmotionSerializer(paginated_emotions, many=True)
        return paginator.get_paginated_response(serializer.data)

class AddEmotion(APIView):
    def post(self, request):
        content = request.data.get('content', '')
        limit = request.data.get('limit')
        
        if limit == '公开':
            limit = 1
        elif limit == '私密':
            limit = 2
        else:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()

        emotion = Emotion.objects.create(
            content=content,
            status=limit,
            created_at=current_time,
            updated_at=current_time
        )
        
        return Response({"emotionId": emotion.id}, status=status.HTTP_201_CREATED)

class DeleteEmotions(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No category IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        emotions = Emotion.objects.filter(id__in=ids)
        if not emotions.exists():
            return Response({"detail": "No emotions found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        for emotion in emotions:
            # 获取与当前 Emotion 相关的所有 EmotionMedia 实例
            emotion_media = EmotionMedia.objects.filter(emotion=emotion)
            for media in emotion_media:
                # 删除与该 EmotionMedia 相关联的文件
                if media.file and os.path.isfile(media.file.path):
                    os.remove(media.file.path)  # 删除实际的文件

            emotion_media.delete()

        emotions.delete()

        return Response({"detail": "Emotions and related media files have been deleted."}, status=status.HTTP_200_OK)

class AddEmotionMedia(APIView):
    def post(self, request):
        emotion_id = request.data.get('emotionId')
        images = request.FILES.getlist('images[]')

        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        try:
            emotion = Emotion.objects.get(id=emotion_id)
        except Emotion.DoesNotExist:
            return Response({"error": "没有这条说说"}, status=status.HTTP_404_NOT_FOUND)

        for idx, image in enumerate(images, start=1):  
            ext = os.path.splitext(image.name)[1]
            new_filename = f"Emotion{timestamp}_{idx}{ext}"
            image.name = new_filename
            emotionMedia_instance = EmotionMedia.objects.create(
                file = image,
                emotion = emotion
            )

        return Response({
            "image_count": len(images),
        }, status=status.HTTP_201_CREATED)
    
class EmotionDetail(APIView):
    def get(self, request):
        emotion_id = request.GET.get('emotionId')

        try:
            emotion = Emotion.objects.get(id=emotion_id)
        except Emotion.DoesNotExist:
            return Response({"detail": "Emotion not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmotionDetailSerializer(emotion)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateEmotion(APIView):
    def post(self, request):
        emotion_id = request.data.get('emotionId')
        images = request.data.getlist('images[]')
        newimages = request.FILES.getlist('newimages[]')
        limit = request.data.get('limit')
        content = request.data.get('content', '')
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        print("处理前的: ", images)

        print(newimages)

        images = list(map(lambda x: x[7:], images))
        print("处理后的: ",images)
        if limit == "公开":
            limit = 1
        elif limit == "私密":
            limit = 2 

        try:
            emotion = Emotion.objects.get(id=emotion_id)
        except Emotion.DoesNotExist:
            return Response({"detail": "Emotion not found."}, status=status.HTTP_404_NOT_FOUND)

        # 删除原本的媒体文件
        current_media_files = EmotionMedia.objects.filter(emotion=emotion)
        # current_media_files_in = EmotionMedia.objects.filter(file__in=images)
        media_files_to_delete = current_media_files.exclude(file__in=images)
        print(media_files_to_delete)
        for media in media_files_to_delete:
            if media.file and os.path.isfile(media.file.path):
                os.remove(media.file.path)
        media_files_to_delete.delete()

        # 添加新的媒体文件
        for idx, image in enumerate(newimages, start=1):  
            ext = os.path.splitext(image.name)[1]
            new_filename = f"Emotion{timestamp}_{idx}{ext}"
            image.name = new_filename
            emotionMedia_instance = EmotionMedia.objects.create(
                file = image,
                emotion = emotion
            )
        
        emotion.content = content
        emotion.status = limit
        emotion.updated_at = timezone.now()
        emotion.save()

        return Response({}, status=status.HTTP_200_OK)