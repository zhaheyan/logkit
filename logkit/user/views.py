import datetime
import jwt
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from logkit.utils import jwt_token
from user.models import User, UserSerializer


# Create your views here.
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_description="logkit register",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'email'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL),
            },
        ),
        security=[]
    )
    def post(self, request, *args, **kwargs):
        response = {'status_code': 200, "message": "注册成功"}

        username = request.data.get('username')
        password = request.data.get("password")
        user_obj = User.objects.filter(username=username)
        if not user_obj:
            # 反序列话
            user = UserSerializer(data=request.data)
            print(user)
            if user.is_valid():
                user.save()
                response['data'] = user.validated_data
            else:
                response['status_code'] = 400
                response['message'] = '注册失败'
        else:
            response['status_code'] = 201
            response['message'] = "用户已存在"
        return JsonResponse(response)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_description="logkit login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[]
    )
    def post(self, request, *args, **kwargs):
        response = {'status_code': 200, 'message': '登录成功'}

        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = User.objects.get(username=username)
        if not user_obj:
            response['status_code'] = 401
            response['message'] = '登录失败，用户不存在'
        else:
            token = jwt_token.create_token(user_obj.username)
            response['token'] = token

        return JsonResponse(response)

