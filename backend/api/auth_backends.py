# your_app/auth_backends.py
from django.contrib.auth.backends import BaseBackend
from api.models import User  
from django.contrib.auth.hashers import check_password

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 查找自定义 User 模型中的用户名
            user = User.objects.get(username=username)
            
            # 使用 check_password 比较哈希密码
            if check_password(password, user.password_hash):
                return user
        except User.DoesNotExist:
            return None
