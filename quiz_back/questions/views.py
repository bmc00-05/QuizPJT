from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import QuestionSerializer
from .models import Problem
from game.models import ProblemSet
from game.serializers import ProblemSetSerializer

# Create your views here.
# 개인 문제집 조회 및 문제집 프레임 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def problemset_create(request):
    if request.method == 'GET':
        problemsets = ProblemSet.objects.filter(created_by=request.user)
        serializer = ProblemSetSerializer(problemsets, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProblemSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# 문제집 상세 페이지, 수정, 삭제    
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def problemset_detail(request, set_pk):

    # 문제집 선택
    try:
        problemset = ProblemSet.objects.get(pk=set_pk, created_by=request.user)
    except ProblemSet.DoesNotExist:
        return Response({"detail": "문제집을 찾을 수 없습니다."}, status=404)

    # 조회
    if request.method == 'GET':
        serializer = ProblemSetSerializer(problemset)
        return Response(serializer.data)

    # 부분 수정(PATCH) → 이름/설명 수정
    elif request.method == 'PATCH':
        serializer = ProblemSetSerializer(problemset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # created_by는 이미 존재하므로 갱신되지 않음
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # 삭제
    elif request.method == 'DELETE':
        problemset.delete()
        return Response(status=204)
    
# 문제집 안 문제들에 대한 조회 및 수정 삭제
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def problemset_problems(request, set_pk):
    # 문제집 존재 여부 + 유저 소유권 체크
    try:
        problemset = ProblemSet.objects.get(pk=set_pk, created_by=request.user)
    except ProblemSet.DoesNotExist:
        return Response({"detail": "문제집을 찾을 수 없습니다."}, status=404)

    # 1) 문제 리스트 조회
    if request.method == 'GET':
        problems = problemset.problem.all()
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)

    # 2) 문제 생성 + 문제집 자동 추가
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            # 문제 생성 (유저 소유 문제)
            new_problem = serializer.save(created_by=request.user)
            # 문제집에 포함
            problemset.problem.add(new_problem)

            return Response({
                "detail": "문제 생성 완료",
                "problem": QuestionSerializer(new_problem).data
            }, status=201)

        return Response(serializer.errors, status=400)

    # 3) 문제 삭제 (문제집에서만 제거됨)
    elif request.method == 'DELETE':
        problem_id = request.data.get("problem_id")

        if not problem_id:
            return Response({"detail": "problem_id는 필수입니다."}, status=400)

        try:
            problem = Problem.objects.get(id=problem_id, created_by=request.user)
        except Problem.DoesNotExist:
            return Response({"detail": "해당 문제를 찾을 수 없거나 권한이 없습니다."}, status=404)

        problem.delete()

        return Response({"detail": "문제 삭제 완료"}, status=200)
    
