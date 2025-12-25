from django.utils import timezone
from profiles.models import Badge, UserBadge, Profile  # 앱 경로는 네 프로젝트에 맞게

def grant_badge_to_user(user, badge_code: str) -> bool:
    """
    뱃지 지급(중복 방지)
    - True: 이번에 새로 지급됨
    - False: 이미 가지고 있거나, 뱃지 코드가 없음
    """
    profile, _ = Profile.objects.get_or_create(user=user)

    badge = Badge.objects.filter(code=badge_code).first()
    if not badge:
        return False

    # uniq_profile_badge 덕분에 중복 지급 자동 방지
    obj, created = UserBadge.objects.get_or_create(
        profile=profile,
        badge=badge,
        defaults={"earned_at": timezone.now()},
    )
    return created