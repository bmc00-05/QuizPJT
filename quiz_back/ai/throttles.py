from rest_framework.throttling import UserRateThrottle


class AIRateThrottle(UserRateThrottle):
    """
    AI 호출 전용 사용자당 요청 제한.

    요율은 settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["ai"] 에서 읽는다.

    ScopedRateThrottle 을 쓰지 않는 이유:
        @api_view 는 함수를 WrappedAPIView 로 감싸면서 renderer_classes /
        parser_classes / authentication_classes / throttle_classes /
        permission_classes / schema 여섯 개만 함수에서 복사한다.
        throttle_scope 는 전달되지 않으므로 ScopedRateThrottle 은
        scope 를 찾지 못하고 allow_request 가 조용히 True 를 반환한다.
        (예외도 경고도 없이 제한이 사라진다)

        scope 를 클래스 속성으로 고정하면 view 에 의존하지 않으므로
        함수형 뷰에서도 확실히 동작한다.
    """

    scope = "ai"
