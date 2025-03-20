# api/utils.py
from django.core.cache import cache
from django.utils import timezone
from api.models import Article, WebInformation

def record_visit(request, article_id=None):
    # 确保 "total_views" 键存在，若不存在，则初始化为 0
    if cache.get("total_views") is None:
        web_information = WebInformation.objects.latest('date') 
        total_views = web_information.total_views
        cache.set("total_views", total_views)

    # 确保 "today_views" 键存在，若不存在，则初始化为 0
    if cache.get("today_views") is None:
        cache.set("today_views", 0)

    # 递增访问量
    cache.incr("total_views")
    cache.incr("today_views")

    # 如果是文章页面，递增文章访问量
    if article_id:
        article_cache_key = f"article_views:{article_id}"
        article_views = cache.get(article_cache_key)
        if article_views is None:
            try:
                article = Article.objects.get(id=article_id)
                article_views = article.visits

                # 将从数据库读取的访问量存入缓存
                cache.set(article_cache_key, article_views, timeout=3600)
            except Article.DoesNotExist:
                article_views = 0  # 如果找不到该文章，默认为 0

        # 递增文章访问量
        cache.incr(article_cache_key)

    # 记录独立访客
    user_ip = request.META.get("REMOTE_ADDR")  # 获取用户 IP
    today = timezone.now().strftime("%Y-%m-%d")
    
    # 获取 Redis 客户端
    redis_client = cache.client.get_client()
    
    # 使用 Redis 客户端执行 sadd 操作
    redis_client.sadd(f"unique_visitors_{today}", user_ip)