from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)  # 선택 사항

    def __str__(self):
        return self.name
    
class Problem(models.Model):
    # 문제, 선택지, 정답 필드
    question = models.TextField()
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    
    answer = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    help_text="정답 선택지 번호 (1~4)"
    )
    explanation = models.TextField()
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    help_text="난이도 (1~3)"
    )
    # 난이도 선택지
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]
    # 난이도 필드
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=EASY,
        help_text="문제 난이도"
    )
    # 운영자 생성 여부
    created_by_admin = models.BooleanField(
        default = False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 카테고리 필드 설정
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # 카테고리가 삭제되도 문제는 유지
        null=True,
        blank=True,
        related_name='questions'
    )
    def __str__(self):
        return self.question

    

        
