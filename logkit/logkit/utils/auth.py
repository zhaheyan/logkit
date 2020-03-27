import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from logkit.utils import jwt_token

class MyAuthentication(BaseAuthentication):
    """Authentication"""

    def authenticate(self, request):
        """从请求中获取token和username, 验证通过重置有效期"""
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise exceptions.NotAuthenticated('用户认证失败: token信息获取失败，请重新登录')

        username = jwt_token.get_username(token)
        if username is None:
            raise exceptions.AuthenticationFailed('用户认证失败: token无效，请重新登录')

        token = jwt_token.create_token(username)
        return username, token

