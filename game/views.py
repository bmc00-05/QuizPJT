from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Map, ProblemSet
from .serializers import (
    MapSerializer, 
    MapProblemSetSerializer, 
    ProblemSetProblemSerializer, 
    ProblemSetSerializer,
    ProblemViewSerializer
)
from django.contrib.auth import get_user_model

# Create your views here.

# 맵 목록 호출
@api_view(['GET'])
def map_list(request):
    maps = Map.objects.all()
    serializer = MapSerializer(maps, many=True)
    return Response(serializer.data)

# 특정 맵 안에 존재하는 문제집 호출
@api_view(['GET'])
def map_detail(request, map_pk):
    maps = Map.objects.get(pk=map_pk)
    serializer = MapProblemSetSerializer(maps)
    return Response(serializer.data)

# 문제집 안 문제중 10문제 조회
@api_view(['GET'])
def problem_set_questions(request, problem_set_pk):
    # 1. 문제집 불러오기
    try:
        problem_set = ProblemSet.objects.get(pk=problem_set_pk)
    except ProblemSet.DoesNotExist:
        return Response({"error": "ProblemSet not found"}, status=status.HTTP_404_NOT_FOUND)

    # 2. 문제집 안의 문제들 가져오기
    problems = problem_set.problem.all()  # 문제집에 연결된 모든 문제
    # 3. 문제 10개만 랜덤으로 선택
    problems = problems.order_by('?')[:10]  # '?'는 랜덤 정렬

    # 4. 시리얼라이즈 후 반환
    serializer = ProblemViewSerializer(problems, many=True)
    return Response(serializer.data)

User = get_user_model()
@api_view(['GET'])
def user_problem_set(request, user_pk):
    # 1. 유저 존재 여부 확인
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # 2. 해당 유저가 만든 문제집 조회
    problemsets = ProblemSet.objects.filter(created_by=user)
    
    # 3. 시리얼라이즈
    serializer = ProblemSetSerializer(problemsets, many=True)
    return Response(serializer.data)

# 유저 제작 문제집들을 조회
@api_view(['GET'])
def user_created_problem_set(request):

    problemsets = ProblemSet.objects.filter(created_by_admin=False)
    
    serializer = ProblemSetSerializer(problemsets, many=True)
    return Response(serializer.data)