from django.db import models
from django.conf import settings
from questions.models import Category 

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # 표시명(선택)
    nickname = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    # ✅ 회원가입 후 "홈(프로필) 최초 진입" 기록 (WELCOME_HOME 지급 트리거용)
    first_home_visited_at = models.DateTimeField(null=True, blank=True)

    # 레벨/경험치
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)        # 현재 레벨의 경험치
    total_experience = models.PositiveIntegerField(default=0, db_index=True)  # 누적 경험치(랭킹용)

    # 메모/장착 뱃지
    memo = models.TextField(blank=True, default="")
    equipped_badge = models.ForeignKey(
        "Badge",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="equipped_profiles",
    )

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display = self.nickname or self.user.username
        return f"{display} ({self.user.username})"

    @staticmethod
    def required_exp_for_level(level: int) -> int:
        """
        다음 레벨업에 필요한 경험치
        현재 로직: level * 100
        """
        if level < 1:
            level = 1
        return level * 100

    def add_experience(self, amount: int):
        """
        경험치/레벨 반영
        - amount <= 0이면 변화 없음
        - 결과를 dict로 반환 (check_answer에서 레벨업/LEVEL_10 배지 판단에 유용)
        """
        level_before = self.level
        exp_before = self.experience
        total_before = self.total_experience

        if amount <= 0:
            return {
                "level_before": level_before,
                "level_after": self.level,
                "exp_before": exp_before,
                "exp_after": self.experience,
                "total_before": total_before,
                "total_after": self.total_experience,
                "leveled_up": False,
            }

        self.total_experience += amount
        self.experience += amount

        # 레벨업 처리
        while self.experience >= self.required_exp_for_level(self.level):
            self.experience -= self.required_exp_for_level(self.level)
            self.level += 1

        # ✅ updated_at(auto_now)까지 확실히 갱신하려면 update_fields에 updated_at 포함
        self.save(update_fields=["total_experience", "experience", "level", "updated_at"])

        return {
            "level_before": level_before,
            "level_after": self.level,
            "exp_before": exp_before,
            "exp_after": self.experience,
            "total_before": total_before,
            "total_after": self.total_experience,
            "leveled_up": self.level > level_before,
        }
    
class UserStats(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stats"
    )

    total_solved = models.PositiveIntegerField(default=0)
    total_correct = models.PositiveIntegerField(default=0)
    total_wrong = models.PositiveIntegerField(default=0)

    last_solved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def accuracy(self):
        return 0.0 if self.total_solved == 0 else (self.total_correct / self.total_solved)

    def __str__(self):
        return f"Stats({self.user_id})"
    


class UserCategoryStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="category_stats"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="user_stats"
    )

    solved = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong = models.PositiveIntegerField(default=0)

    last_solved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "category"], name="uniq_user_category_stats")
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["category"]),
        ]

    @property
    def accuracy(self):
        return 0.0 if self.solved == 0 else (self.correct / self.solved)

    def __str__(self):
        return f"CatStats(u={self.user_id}, c={self.category_id})"



class Badge(models.Model):
    code = models.SlugField(max_length=50, unique=True)   # 예: "first_clear"
    name = models.CharField(max_length=50)                # 표시 이름
    description = models.CharField(max_length=200, blank=True, default="")
    icon = models.CharField(max_length=200, blank=True, default="")  # 아이콘 url/파일경로(선택)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class UserBadge(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="user_badges",
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="user_badges",
    )
    earned_at = models.DateTimeField(auto_now_add=True)
    announced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "badge"], name="uniq_profile_badge")
        ]

    def __str__(self):
        return f"{self.profile_id}-{self.badge.code}"