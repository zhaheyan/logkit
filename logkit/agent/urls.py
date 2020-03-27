from django.urls import path

from agent import views

urlpatterns = [
    path("status", views.AgentView.as_view()),
    # 使用 django_crontab 实现健康检查
    # path("health_check", views.AgentHealthCheckView.as_view()),
]

