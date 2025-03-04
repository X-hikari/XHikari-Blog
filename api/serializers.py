from rest_framework import serializers
from .models import *

class ArticleAllSerializer(serializers.ModelSerializer):
    imageSrc = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'visits', 'updated_at', 'imageSrc']
    
    def get_imageSrc(self, obj):
        if obj.bannar_id:
            return obj.bannar_id.file.url  # 返回图片的URL
        return None

class ArticleSerializer(serializers.ModelSerializer):
    banner_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = '__all__'  # 保留所有字段
        extra_fields = ['category', 'banner_url']

    def get_banner_url(self, obj):
        if obj.bannar_id and obj.bannar_id.file:
            return obj.bannar_id.file.url  # 确保返回的是图片文件的 URL
        return None

    def get_category(self, obj):
        if obj.category_id:
            return obj.category_id.name
        return None

class CategoryAllSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()  # 获取子分类
    parent = serializers.SerializerMethodField()  # 获取祖先分类
    article_count = serializers.SerializerMethodField()  # 获取文章数量

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'children', 'parent', 'article_count']
    
    def get_children(self, obj):
        return obj.get_children_recursive()

    def get_parent(self, obj):
        return obj.get_ancestors()

    def get_article_count(self, obj):
        # 计算当前分类的文章数量
        total_articles = obj.articles.count()

        # 递归地计算所有子分类的文章数量
        for child in obj.subcategories.all():
            total_articles += self.get_article_count(child)

        return total_articles
    
class CategorySerializer(serializers.ModelSerializer):
    banner_url = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()  # 获取文章数量
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Category
        fields = '__all__'  # 保留所有字段
        extra_fields = ['category', 'banner_url']

    def get_banner_url(self, obj):
        if obj.bannar_id and obj.bannar_id.file:
            return obj.bannar_id.file.url  # 确保返回的是图片文件的 URL
        return None
   
    def get_article_count(self, obj):
        # 计算当前分类的文章数量
        total_articles = obj.articles.count()

        # 递归地计算所有子分类的文章数量
        for child in obj.subcategories.all():
            total_articles += self.get_article_count(child)

        return total_articles
    
class AlbumSerializer(serializers.ModelSerializer):
    imageSrc = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'name', 'imageSrc'] 

    def get_imageSrc(self, obj):
        # 获取与该相册关联的最多 3 张最新照片，按 id 降序排列
        latest_photos = AlbumPhoto.objects.filter(album_id=obj.id).order_by('-id')[:3]
        # 返回图片 URL 列表
        return [photo.file.url for photo in latest_photos] if latest_photos else None
    
class AlbumPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumPhoto
        fields = ['file']

    # 通过 `to_representation` 方法，返回一个包含所有 file 路径的列表
    def to_representation(self, instance):
        return instance.file.url
    
class EmotionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Emotion
        fields =  ['content', 'created_at', 'images']

    def get_images(self, obj):
        images = EmotionMedia.objects.filter(emotion_id=obj.id).order_by('id')
        return [image.file.url for image in images] if images else None