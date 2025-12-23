from django.db import models
from django.conf import settings

class AIFeedbackRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_feedbacks",
        db_index=True,
    )

    # 요청 파라미터 스냅샷
    days = models.PositiveIntegerField(default=7)
    limit = models.PositiveIntegerField(default=20)
    wrong_count = models.PositiveIntegerField(default=0)

    # 프론트에서 받은 추가 입력(최대 500자)
    extra_input = models.CharField(max_length=500, blank=True, default="")

    # AI 결과
    model_name = models.CharField(max_length=50, default="gpt-5-mini")
    feedback = models.TextField()

    # 프론트 그래프용 스냅샷
    category_trend = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"AIFeedbackRecord(u={self.user_id}, id={self.id})"
