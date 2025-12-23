# profiles/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth import get_user_model

from questions.models import Category
from .models import Profile, UserStats, UserCategoryStats, Badge, UserBadge

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    """
    ✅ 회원가입(User 생성) 시
    - Profile 생성
    - UserStats 생성
    - 현재 존재하는 모든 Category에 대해 UserCategoryStats 생성
    """
    if not created:
        return

    # 1) Profile
    # Profile에 username 필드가 없으니 user만 연결 (nickname은 선택)
    Profile.objects.get_or_create(user=instance)

    # 2) UserStats
    UserStats.objects.get_or_create(user=instance)

    # 3) UserCategoryStats: 현재 존재하는 Category 전부 0으로 초기화
    categories = Category.objects.all()
    UserCategoryStats.objects.bulk_create(
        [UserCategoryStats(user=instance, category=c) for c in categories],
        ignore_conflicts=True,
    )


@receiver(post_save, sender=Category)
def create_category_stats_for_all_users(sender, instance, created, **kwargs):
    """
    ✅ Category가 새로 추가될 때(created=True)
    - 기존 모든 유저에 대해 해당 Category의 UserCategoryStats를 생성
    """
    if not created:
        return

    # 유저가 많아질 수 있으니 iterator()로 메모리 절약
    users = User.objects.all().only("id").iterator()

    to_create = []
    batch_size = 1000

    for u in users:
        to_create.append(UserCategoryStats(user=u, category=instance))
        if len(to_create) >= batch_size:
            UserCategoryStats.objects.bulk_create(to_create, ignore_conflicts=True)
            to_create.clear()

    if to_create:
        UserCategoryStats.objects.bulk_create(to_create, ignore_conflicts=True)

DEFAULT_BADGE = {
    "code": "default",
    "name": "기본 뱃지",
    "description": "가입을 환영합니다!",
    "icon": "",  # 선택
}

@receiver(post_save, sender=User)
def create_profile_and_default_badge(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        profile, _ = Profile.objects.get_or_create(user=instance)

        badge, _ = Badge.objects.get_or_create(
            code="default",
            defaults={
                "name": "초심자",
                "description": "기본 제공 뱃지",
                "icon": "badges/default.png",
            },
        )

        UserBadge.objects.get_or_create(profile=profile, badge=badge)

        # (선택) 대표 뱃지까지 자동 장착하고 싶으면:
        # profile.equipped_badge = badge
        # profile.save(update_fields=["equipped_badge"])