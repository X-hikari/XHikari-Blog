from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置默认 Django 配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')

# 使用 Django 的 settings.py 中的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有注册的任务
app.autodiscover_tasks()