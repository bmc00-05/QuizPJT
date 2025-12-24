from django.urls import path
from . import views

urlpatterns = [
    path("echo/", views.ai_echo),
    path("feedback/", views.wrong_feedback),
    path("feedback/history/", views.feedback_history),
    path("feedback/history/<int:feedback_id>/", views.feedback_detail),
    path("feedback/history/<int:feedback_id>/delete/", views.feedback_delete),
]