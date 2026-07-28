"""
AI 호출 잔여량 조회.

두 제한의 리셋 방식이 다르다는 점에 주의한다.

  사용자당 제한 : 롤링 24시간
      DRF는 요청 시각 리스트를 캐시에 저장하고, 각 항목이 24시간 뒤 개별 만료된다.
      자정에 일괄 초기화되지 않는다. UI에 "자정 초기화"로 표기하면 사실과 다르다.

  전역 상한 : 달력 날짜
      ai.services.limits 가 timezone.localdate() 를 키로 쓰므로 자정에 초기화된다.
"""

import time

from django.conf import settings

from ai.services.limits import calls_today
from ai.throttles import AIRateThrottle


def get_quota(request) -> dict:
    throttle = AIRateThrottle()

    # UserRateThrottle.get_cache_key 는 view 를 참조하지 않는다.
    key = throttle.get_cache_key(request, None)

    now = time.time()
    history = [ts for ts in throttle.cache.get(key, []) if ts > now - throttle.duration]

    used_global = calls_today()

    return {
        "user_limit": throttle.num_requests,
        "user_used": len(history),
        "user_remaining": max(0, throttle.num_requests - len(history)),
        # 가장 오래된 호출이 만료되어 1회분이 복구되기까지 남은 초.
        # 여유가 있으면 0을 반환한다.
        "user_recover_in_sec": (
            max(0, int(history[-1] + throttle.duration - now))
            if len(history) >= throttle.num_requests
            else 0
        ),
        "global_limit": settings.AI_DAILY_LIMIT,
        "global_used": used_global,
        "global_remaining": max(0, settings.AI_DAILY_LIMIT - used_global),
    }
