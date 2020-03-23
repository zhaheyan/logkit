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
        responses={201: "{'status_code': 201, 'message': '注册成功'}"},
        security=[]
    )
    def post(self, request, *args, **kwargs):
        response = {'status_code': 201, "message": "注册成功"}

        username = request.data.get('username')
        email = request.data.get('email')
        user_obj = User.objects.filter(username=username)
        if not user_obj:
            # 反序列话
            user = UserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                response['data'] = {'username': username, 'email': email}
            else:
                response['status_code'] = 400
                response['message'] = '注册失败'
        else:
            response['status_code'] = 202
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
        responses={201: "{'status_code': 201, 'message': '登录成功'}"},
        security=[]
    )
    def post(self, request, *args, **kwargs):
        response = {'status_code': 201, 'message': '登录成功'}

        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = User.objects.get(username=username, password=password)
        if not user_obj:
            response['status_code'] = 401
            response['message'] = '登录失败，用户不存在'
        else:
            token = jwt_token.create_token(user_obj.username)
            response['data'] = {
		'token': token,
                'username': user_obj.username,
                'email': user_obj.email,
            }

        return JsonResponse(response)

