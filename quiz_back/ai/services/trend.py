# ai/services/trend.py (원하는 위치에 파일로 분리 추천)
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from game.models import SessionLog

def _category_window(user, start, end):
    """
    기간 내 카테고리별 {total, correct, acc_pct} 집계
    """
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

    result = {}
    for r in rows:
        cid = r["problem__category_id"] or 0
        cname = r["problem__category__name"] or "미분류"
        total = r["total"] or 0
        correct = r["correct"] or 0
        acc_pct = round((correct / total) * 100, 1) if total > 0 else 0.0

        result[cid] = {
            "category_id": cid,
            "category_name": cname,
            "total": total,
            "correct": correct,
            "accuracy_pct": acc_pct,
        }
    return result


def get_category_accuracy_trend(user, days: int):
    """
    최근 days일 vs 직전 days일 카테고리별 정답률 변화량(Δ%p) 반환
    - 모든 카테고리 포함 (데이터 없으면 0으로)
    """
    now = timezone.now()
    cur_start = now - timedelta(days=days)
    prev_start = now - timedelta(days=days * 2)

    cur = _category_window(user, cur_start, now)
    prev = _category_window(user, prev_start, cur_start)

    keys = set(cur.keys()) | set(prev.keys())
    out = []

    for cid in keys:
        c = cur.get(cid, {"category_id": cid, "category_name": prev.get(cid, {}).get("category_name", "미분류"),
                          "total": 0, "correct": 0, "accuracy_pct": 0.0})
        p = prev.get(cid, {"category_id": cid, "category_name": c.get("category_name", "미분류"),
                           "total": 0, "correct": 0, "accuracy_pct": 0.0})

        out.append({
            "category_id": cid,
            "category_name": c["category_name"] or p["category_name"] or "미분류",
            "current_total": c["total"],
            "current_correct": c["correct"],
            "current_accuracy_pct": c["accuracy_pct"],
            "previous_total": p["total"],
            "previous_correct": p["correct"],
            "previous_accuracy_pct": p["accuracy_pct"],
            "delta_pp": round(c["accuracy_pct"] - p["accuracy_pct"], 1),  # ✅ 변화량(퍼센트포인트)
        })

    # 보기 좋게: 최근 기간에서 많이 푼 순으로 정렬(동률이면 변화량 큰 순)
    out.sort(key=lambda x: (x["current_total"], abs(x["delta_pp"])), reverse=True)

    return {
        "days": days,
        "items": out,
    }


def pack_category_trend_for_ai(trend: dict, min_total_each_window: int = 0) -> str:
    """
    AI에 넣을 텍스트로 압축.
    min_total_each_window > 0 이면 표본 너무 적은 카테고리는 제외(노이즈 방지)
    """
    lines = []
    days = trend["days"]

    for it in trend["items"]:
        if min_total_each_window > 0:
            if it["current_total"] < min_total_each_window and it["previous_total"] < min_total_each_window:
                continue

        lines.append(
            f"- {it['category_name']}: "
            f"{it['previous_accuracy_pct']}%({it['previous_correct']}/{it['previous_total']})"
            f" → {it['current_accuracy_pct']}%({it['current_correct']}/{it['current_total']})"
            f" (Δ {it['delta_pp']}%p)"
        )

    if not lines:
        return f"[카테고리별 정답률 변화]\n- 데이터가 충분하지 않습니다.\n"

    return "[카테고리별 정답률 변화]\n" + "\n".join(lines) + "\n"
