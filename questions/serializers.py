from rest_framework import serializers
from .models import Category, Problem

# 문제 등록 시리얼 라이저
class  QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Problem
        fields = (
            'question',
            'choice1',
            'choice2',
            'choice3',
            'choice4',
            'answer',
            'difficulty',
            'explanation',
            'category',
        )
        read_only_fields = ['created_by_admin']