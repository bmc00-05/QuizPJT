from datetime import timedelta

from django.utils import timezone
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Map, ProblemSet, PlaySession, SessionLog
from questions.models import Problem
from .serializers import (
    MapSerializer,
    MapProblemSetSerializer,
    ProblemSetSerializer,
    ProblemViewSerializer,
    RecentWrongLogSerializer,
)
from profiles.models import Profile
from profiles.services.stats_service import update_stats_from_log


# ==============================================================================================
# 공통 QuerySet (like_count / problem_count annotate)
# ==============================================================================================
def problemset_annotated_qs():
    return (
        ProblemSet.objects
        .select_related("created_by")
        .annotate(
            like_count=Count("like_users", distinct=True),
            problem_count=Count("problem", distinct=True),
        )
        .order_by("-created_at")
    )


# ==============================================================================================
# 메인 모드 구현
# ==============================================================================================

# 맵 목록 호출
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def map_list(request):
    maps = Map.objects.all()
    serializer = MapSerializer(maps, many=True)
    return Response(serializer.data)


# 특정 맵 안에 존재하는 문제집 호출 (✅ 문제집에 like_count / problem_count 반영 + context 전달)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def map_detail(request, map_pk):
    maps = get_object_or_404(
        Map.objects.prefetch_related(
            Prefetch("problem_sets", queryset=problemset_annotated_qs())
        ),
        pk=map_pk
    )
    serializer = MapProblemSetSerializer(maps, context={"request": request})
    return Response(serializer.data)


# ✅ 문제집 좋아요 토글
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def problemset_like(request, problem_set_pk):
    ps = get_object_or_404(ProblemSet, pk=problem_set_pk)
    user = request.user

    if ps.like_users.filter(pk=user.pk).exists():
        ps.like_users.remove(user)
        liked = False
    else:
        ps.like_users.add(user)
        liked = True

    return Response({
        "problemset_id": ps.id,
        "liked": liked,
        "like_count": ps.like_users.count(),
    }, status=status.HTTP_200_OK)


# 게임 플레이 세션 생성 및 문제 조회
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def start_play_session(request):
    problem_set_id = request.data.get("problem_set_id")

    if problem_set_id is None:
        return Response({"error": "problem_set_id는 필수값입니다."}, status=400)

    # 🧹 기존 0문제 세션 정리
    PlaySession.objects.filter(user=request.user, solved_count=0).delete()

    # 문제집 조회
    try:
        problem_set = ProblemSet.objects.get(id=problem_set_id)
    except ProblemSet.DoesNotExist:
        return Response({"error": "해당 문제집이 존재하지 않습니다."}, status=404)

    # ✅ 문제 수 체크
    available_count = problem_set.problem.count()
    if available_count == 0:
        return Response({"error": "문제집에 문제가 없습니다."}, status=400)

    pick_count = min(10, available_count)  # 기본 10, 부족하면 있는 만큼

    # 1) PlaySession 생성
    session = PlaySession.objects.create(
        user=request.user,
        problem_set=problem_set,
        total_problems=pick_count,
    )

    # 2) 문제집에서 문제 랜덤 선택
    problems = problem_set.problem.order_by("?")[:pick_count]

    # 세션에 문제 저장
    session.selected_problems.set(problems)

    # 3) 프론트 반환 데이터
    serialized = ProblemViewSerializer(problems, many=True).data

    return Response({
        "session_id": session.id,
        "total_problems": pick_count,
        "available_count": available_count,
        "problems": serialized
    }, status=201)


# 퀴즈 정답 채점 함수
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def check_answer(request):
    try:
        session_id = request.data.get("session_id")
        question_id = request.data.get("question_id")
        selected = request.data.get("selected")

        if session_id is None or question_id is None or selected is None:
            return Response(
                {"error": "session_id, question_id, selected는 필수값입니다."},
                status=400
            )

        try:
            selected_int = int(selected)
        except (TypeError, ValueError):
            return Response({"error": "selected는 숫자여야 합니다."}, status=400)

        # 🔐 세션 조회 & 유저 확인
        session = PlaySession.objects.get(id=session_id, user=request.user)

        if session.is_completed or session.expired:
            return Response({"error": "이미 종료된 세션입니다."}, status=400)

        # 문제 조회
        question = Problem.objects.get(id=question_id)

        # 🧩 이 문제가 세션에 포함된 문제인지 확인
        if not session.selected_problems.filter(id=question.id).exists():
            return Response({"error": "세션과 관련 없는 문제입니다."}, status=400)

        # 🎯 채점
        is_correct = (question.answer == selected_int)

        # 📝 SessionLog 저장
        try:
            log = SessionLog.objects.create(
                user=request.user,
                session=session,
                problem=question,
                selected_answer=selected_int,
                is_correct=is_correct,
                solved_at=timezone.now()
            )
        except IntegrityError:
            return Response({"error": "이미 제출한 문제입니다."}, status=400)

        # ✅ 통계 업데이트
        update_stats_from_log(log)

        # answered_count
        answered_count = SessionLog.objects.filter(session=session).count()

        # 🔥 세션 상태 업데이트 (현재 로직: 맞춘 개수만 solved_count 증가)
        if is_correct:
            session.solved_count += 1

        session_completed_result = None

        if answered_count >= session.total_problems:
            session.mark_completed()

            correct = session.solved_count
            total = session.total_problems
            score = correct * 20

            profile, _ = Profile.objects.get_or_create(user=request.user)

            before_level = profile.level
            before_exp = profile.experience

            profile.add_experience(score)

            session_completed_result = {
                "score": score,
                "correct": correct,
                "total": total,
                "level_before": before_level,
                "level_after": profile.level,
                "before_exp": before_exp,
                "experience": profile.experience,
                "leveled_up": profile.level > before_level,
            }
        else:
            session.save()

        return Response({
            "correct": is_correct,
            "correct_answer": question.answer,
            "explanation": question.explanation,
            "is_completed": session.is_completed,
            "solved_count": session.solved_count,
            "total_problems": session.total_problems,
            "session_result": session_completed_result
        }, status=status.HTTP_200_OK)

    except PlaySession.DoesNotExist:
        return Response(
            {"error": "잘못된 session_id이거나 접근 권한이 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )

    except Problem.DoesNotExist:
        return Response(
            {"error": "해당 문제를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )


# ==============================================================================================
# 유저 모드 구현
# ==============================================================================================

User = get_user_model()

@api_view(["GET"])
def user_problem_set(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    problemsets = problemset_annotated_qs().filter(created_by=user)
    serializer = ProblemSetSerializer(problemsets, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def user_created_problem_set(request):
    problemsets = problemset_annotated_qs().filter(created_by_admin=False)
    serializer = ProblemSetSerializer(problemsets, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recent_wrong_logs(request):
    days = 7
    limit = 30
    since = timezone.now() - timedelta(days=days)

    qs = (
        SessionLog.objects
        .filter(
            user=request.user,
            is_correct=False,
            solved_at__gte=since,
        )
        .select_related("problem", "problem__category")
        .order_by("-solved_at")[:limit]
    )

    items = RecentWrongLogSerializer(qs, many=True).data

    wrong_by_difficulty = (
        SessionLog.objects
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .values("problem__difficulty")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )

    wrong_by_category = (
        SessionLog.objects
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .values("problem__category_id", "problem__category__name")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )

    return Response({
        "window_days": days,
        "limit": limit,
        "count": len(items),
        "items": items,
        "stats": {
            "wrong_by_difficulty": list(wrong_by_difficulty),
            "wrong_by_category": list(wrong_by_category),
        }
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 로그인 없이도 보이게 하려면 AllowAny로 바꿔도 됨
def problemset_list(request):
    sort = request.query_params.get("sort", "recent")

    qs = problemset_annotated_qs()  # ✅ like_count, problem_count 이미 annotate 되어 있음

    if sort == "like":
        qs = qs.order_by("-like_count", "-created_at")
    else:
        qs = qs.order_by("-created_at")

    serializer = ProblemSetSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)