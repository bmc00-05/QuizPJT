import requests
from django.conf import settings


class UpstreamAIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def call_chat_completions(messages, model=None, timeout=30):
    api_key = settings.AI_API_KEY
    if not api_key:
        raise RuntimeError("AI_API_KEY is not configured")

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
