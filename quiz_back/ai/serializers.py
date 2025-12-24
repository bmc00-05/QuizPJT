from rest_framework import serializers
from ai.models import AIFeedbackRecord

class AIFeedbackRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFeedbackRecord
        fields = [
            "id",
            "days", "limit", "wrong_count",
            "extra_input",
            "model_name",
            "feedback",
            "category_trend",
            "created_at",
        ]