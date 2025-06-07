from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.utils import timezone
from django_redis import get_redis_connection
import os

# Create your models here.
class WebInformation(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)  # 统计日期
    total_views = models.IntegerField(default=0)  # 总访问量
    today_views = models.IntegerField(default=0)  # 今日访问量
    unique_visitors = models.IntegerField(default=0)  # 独立访客

    @classmethod
    def update_stats(cls):
        """每天定时同步 Redis 数据到数据库"""
        today = timezone.now().date()
         # 获取 Redis 连接
        redis_conn = get_redis_connection("default")
        # 获取 Redis 集合中独立访客的数量
        unique_visitors_count = redis_conn.scard("unique_visitors_" + str(today))

        site_stats, _ = cls.objects.get_or_create(date=today)
        
        site_stats.today_views = cache.get("today_views", 0)
        site_stats.total_views = cache.get("total_views", 0)
        site_stats.unique_visitors = unique_visitors_count

        site_stats.save()

class Media(models.Model):
    file = models.FileField(upload_to='images/')  # 存储文件的路径
    file_type = models.CharField(max_length=50)  # 文件类型（如图片、视频等）
    file_size = models.PositiveIntegerField()  # 文件大小
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 上传时间

    class Meta:
        indexes = [
            models.Index(fields=['file_type']),
        ]

    def __str__(self):
        return self.file.name

class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)  # 分类描述
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('private', 'Private'), ('public', 'Public')], default='public')

    def __str__(self):
        return self.name

class AlbumPhoto(models.Model):
    file = models.FileField(upload_to='uploads/')  # 存储文件的路径
    file_type = models.CharField(max_length=50)  # 文件类型（如图片、视频等）
    file_size = models.PositiveIntegerField()  # 文件大小
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 上传时间

    album_id = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.file.name

class User(AbstractUser):
    UID = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    signature = models.CharField(max_length=100, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # 外键
    avater = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # 只在没有设置 user_id 的情况下，才自动赋值
        if not self.UID:
            # 获取当前最大的 user_id，并加 1
            max_user_id = User.objects.aggregate(Max('UID'))['UID__max']
            if max_user_id:
                new_user_id = max_user_id + 1
            else:
                new_user_id = 10000000  # 如果没有记录，初始化为 10000000（8 位）
            # 确保 user_id 是 8 位
            self.UID = new_user_id
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 分类名称
    description = models.TextField(null=True, blank=True)  # 分类描述
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bannar_id = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    # 外键关联父类分类（如果有），树状结构
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_children_recursive(self):
        """递归获取当前分类的所有子分类及其子分类"""
        children = self.subcategories.all()
        result = []
        for child in children:
            # 对每个子类进行递归
            child_data = {
                'id': child.id,
                'name': child.name,
                'children': child.get_children_recursive(),
                'parent': child.get_ancestors(),
                'article_count': child.articles.count()  # 统计该分类下的文章数量
            }
            result.append(child_data)
        return result

    def get_children(self):
        """获取当前分类的所有子分类"""
        return self.subcategories.all()

    def get_ancestors(self):
        """递归获取当前分类的所有父分类（祖先）"""
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent.id)
            parent = parent.parent
        return ancestors[::-1]  # 返回从上到下的父分类列表

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    visits = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    # 外键
    user_id = models.ForeignKey(User, to_field='UID', on_delete=models.CASCADE, related_name='articles')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    bannar_id = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['title']),
            models.Index(fields=['category_id']),
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 外键
    user_id = models.ForeignKey(User, to_field='UID',  on_delete=models.CASCADE, related_name='comment')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')
    
    # 外键关联父评论（如果有）
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_at']  # 默认按创建时间排序（可以按需修改）
        indexes = [
            models.Index(fields=['user_id', 'article_id']),
        ]

    def __str__(self):
        return f"Comment by {self.user_id.username} on {self.article_id.title}"

class Emotion(models.Model):
    content = models.TextField(verbose_name="内容", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    status = models.PositiveSmallIntegerField(default=1, choices=[
        (1, '公开'),
        (2, '私密')
    ])

    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

class EmotionMedia(models.Model):
    file = models.FileField(upload_to='emotions/')
    created_at = models.DateTimeField(auto_now_add=True)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
class Message(models.Model):
    content = models.TextField(verbose_name="内容", blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    