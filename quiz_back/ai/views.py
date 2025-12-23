from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from ai.models import AIFeedbackRecord
# (옵션) Profile에도 최신 정보 찍고 싶으면:
from profiles.models import Profile
from .serializers import AIFeedbackRecordSerializer

import json
import logging

from game.models import SessionLog
from ai.services.ai_client import call_chat_completions, UpstreamAIError

def extract_chat_text(data: dict) -> str:
    try:
        return (data["choices"][0]["message"]["content"] or "").strip()
    except Exception:
        return ""

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_echo(request):
    user_input = request.data.get("input", "")
    if not user_input:
        return Response({"detail": "input is required"}, status=400)

    messages = [
        {"role": "developer", "content": "Answer in Korean."},
        {"role": "user", "content": user_input},
    ]

    try:
        raw = call_chat_completions(messages=messages)
        return Response({"output": extract_chat_text(raw)}, status=200)

    except UpstreamAIError as e:
        # 개발 중엔 원인 노출, 배포 시엔 숨김
        if settings.DEBUG:
            return Response(
                {"detail": "AI upstream error", "upstream_status": e.status_code, "upstream_body": e.detail},
                status=502,
            )
        return Response({"detail": "AI service unavailable"}, status=502)

    except Exception as e:
        # 진짜 서버 코드 버그
        if settings.DEBUG:
            return Response({"detail": f"Server error: {e}"}, status=500)
        return Response({"detail": "Server error"}, status=500)
    
def get_choice(problem, n: int) -> str:
    """
    n(1~4)에 해당하는 선택지 텍스트 반환
    """
    if n not in (1, 2, 3, 4):
        return "-"
    return getattr(problem, f"choice{n}", "-") or "-"


def pack_wrong_logs_for_ai(logs) -> str:
    """
    AI에 넣기 좋은 텍스트로 '최소' 압축:
    - category/difficulty
    - 문제 지문(짧게)
    - 내가 고른 보기 텍스트 / 정답 보기 텍스트
    """
    lines = []

    for i, log in enumerate(logs, start=1):
        p = log.problem
        category = p.category.name if p.category else "-"

        # 안전 변환
        try:
            selected = int(log.selected_answer)
        except Exception:
            selected = 0

        correct = int(p.answer)

        chosen_txt = get_choice(p, selected)[:80]
        correct_txt = get_choice(p, correct)[:80]

        lines.append(
            f"[{i}] {category}/{p.difficulty}\n"
            f"Q: {(p.question or '')[:160]}\n"
            f"chosen: {selected}) {chosen_txt}\n"
            f"correct: {correct}) {correct_txt}"
        )

    return "\n\n".join(lines)

def build_category_accuracy_trend(user, days: int):
    """
    최근 days일 vs 직전 days일 카테고리별 정답률 변화(Δ%p) 계산
    """
    now = timezone.now()
    cur_start = now - timedelta(days=days)
    prev_start = now - timedelta(days=days * 2)

    def window(start, end):
        rows = (
            SessionLog.objects
            .filter(user=user, solved_at__gte=start, solved_at__lt=end)
            .select_related("problem", "problem__category")
            .values("problem__category_id", "problem__category__name")
            .annotate(
                total=Count("id"),
                correct=Count("id", filter=Q(is_correct=True)),
            )
        )
        out = {}
        for r in rows:
            cid = r["problem__category_id"] or 0
            name = r["problem__category__name"] or "미분류"
            total = r["total"] or 0
            correct = r["correct"] or 0
            acc = round((correct / total) * 100, 1) if total > 0 else 0.0
            out[cid] = {
                "category_id": cid,
                "category_name": name,
                "total": total,
                "correct": correct,
                "accuracy_pct": acc,
            }
        return out

    cur = window(cur_start, now)
    prev = window(prev_start, cur_start)

    keys = set(cur.keys()) | set(prev.keys())

    items = []
    for cid in keys:
        c = cur.get(cid, {"category_id": cid, "category_name": prev.get(cid, {}).get("category_name", "미분류"),
                        "total": 0, "correct": 0, "accuracy_pct": 0.0})
        p = prev.get(cid, {"category_id": cid, "category_name": c.get("category_name", "미분류"),
                        "total": 0, "correct": 0, "accuracy_pct": 0.0})

        items.append({
            "category_id": cid,
            "category_name": c["category_name"] or p["category_name"] or "미분류",
            "current_total": c["total"],
            "current_correct": c["correct"],
            "current_accuracy_pct": c["accuracy_pct"],
            "previous_total": p["total"],
            "previous_correct": p["correct"],
            "previous_accuracy_pct": p["accuracy_pct"],
            "delta_pp": round(c["accuracy_pct"] - p["accuracy_pct"], 1),
        })

    # 최근 기간에서 많이 푼 순으로
    items.sort(key=lambda x: x["current_total"], reverse=True)

    return {"days": days, "items": items}


def pack_category_trend_for_ai(trend: dict, min_total: int = 0) -> str:
    """
    AI 입력용 텍스트로 압축
    - min_total: (최근/이전) 둘 다 너무 적으면 제외하고 싶을 때
    """
    days = trend.get("days", 7)
    lines = [f"[카테고리별 정답률 변화: 최근 {days}일 vs 직전 {days}일]"]

    for it in trend.get("items", []):
        if min_total > 0 and it["current_total"] < min_total and it["previous_total"] < min_total:
            continue

        lines.append(
            f"- {it['category_name']}: "
            f"{it['previous_accuracy_pct']}%({it['previous_correct']}/{it['previous_total']})"
            f" → {it['current_accuracy_pct']}%({it['current_correct']}/{it['current_total']})"
            f" (Δ {it['delta_pp']}%p)"
        )

    if len(lines) == 1:
        lines.append("- 데이터가 충분하지 않습니다.")

    return "\n".join(lines)

MAX_EXTRA_LEN = 500

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wrong_feedback(request):
    """
    최근 N일 오답을 AI에 보내 피드백 받기
    + 카테고리별 정답률 변화 주입
    + (추가) 사용자 extra_input(최대 500자) 주입
    """
    # ✅ 기본 파라미터
    try:
        days = int(request.data.get("days", 7))
    except Exception:
        days = 7

    try:
        limit = int(request.data.get("limit", 20))
    except Exception:
        limit = 20

    limit = min(max(limit, 1), 20)

    # ✅ 추가 입력(프론트 textarea)
    extra_input = (request.data.get("extra_input") or "").strip()
    extra_input = extra_input[:MAX_EXTRA_LEN]  # ✅ 백엔드에서도 강제

    since = timezone.now() - timedelta(days=days)

    logs = (
        SessionLog.objects
        .select_related("problem", "problem__category")
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .order_by("-solved_at")[:limit]
    )

    if not logs:
        # extra_input은 있어도 오답이 없으면 코칭 재료가 부족하니까 그대로 안내
        return Response(
            {"detail": f"최근 {days}일 내 오답이 없습니다.", "count": 0, "from_days": days},
            status=200
        )

    # ✅ 카테고리별 정답률 변화
    cat_trend = build_category_accuracy_trend(request.user, days)
    cat_trend_text = pack_category_trend_for_ai(cat_trend, min_total=0)

    # ✅ 오답 압축 텍스트
    packed = pack_wrong_logs_for_ai(logs)

    # ✅ 추가 요청 텍스트(있을 때만)
    extra_block = ""
    if extra_input:
        extra_block = (
            "\n\n[사용자 추가 요청]\n"
            f"{extra_input}\n"
            "- 위 요청을 반드시 반영하되, 오답/정답률 데이터와 충돌하면 데이터 기반 코칭을 우선하라."
        )

    messages = [
        {
            "role": "developer",
            "content": (
                "너는 뛰어난 CS 학습 코치다. 반드시 한국어로만 답해라.\n"
                "아래 '카테고리별 정답률 변화'와 '오답 요약' 그리고 (있다면) '사용자 추가 요청'을 보고 짧게 피드백하라.\n"
                "규칙:\n"
                "- 전체 700~900자 이내\n"
                "- 섹션은 4개(1~4) 유지\n"
                "- 각 섹션은 최대 3개 bullet만\n"
                "- 불필요한 서론 금지, 바로 답만\n"
                "- 정답률이 하락한 카테고리는 원인 가설 + 처방을 우선 제시\n"
                "- 첫번째 섹션에는 입력 받은 데이터를 기반으로 객관적인 분석을 진행하고 총괄적으로 요약한 내용을 나타낸다.\n"
                "- 사용자 추가 요청이 있으면 마지막 섹션(4)에서 우선 반영 요약을 포함"
            )
        },
        {
            "role": "user",
            "content": (
                f"{cat_trend_text}\n\n"
                f"[최근 {days}일 오답 {len(logs)}개]\n\n{packed}"
                f"{extra_block}"
            )
        }
    ]

    model_name = "gpt-5-mini"

    try:
        logger = logging.getLogger(__name__)

        payload = {
            "model": model_name,
            "messages": messages,
            "timeout": 60,
        }

        # ✅ 디버그 시 실제로 AI에 보내는 payload 확인 가능
        if settings.DEBUG:
            logger.info("[AI REQUEST PAYLOAD]\n%s", json.dumps(payload, ensure_ascii=False, indent=2))

        raw = call_chat_completions(**payload)
        feedback_text = extract_chat_text(raw)
        extra_input = (request.data.get("extra_input") or "").strip()
        extra_input = extra_input[:500]

        AIFeedbackRecord.objects.create(
            user=request.user,
            days=days,
            limit=limit,
            wrong_count=len(logs),
            extra_input=extra_input,
            model_name=model_name,
            feedback=feedback_text,
            category_trend=cat_trend,
        )

        return Response(
            {
                "count": len(logs),
                "from_days": days,
                "model": model_name,
                "category_trend": cat_trend,     # 프론트 그래프용
                "extra_input": extra_input,      # 프론트 디버그/표시용(원하면 제거)
                "feedback": feedback_text,
            },
            status=200
        )

    except UpstreamAIError as e:
        if settings.DEBUG:
            return Response(
                {
                    "detail": "AI upstream error",
                    "upstream_status": e.status_code,
                    "upstream_body": e.detail
                },
                status=502
            )
        return Response({"detail": "AI service unavailable"}, status=502)

    except Exception as e:
        if settings.DEBUG:
            return Response({"detail": f"Server error: {e}"}, status=500)
        return Response({"detail": "Server error"}, status=500)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feedback_history(request):
    """
    내 AI 코칭 기록 리스트(과거 기록 조회)
    - page(1부터), page_size(기본 10, 최대 50)
    """
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))
    page = max(page, 1)
    page_size = min(max(page_size, 1), 50)

    qs = AIFeedbackRecord.objects.filter(user=request.user).order_by("-created_at")

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size

    items = qs[start:end]
    data = AIFeedbackRecordSerializer(items, many=True).data

    return Response(
        {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "items": data,
        },
        status=200
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feedback_detail(request, feedback_id: int):
    """
    특정 코칭 기록 상세 조회
    """
    obj = AIFeedbackRecord.objects.filter(user=request.user, id=feedback_id).first()
    if not obj:
        return Response({"detail": "not found"}, status=404)

    return Response(AIFeedbackRecordSerializer(obj).data, status=200)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def feedback_delete(request, feedback_id: int):
    obj = AIFeedbackRecord.objects.filter(user=request.user, id=feedback_id).first()
    if not obj:
        return Response({"detail": "not found"}, status=404)

    obj.delete()
    return Response({"detail": "deleted"}, status=200)