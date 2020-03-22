from django.urls import path

from agent import views

urlpatterns = [
    path("", views.AgentView.as_view()),
    path("operation", views.AgentManagerView.as_view()),
]

