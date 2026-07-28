import requests
from django.conf import settings


class UpstreamAIError(Exception):
    """AI 제공자로부터 오류 응답을 받은 경우."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class AIUnavailable(Exception):
    """
    키 미설정, 호출량 한도 초과 등 '정상적인 축소 동작'이 필요한 상황.

    서버 버그(Exception)와 구분하기 위한 전용 타입이다.
    호출부는 이 예외를 잡아 데모 응답으로 대체한다.
    """


def call_chat_completions(messages, model=None, timeout=30):
    api_key = settings.AI_API_KEY
    if not api_key:
        raise AIUnavailable("AI_API_KEY is not configured")

    model_name = model or settings.AI_MODEL

    payload = {
        "model": model_name,
        "messages": messages,
    }

    url = f"{settings.AI_BASE_URL}/chat/completions"

    try:
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )

        if res.status_code >= 400:
            raise UpstreamAIError(res.status_code, res.text)

        return res.json()

    except requests.RequestException as e:
        raise UpstreamAIError(502, str(e))
