from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import QuestionSerializer
from game.models import ProblemSet
from game.serializers import ProblemSetSerializer

# Create your views here.
# 문제집 생성 CR
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def problemset_list_create(request):
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
    
# 개인 문제집 안 문제 CR
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def problem_list_create(request, problemset_pk):
    try:
        problemset = ProblemSet.objects.get(pk=problemset_pk, created_by=request.user)
    except ProblemSet.DoesNotExist:
        return Response({"error":"ProblemSet not found"}, status=404)

    if request.method == 'GET':
        problems = problemset.questions.all()
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            problem = serializer.save(created_by=request.user)
            # 문제집에 문제 추가
            problemset.questions.add(problem)  # << 여기 수정
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)