import math
from rest_framework import serializers
from .models import Profile, UserCategoryStats, UserStats, Badge


class EquippedBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "code", "name", "icon"]

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    exp = serializers.IntegerField(source="experience", read_only=True)
    max_exp = serializers.SerializerMethodField()

    # ✅ 대표 뱃지(선택): FK면 PK만 내려도 되고, 상세도 가능
    equipped_badge_id = serializers.IntegerField(source="equipped_badge.id", read_only=True)
    equipped_badge = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "level",
            "exp",
            "max_exp",
            "equipped_badge_id",
            "equipped_badge",   # ✅ 반드시 포함
        ]

    def get_max_exp(self, obj):
        return obj.level * 100

    def get_equipped_badge(self, obj):
        b = getattr(obj, "equipped_badge", None)
        if not b:
            return None
        return {
            "id": b.id,
            "code": b.code,
            "name": b.name,
            "icon": b.icon,
        }
    
class UserStatsSerializer(serializers.ModelSerializer):
    accuracy = serializers.SerializerMethodField()
    accuracy_pct = serializers.SerializerMethodField()

    class Meta:
        model = UserStats
        fields = [
            "total_solved",
            "total_correct",
            "total_wrong",
            "accuracy",
            "accuracy_pct",
            "last_solved_at",
            "updated_at",
        ]

    def get_accuracy(self, obj):
        return 0.0 if obj.total_solved == 0 else (obj.total_correct / obj.total_solved)

    def get_accuracy_pct(self, obj):
        acc = self.get_accuracy(obj)
        return round(acc * 100, 1)


class UserCategoryStatsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    accuracy = serializers.SerializerMethodField()
    accuracy_pct = serializers.SerializerMethodField()
    proficiency_score = serializers.SerializerMethodField()

    class Meta:
        model = UserCategoryStats
        fields = [
            "category_id",
            "category_name",
            "solved",
            "correct",
            "wrong",
            "accuracy",
            "accuracy_pct",
            "proficiency_score",
            "last_solved_at",
            "updated_at",
        ]

    def get_accuracy(self, obj):
        return 0.0 if obj.solved == 0 else (obj.correct / obj.solved)

    def get_accuracy_pct(self, obj):
        return round(self.get_accuracy(obj) * 100, 1)

    def get_proficiency_score(self, obj):
        solved = obj.solved or 0
        correct = obj.correct or 0

        if solved <= 0:
            return 0.0

        smoothed = (correct + 2) / (solved + 4)          # 0~1
        confidence = 1 - math.exp(-solved / 20.0)        # 0~1
        score = 100.0 * smoothed * confidence            # 0~100

        return round(score, 1)
    
class RankingItemSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    equipped_badge = EquippedBadgeSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ["user_id", "username", "level", "experience", "total_experience", "equipped_badge"]




class BadgeDexSerializer(serializers.ModelSerializer):
    owned = serializers.BooleanField(read_only=True)
    earned_at = serializers.DateTimeField(read_only=True, allow_null=True)
    equipped = serializers.BooleanField(read_only=True)

    class Meta:
        model = Badge
        fields = ["id", "code", "name", "description", "icon", "owned", "earned_at", "equipped"]

