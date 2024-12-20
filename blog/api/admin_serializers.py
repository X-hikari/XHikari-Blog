from rest_framework import serializers
from .models import *

class ArticleAllSerializer(serializers.ModelSerializer):
    imageSrc = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = ['id', 'imageSrc', 'title', 'summary', 'categoryName', 'status', 'visits', 'updated_at']
    
    def get_categoryName(self, obj):
        if obj.category_id:
            return obj.category_id.name
        return None

    def get_imageSrc(self, obj):
        if obj.bannar_id:
            return obj.bannar_id.file.url  # 返回图片的URL
        return None

class CategoryExistSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['name']

    @staticmethod
    def get_categories_with_articles():
        """返回存在文章的分类名称"""
        # 使用 Django ORM 的 filter 和 values_list 来提高查询效率
        return Category.objects.filter(articles__isnull=False).distinct().values_list('name', flat=True)

class CategoryAllNameMinSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['name']

    @staticmethod
    def get_categories_without_subcategories():
        return Category.objects.filter(subcategories__isnull=True).values_list('name', flat=True)

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