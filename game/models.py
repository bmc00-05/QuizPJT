from django.db import models
from django.conf import settings

# 문제집 테이블
class ProblemSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정 시간
    created_by = models.ForeignKey(     # 만든 유저 왜래키
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,      # 유저가 삭제돼도 문제집은 남김
        null=True,                       # 필수값 X
        blank=True,                      # admin 폼에서도 optional
        related_name="created_problem_sets",  # User.created_problem_sets로 User에서 접근 가능
        verbose_name="작성자"
    )
    questions = models.ManyToManyField( # 문제 M:N 참조
        'questions.Problem',  # questions 앱에 있는 Question 모델
        through='ProblemSetQuestion', # 기본 M:N 테이블 대신 스루 테이블 생성
        related_name='problem_sets' # 역참조 이름 설정
    )
    like_users = models.ManyToManyField(    # 좋아요, 유저 테이블 M:N 참조
        settings.AUTH_USER_MODEL,   
        related_name='liked_problem_sets',
        blank=True
    )
    created_by_admin = models.BooleanField(default = False) # 운영자 생성 여부
    class Meta:
        ordering = ['-created_at']  # 최신 문제집 우선
        verbose_name = "문제집"
        verbose_name_plural = "문제집 목록"
        
    def __str__(self):
        return self.title  

# 문제 x 문제집 중개 스루 테이블
class ProblemSetQuestion(models.Model):
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE) 
    question = models.ForeignKey('questions.Problem', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        unique_together = ('problem_set', 'question') # 문제집 문제 중복 방지
        ordering = ['order']  # order 기준 기본 정렬

# 게임 맵 테이블
class Map(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정 시간

    problem_sets = models.ManyToManyField(  # 문제집과 M:N 참조
        ProblemSet, 
        related_name='maps',  # 문제집에서 역참조: 문제집.maps
        blank=True
    )
    def __str__(self):
        return self.name
