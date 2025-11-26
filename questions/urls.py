from django.urls import path
from . import views

urlpatterns = [
    # 유저 개인 문제 관련 등록 및 조회
    path('problemsets/', views.problemset_list_create),
    path('problemsets/<int:problemset_pk>/problems/', views.problem_list_create),
]