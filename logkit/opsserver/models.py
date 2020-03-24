"""opsserver.models

This module implements the Requests Models.

:copyright: (c) 2020 by <947201342@qq.com>.
:license: MIT, see LICENSE for more details.
:updateTime: 2020.03.18

nginx 日志内容
$remote_addr, $http_x_forwarded_for 记录客户端IP地址
$remote_user 记录客户端用户名称
$request 记录请求的URL和HTTP协议
$status 记录请求状态
$body_bytes_sent 发送给客户端的字节数，不包括响应头的大小； 该变量与Apache模块mod_log_config里的“%B”参数兼容。
$bytes_sent 发送给客户端的总字节数。
$connection 连接的序列号。
$connection_requests 当前通过一个连接获得的请求数量。
$msec 日志写入时间。单位为秒，精度是毫秒。
$pipe 如果请求是通过HTTP流水线(pipelined)发送，pipe值为“p”，否则为“.”。
$http_referer 记录从哪个页面链接访问过来的
$http_user_agent 记录客户端浏览器相关信息
$request_length 请求的长度（包括请求行，请求头和请求正文）。
$request_time 请求处理时间，单位为秒，精度毫秒； 从读入客户端的第一个字节开始，直到把最后一个字符发送给客户端后进行日志写入为止。
$time_iso8601 ISO8601标准格式下的本地时间。
"""
from django.db import models
from django.utils import timezone


class RequestData(models.Model):
    """request data
    agent_ip = models.CharField(max_length=16, blank=True)
    remote_addr = models.CharField(max_length=512, blank=True, null=True)
    http_x_forwarded_for = models.CharField(max_length=512, blank=True, null=True)
    remote_user = models.CharField(max_length=512, blank=True, null=True)
    request = models.CharField(max_length=512, blank=True, null=True)
    status = models.CharField(max_length=512, blank=True, null=True)
    body_bytes_sent = models.CharField(max_length=512, blank=True, null=True)
    bytes_sent = models.CharField(max_length=512, blank=True, null=True)
    connection = models.CharField(max_length=512, blank=True, null=True)
    connection_requests = models.CharField(max_length=512, blank=True, null=True)
    msec = models.CharField(max_length=512, blank=True, null=True)
    pipe = models.CharField(max_length=512, blank=True, null=True)
    http_referer = models.CharField(max_length=512, blank=True, null=True)
    request_length = models.CharField(max_length=512, blank=True, null=True)
    request_time = models.CharField(max_length=512, blank=True, null=True)
    """
    # id = models.IntegerField(primary_key=True, blank=True)
    id = models.AutoField(primary_key=True)
    agent_ip = models.CharField(max_length=32, blank=True)
    remote_addr = models.CharField(max_length=32, blank=True, null=True)
    request_time = models.CharField(max_length=32, blank=True, null=True)
    method = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)
    protocol = models.CharField(max_length=32, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    exist = models.BooleanField(blank=True, default=True)
    join_time = models.DateTimeField("加入时间", default=timezone.now)

    class Meta:
        """RequestData meta data"""
        managed = True
        db_table = "request_data"
        # ordering = ["-remote_addr"]


class IPCount(models.Model):
    """IP count info"""
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=512, blank=True)
    remote_addr = models.CharField(max_length=512, blank=True)
    remote_addr_number = models.IntegerField()

