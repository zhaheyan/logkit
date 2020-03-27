import json
import logging
import requests
from requests import exceptions

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


from django.conf import settings


class AgentHealthCheckView(APIView):
    """docsting"""

    token = openapi.Parameter("token", openapi.IN_HEADER, description="token",
                                   type=openapi.IN_HEADER)
    @swagger_auto_schema(operation_description="agent health check",
                         responses={404: 'args not found'},
                         manual_parameters=[token])
    def get(self, request):
        """docstring"""
        response = {'status_code': 200, "message": "操作成功"}

        try:
            agents_info = settings.OPSAGENT['agents_info']
            for agent_info in agents_info:
                agent_url = agent_info + "/agent/health_check"
                agent_ip = agent_url.split('/')[2]
                try:
                    r = requests.get(agent_url, timeout=5)
                    if r.status_code == 200:
                        Agent.objects.filter(agent_ip=agent_ip).update(agent_status='health')
                    else:
                        Agent.objects.filter(agent_ip=agent_ip).update(agent_status='abnormal')
                except exceptions.Timeout as e:
                    Agent.objects.filter(agent_ip=agent_ip).update(agent_status='abnormal')
                    LOG.error('agent status abnormal! error info: %s', e)
                LOG.info("check agent: %s", agent_ip)
        except Exception as e:
            response['status_code'] = "500"
            response['message'] = "检查agent信息失败. {}".format(e)
            LOG.error('check agent status failed! error info: %s', e)

        return JsonResponse(response)

