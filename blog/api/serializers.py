from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # 自定义字段 - 获取文章图片
    imageSrc = serializers.SerializerMethodField()
    
    # 自定义字段 - 获取最后更新时间
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'visits', 'updated_at', 'imageSrc']
    
    # 自定义方法来获取文章图片链接
    def get_imageSrc(self, obj):
        if obj.bannar_id:
            return obj.bannar_id.file.url  # 返回图片的URL
        return None
