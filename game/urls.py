from django.urls import path
from game import views

urlpatterns = [
    # 게임모드 관련 문제 조회 url
    # 조회
    path('maps/', views.map_list),  # 맵 리스트
    path('maps/<int:map_pk>/', views.map_detail),   # 맵 리스트안 문제집
    path('maps/<int:map_pk>/sets/<int:problem_set_pk>/', views.problem_set_questions),  # 맵 안 문제집 안 문제들
    path('users/<int:user_pk>/problemsets/', views.user_problem_set),   # 특정 유저 문제집
    path('problemsets/user-created/', views.user_created_problem_set),   # madeBy 유저 문제집만 조회
    
    # 등록
    

]