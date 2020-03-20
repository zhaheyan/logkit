"""logkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers, permissions
# 导入辅助函数get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from opsserver import views as opsserver_views

# 路由
router = routers.DefaultRouter()
router.register('opsserver', opsserver_views.OpsServerView, 'opsserver')

schema_view = get_schema_view(
   openapi.Info(
      title="OpsServer API",
      default_version='v1.0',
      description="ops-server接口文档",
      terms_of_service="https://localhost:8080/redoc/",
      contact=openapi.Contact(email="315675275@qq.com"),
      license=openapi.License(name="Apache License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 配置django-rest-framwork API路由
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 配置drf-yasg路由
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('opsserver/', include('opsserver.urls')),
    # path('', TemplateView.as_view(template_name="index.html")),
]

