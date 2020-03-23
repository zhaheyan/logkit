"""opsserver.views

This module implements the Requests Views.
View is an logical management library, written in Python, for opsserver beings.

:copyright: (c) 2020 by <947201342@qq.com>.
:license: MIT, see LICENSE for more details.
:updateTime: 2020.03.18
"""
import json
import logging

from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from logkit.utils.api import get_request_args
from opsserver.models import RequestData

LOG = logging.getLogger('default')


class OpsServerView(APIView):
    """View of ops-server."""

    @swagger_auto_schema(
        operation_description="ops-server post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['remote_addr', "remote_user", 'token'],
            properties={
                'remote_addr': openapi.Schema(type=openapi.TYPE_STRING),
                'remote_user': openapi.Schema(type=openapi.TYPE_STRING),
                'token': openapi.Schema(type=openapi.IN_HEADER),
            },
        ),
        #security=[]
    )
    @get_request_args
    def post(self, request, args):
        """docstring"""
        response = {}
        print(request.META)

        LOG.info(args)
        remote_addr = args['remote_addr']
        remote_user = args['remote_user']
        try:
            # 数据库更新数据，如果不存在，创建
            RequestData.objects.update_or_create(remote_addr=remote_addr, remote_user=remote_user)
        except Exception as e:
            LOG.error("error info: %s", e)
            response['message'] = "ERROR: Update RequestData information to database failed!"
            response['status_code'] = 500
            return JsonResponse(response)

        response['message'] = "SUCCESS: Update RequestData information to database successful!"
        response['status_code'] = 200
        return JsonResponse(response)

    def _get_data_list(self, limit, page):
        data_list = []
        datas = []

        try:
            datas = RequestData.objects.values().order_by('time_iso8601')
        except Exception as e:
            raise APIException("ERROR: Get datas from database failed! {0}".format(e))
        total = len(datas)

        paginator = Paginator(datas, limit)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of resluts.
            contacts = paginator.page(paginator.num_pages)

        for data in contacts:
            data_list.append(data)

        return data_list, total


    limit = openapi.Parameter("limit", openapi.IN_QUERY, description="single page limit",
                                   type=openapi.TYPE_INTEGER)
    page = openapi.Parameter("page", openapi.IN_QUERY, description="page number",
                                   type=openapi.TYPE_INTEGER)
    token = openapi.Parameter("token", openapi.IN_HEADER, description="token",
                                   type=openapi.IN_HEADER)
    @swagger_auto_schema(operation_description="partial_update description override",
                         responses={404: 'args not found'},
                         manual_parameters=[limit, page, token])
    @get_request_args
    def get(self, request, args):
        """Get nginx request data information from database."""
        response = {}

        limit = args['limit']
        page = args['page']
        try:
            data_list, total = self._get_data_list(limit, page)
        except Exception as e:
            message = "ERROR: Get data list information failed! {0}".format(e)
            response['message'] = message
            response['status_code'] = 500
            return JsonResponse(response)
        LOG.info("get opsserver data successful!")

        response['data_list'] = data_list
        response['total'] = total
        response['message'] = "SUCCESS: Get data list information successful!"
        response['status_code'] = 200
        return JsonResponse(response)

from opsserver.models import IPCount

class IPCountView(APIView):
    """count ip number from address"""

    token = openapi.Parameter("token", openapi.IN_HEADER, description="token",
                                   type=openapi.IN_HEADER)
    @swagger_auto_schema(operation_description="ipcount token",
                         responses={404: 'args not found'},
                         manual_parameters=[token])
    @get_request_args
    def get(self, request, args):
        """get ip count"""
        response = {'status_code': 200, 'message': '查询成功'}

        try:
            ip_counts = IPCount.objects.all()
            response['data'] = json.loads(serializers.serialize("json", ip_counts))
        except Exception as e:
            response['status_code'] = "500"
            response['message'] = "获取agent信息失败. {}".format(e)

        return JsonResponse(response)

class LogManagerView(APIView):
    """manage database log data"""

    @swagger_auto_schema(
        operation_description="ops-server delete log info",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['agent_ip', 'remote_addr', 'request', 'token'],
            properties={
                'agent_ip': openapi.Schema(type=openapi.TYPE_STRING),
                'remote_addr': openapi.Schema(type=openapi.TYPE_STRING),
                'request': openapi.Schema(type=openapi.TYPE_STRING),
                'token': openapi.Schema(type=openapi.IN_HEADER),
            },
        ),
        security=[]
    )
    @get_request_args
    def post(self, request, args):
        """docstring"""
        response = {}

        try:
            LOG.info(args)
            # 数据库更新数据，如果不存在，创建
            # RequestData.objects.update_or_create(remote_addr=remote_addr, remote_user=remote_user)
        except Exception as e:
            LOG.error("error info: %s", e)
            response['message'] = "ERROR: Update RequestData information to database failed!"
            response['status_code'] = 500
            return JsonResponse(response)

        response['message'] = "SUCCESS: Update RequestData information to database successful!"
        response['status_code'] = 200
        return JsonResponse(response)

