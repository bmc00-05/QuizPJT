from rest_framework import serializers
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    exp = serializers.IntegerField(source="experience")
    max_exp = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "level",
            "exp",
            "max_exp",
        ]

    def get_max_exp(self, obj):
        # 현재 레벨 기준 최대 경험치
        return obj.level * 100