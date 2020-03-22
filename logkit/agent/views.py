import json
import logging
from django.core import serializers
from rest_framework.views import APIView
from django.http import JsonResponse
from agent.models import Agent
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from logkit.utils.api import get_request_args

LOG = logging.getLogger('default')


# Create your views here.
class AgentView(APIView):
    """docstring"""

    token = openapi.Parameter("token", openapi.IN_HEADER, description="token",
                                   type=openapi.IN_HEADER)
    @swagger_auto_schema(operation_description="get agent info",
                         responses={404: 'args not found'},
                         manual_parameters=[token])
    def get(self, request):
        """get agent info"""
        response = {'status_code': 200, "message": "获取信息成功"}
        try:
            agents = Agent.objects.all()
            response['data'] = json.loads(serializers.serialize("json", agents))
        except Exception as e:
            response['status_code'] = "500"
            response['message'] = "获取agent信息失败. {}".format(e)

        return JsonResponse(response)


class AgentManagerView(APIView):
    """docsting"""

    @swagger_auto_schema(
        operation_description="handle log",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['agent_ip', "operation", 'token'],
            properties={
                'agent_ip': openapi.Schema(type=openapi.TYPE_STRING),
                'operation': openapi.Schema(type=openapi.TYPE_STRING),
                'token': openapi.Schema(type=openapi.IN_HEADER),
            },
        ),
        security=[]
    )
    @get_request_args
    def post(self, request, args):
        """docstring"""
        response = {'status_code': 200, "message": "操作成功"}

        LOG.info(args)

        return JsonResponse(response)

