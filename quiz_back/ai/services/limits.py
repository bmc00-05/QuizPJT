"""
AI 호출 전역 일일 상한.

사용자당 제한(ai.throttles.AIRateThrottle)과는 목적이 다르다.
- 사용자당 제한 : 한 사람이 과하게 쓰는 것을 막는다 → 429 로 명시적으로 알림
- 전역 상한     : 서비스 전체의 무료 티어 소진을 막는다 → 데모 응답으로 축소

캐시 백엔드 주의:
    Django 기본 캐시(locmem)는 프로세스마다 별도로 존재한다.
    gunicorn 을 워커 N개로 띄우면 카운터가 N개가 되어 실제 상한이 N배가 된다.
    settings.CACHES 에서 프로세스 간 공유되는 백엔드(DatabaseCache)를 쓴다.
"""

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

# 자정 경계에서 키가 먼저 사라지지 않도록 하루보다 넉넉히 잡는다.
_TTL_SECONDS = 60 * 60 * 26


def _today_key() -> str:
    return f"ai:calls:{timezone.localdate().isoformat()}"


def check_and_increment() -> bool:
    """
    전역 일일 호출 수를 1 증가시키고, 상한 이내이면 True.

    한계:
        DatabaseCache 의 incr 은 원자적이지 않다(조회 후 갱신).
        동시 요청이 몰리면 카운트가 한두 건 어긋날 수 있으나,
        근사치로 충분한 용도이므로 수용한다.

        또한 호출 '전에' 증가시키므로 AI 호출이 실패해도 카운트는 소모된다.
        장애 상황에서 재시도가 몰리는 것을 억제하는 효과가 있어 되돌리지 않는다.
    """
    key = _today_key()
    cache.add(key, 0, _TTL_SECONDS)  # 없을 때만 생성
    try:
        current = cache.incr(key)
    except ValueError:  # TTL 만료 등으로 키가 사라진 경우
        cache.set(key, 1, _TTL_SECONDS)
        current = 1

    return current <= settings.AI_DAILY_LIMIT


def calls_today() -> int:
    """현재까지의 전역 호출 수 (검증·모니터링용)."""
    return cache.get(_today_key(), 0)
