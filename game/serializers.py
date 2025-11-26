from rest_framework import serializers
from .models import Map, ProblemSet
from questions.models import Problem

# 맵 목록 시리얼라이저
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'description',)

# 문제집 시리얼라이저
class ProblemSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemSet
        fields = ('id', 'title', 'description',)

# 맵 문제집 시리얼라이저
class MapProblemSetSerializer(serializers.ModelSerializer):

    problem_sets = ProblemSetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Map
        fields = ('id', 'name', 'description', 'problem_sets',)

# 문제 보기용 시리얼라이저
class ProblemViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'question', 'choice1', 'choice2', 'choice3', 'choice4',)

# 문제집 문제 시리얼라이저 (보기용)
class ProblemSetProblemSerializer(serializers.ModelSerializer):

    questions = ProblemViewSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemSet
        fields = ('id', 'title', 'description', 'questions',)
