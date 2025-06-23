from celery import shared_task
from api.models import WebInformation, Article
from django.core.cache import cache

@shared_task
def clear_cache_daily():
    """清空所有缓存"""
    cache.clear()

@shared_task
def update_site_stats():
    """更新网站统计信息"""
    # 调用 WebInformation 的 update_stats 方法
    WebInformation.update_stats()

@shared_task
def sync_article_views_to_db():
    """将缓存中的文章访问量写入数据库"""
    article_keys = cache.keys("article_views:*")  # 获取所有文章访问量的缓存键
    
    for key in article_keys:
        article_id = key.split(":")[-1]  # 提取文章 ID
        article_views = cache.get(key)  # 获取缓存中的访问量
        
        if article_views is not None:
            # 更新数据库
            Article.objects.filter(id=article_id).update(visit=article_views)
            print(f"文章 {article_id} 访问量同步到数据库: {article_views}")

            # 可选：重置缓存，避免重复写入
            # cache.set(key, article_views, timeout=3600)  