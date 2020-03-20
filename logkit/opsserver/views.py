"""opsserver.views

This module implements the Requests Views.
View is an logical management library, written in Python, for opsserver beings.

:copyright: (c) 2020 by <947201342@qq.com>.
:license: MIT, see LICENSE for more details.
:updateTime: 2020.03.18
"""
import json
import logging

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from opsserver.models import RequestData

LOG = logging.getLogger('opsserver')


def get_request_args(func):
    def _get_request_args(self, request):
        if request.method == 'GET':
            LOG.info(request.GET)
            args = request.GET
        else:
            # body = request.body
            body = request.data
            if body:
                try:
                    # args = json.loads(body)
                    args = body
                except Exception as e:
                    LOG.error(e)
                    # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                    args = request.POST
            else:
                args = request.POST
        return func(self, request, args)

    return _get_request_args


class OpsServerView(APIView):
    """View of ops-server."""

    @swagger_auto_schema(
        operation_description="ops-server post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['remote_addr', "remote_user"],
            properties={
                'remote_addr': openapi.Schema(type=openapi.TYPE_STRING),
                'remote_user': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[]
    )
    @get_request_args
    def post(self, request, args):
        """docstring"""
        response = {}

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
    @swagger_auto_schema(operation_description="partial_update description override",
                         responses={404: 'args not found'},
                         manual_parameters=[limit, page])
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


