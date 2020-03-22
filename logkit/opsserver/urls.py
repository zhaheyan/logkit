'''opsserver.urls

This module implements the Requests Urls.
Requests is an HTTP library, written in Python, for user beings. Basic GET and POST.

:copyright: (c) 2020 by <947201342@qq.com>.
:license: MIT, see LICENSE for more details.
:updateTime: 2020.03.18
'''

from django.urls import path

from opsserver import views

urlpatterns = [
    path("info", views.OpsServerView.as_view()),
    path("logs/ipcount", views.IPCountView.as_view()),
    path("logs/delete", views.LogManagerView.as_view()),
]

