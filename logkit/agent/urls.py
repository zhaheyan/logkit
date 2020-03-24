from django.urls import path

from agent import views

urlpatterns = [
    path("status", views.AgentView.as_view()),
    path("health_check", views.AgentHealthCheckView.as_view()),
]

