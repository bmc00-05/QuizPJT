from django.db.models import Q
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from game.models import ProblemSet
from questions.models import Category
from .models import Profile, UserStats, UserCategoryStats, UserBadge, Badge
from .serializers import (
    UserProfileSerializer,
    UserStatsSerializer,
    UserCategoryStatsSerializer,
    RankingItemSerializer,
    BadgeDexSerializer,
    ProfileMemoSerializer,
)

# ✅ 상대 임포트로 변경 (노란줄 방지에 도움)
from .services.badge import grant_badge_to_user

User = get_user_model()


def _new_badges_payload(profile: Profile):
    """
    ✅ 아직 모달로 보여주지 않은(announced_at=None) 배지 목록
    """
    qs = (
        UserBadge.objects
        .filter(profile=profile, announced_at__isnull=True)
        .select_related("badge")
        .order_by("earned_at", "id")
    )
    return [
        {
            "id": ub.badge_id,
            "code": ub.badge.code,
            "name": ub.badge.name,
            "description": ub.badge.description,
            "icon": ub.badge.icon,
            "earned_at": ub.earned_at,
        }
        for ub in qs
    ]


def _award_welcome_home_if_first_visit(profile: Profile) -> bool:
    """
    ✅ '홈(프로필) 최초 진입'을 DB에서 1회만 감지해서 WELCOME_HOME 지급
    - True: 이번 요청에서 최초 진입 처리됨
    - False: 이미 방문 기록 있음
    """
    updated = Profile.objects.filter(
        pk=profile.pk,
        first_home_visited_at__isnull=True,
    ).update(first_home_visited_at=timezone.now())

    if updated:
        grant_badge_to_user(profile.user, "WELCOME_HOME")
        return True
    return False


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    로그인한 유저의 현재 프로필 정보를 반환 (user store fetchUser 용)
    - 여기서는 배지 지급/모달까지 넣지 않고, 가볍게 유지 추천
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


def _build_payload(target_user, include_new_badges: bool = False):
    profile, _ = Profile.objects.get_or_create(user=target_user)

    # ✅ 내 프로필(홈 진입)일 때만 최초 방문 처리 + new_badges 포함
    if include_new_badges:
        _award_welcome_home_if_first_visit(profile)

    profile = Profile.objects.select_related("equipped_badge", "user").get(pk=profile.pk)
    stats, _ = UserStats.objects.get_or_create(user=target_user)

    user_stats_qs = (
        UserCategoryStats.objects
        .filter(user=target_user)
        .select_related("category")
    )
    by_cat_id = {ucs.category_id: ucs for ucs in user_stats_qs}

    all_categories = Category.objects.all().order_by("id")

    merged = []
    for c in all_categories:
        ucs = by_cat_id.get(c.id)
        if ucs:
            merged.append(ucs)
        else:
            merged.append(UserCategoryStats(user=target_user, category=c, solved=0, correct=0, wrong=0))

    cat_data = UserCategoryStatsSerializer(merged, many=True).data

    payload = {
        "user": {"id": target_user.id},
        "profile": UserProfileSerializer(profile).data,
        "stats": UserStatsSerializer(stats).data,
        "category_stats": cat_data,
    }

    if include_new_badges:
        payload["new_badges"] = _new_badges_payload(profile)

    return payload


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile_stats(request):
    """
    ✅ 내 프로필(=홈/프로필 화면 진입 시 호출 추천)
    - WELCOME_HOME 최초 지급 트리거
    - new_badges 내려줌 (프론트는 모달 띄우고 ack 호출)
    """
    return Response(_build_payload(request.user, include_new_badges=True), status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def user_profile_stats(request, user_id: int):
    """
    다른 유저 프로필/통계 조회
    - ✅ new_badges 같은 개인 알림 정보는 포함하지 않음
    """
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    return Response(_build_payload(target, include_new_badges=False), status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ack_new_badges(request):
    """
    ✅ 프로필 화면에서 new_badges 모달을 '띄운 뒤' 닫을 때 호출
    Body:
      - codes: ["WELCOME_HOME", "FIRST_CLEAR"]  (선택)
        codes 없으면 announced_at=None 인 것 전부 처리
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    codes = request.data.get("codes")

    qs = UserBadge.objects.filter(profile=profile, announced_at__isnull=True)
    if codes:
        qs = qs.filter(badge__code__in=codes)

    updated = qs.update(announced_at=timezone.now())
    return Response({"acknowledged": updated}, status=200)


def _rank_ordering():
    return ["-total_experience", "-level", "-experience", "user_id"]


def _count_better_than(me: Profile) -> int:
    return Profile.objects.filter(
        Q(total_experience__gt=me.total_experience)
        | (Q(total_experience=me.total_experience) & Q(level__gt=me.level))
        | (Q(total_experience=me.total_experience) & Q(level=me.level) & Q(experience__gt=me.experience))
        | (Q(total_experience=me.total_experience) & Q(level=me.level) & Q(experience=me.experience) & Q(user_id__lt=me.user_id))
    ).count()


@api_view(["GET"])
@permission_classes([AllowAny])
def ranking(request):
    try:
        limit = int(request.query_params.get("limit", 50))
    except ValueError:
        limit = 50

    limit = max(1, min(limit, 200))

    qs = (
        Profile.objects
        .select_related("user")
        .order_by(*_rank_ordering())
    )

    top = list(qs[:limit])
    top_data = RankingItemSerializer(top, many=True).data

    items = []
    for p, row in zip(top, top_data):
        rank_num = _count_better_than(p) + 1
        items.append({**row, "rank": rank_num})

    me_payload = None
    if request.user.is_authenticated:
        me, _ = Profile.objects.get_or_create(user=request.user)
        me_rank = _count_better_than(me) + 1
        me_payload = {**RankingItemSerializer(me).data, "rank": me_rank}

    return Response({"limit": limit, "items": items, "me": me_payload})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_badge_dex(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    badges = list(Badge.objects.all().order_by("id"))

    owned_map = {
        ub.badge_id: ub.earned_at
        for ub in UserBadge.objects.filter(profile=profile).select_related("badge")
    }

    equipped_id = profile.equipped_badge_id

    data = []
    for b in badges:
        earned_at = owned_map.get(b.id)
        data.append({
            "id": b.id,
            "code": b.code,
            "name": b.name,
            "description": b.description,
            "icon": b.icon,
            "owned": earned_at is not None,
            "earned_at": earned_at,
            "equipped": (b.id == equipped_id),
        })

    return Response(data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def equip_badge(request):
    badge_id = request.data.get("badge_id")
    if not badge_id:
        return Response({"detail": "badge_id is required"}, status=400)

    profile, _ = Profile.objects.get_or_create(user=request.user)

    owned = UserBadge.objects.filter(profile=profile, badge_id=badge_id).exists()
    if not owned:
        return Response({"detail": "You don't own this badge"}, status=403)

    profile.equipped_badge_id = badge_id
    profile.save()

    return Response({"detail": "equipped", "badge_id": int(badge_id)}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unequip_badge(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.equipped_badge = None
    profile.save()
    return Response({"detail": "unequipped"}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_problemset_like(request, set_id: int):
    try:
        ps = ProblemSet.objects.get(id=set_id)
    except ProblemSet.DoesNotExist:
        return Response({"detail": "ProblemSet not found"}, status=404)

    user = request.user

    if ps.like_users.filter(id=user.id).exists():
        ps.like_users.remove(user)
        liked = False
    else:
        ps.like_users.add(user)
        liked = True

    return Response({
        "id": ps.id,
        "liked": liked,
        "like_count": ps.like_users.count(),
    }, status=200)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def my_memo(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return Response(ProfileMemoSerializer(profile).data, status=200)

    serializer = ProfileMemoSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=200)
