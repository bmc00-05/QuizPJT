from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ai.models import AIFeedbackRecord
from ai.services.ai_client import UpstreamAIError
from game.models import PlaySession, ProblemSet, SessionLog
from questions.models import Problem

FEEDBACK_URL = "/api/v1/ai/feedback/"
ECHO_URL = "/api/v1/ai/echo/"
QUOTA_URL = "/api/v1/ai/quota/"

# OpenAI 호환 응답 형태. 실제 네트워크를 타지 않기 위해 이 값을 주입한다.
MOCK_AI_RESPONSE = {"choices": [{"message": {"content": "AI 분석 결과입니다."}}]}


class AIBaseTest(TestCase):
    """오답 로그가 있는 인증 사용자를 준비한다."""

    fixtures = ["category", "map", "badge", "problemsets", "problems", "relative"]

    def setUp(self):
        # 스로틀 카운터와 전역 상한이 같은 캐시를 쓴다. 테스트 간 오염 방지.
        cache.clear()

        self.user = get_user_model().objects.create_user(
            username="ai_tester", password="pw12345!"
        )
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        session = PlaySession.objects.create(
            user=self.user, problem_set=ProblemSet.objects.first()
        )

        # build_category_accuracy_trend 는 [now - days, now) 구간을 조회한다.
        # solved_at 을 정확히 now 로 두면 요청 시각과 같아질 때 __lt 조건에서
        # 탈락해 테스트가 간헐적으로 실패한다. 경계에서 떨어뜨린다.
        solved_at = timezone.now() - timedelta(minutes=1)

        for problem in Problem.objects.all()[:3]:
            SessionLog.objects.create(
                user=self.user,
                session=session,
                problem=problem,
                selected_answer=1,
                is_correct=False,
                solved_at=solved_at,
            )

    def request_feedback(self):
        return self.client.post(FEEDBACK_URL, {"days": 7, "limit": 20}, format="json")


@override_settings(AI_DAILY_LIMIT=10000)
class DemoFallbackTest(AIBaseTest):
    """
    AI 응답을 받지 못했을 때 500 이 아니라 예시 응답으로 축소 동작하는지 검증한다.
    회귀하면 사용자에게 오류 화면이 그대로 노출되는 지점이다.
    """

    @override_settings(AI_API_KEY="")
    def test_missing_key_returns_demo_feedback(self):
        res = self.request_feedback()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["demo"])
        self.assertEqual(res.json()["model"], "demo")

    @override_settings(AI_API_KEY="")
    def test_demo_response_does_not_create_record(self):
        """데모 응답이 저장되면 사용자의 코칭 히스토리가 오염된다."""
        before = AIFeedbackRecord.objects.count()

        self.request_feedback()

        self.assertEqual(AIFeedbackRecord.objects.count(), before)

    @override_settings(AI_API_KEY="")
    def test_demo_response_keeps_real_category_trend(self):
        """
        category_trend 는 DB 만으로 계산되므로 데모 모드에서도 실제 값을 내려준다.
        AI 가 작성한 텍스트만 예시로 대체된다.
        """
        trend = self.request_feedback().json()["category_trend"]

        self.assertEqual(trend["days"], 7)
        self.assertTrue(trend["items"])
        self.assertEqual(sum(i["current_total"] for i in trend["items"]), 3)

    @override_settings(AI_API_KEY="")
    def test_missing_key_returns_demo_echo(self):
        res = self.client.post(ECHO_URL, {"input": "안녕"}, format="json")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["demo"])

    @override_settings(AI_API_KEY="dummy", DEBUG=True)
    @patch("ai.views.call_chat_completions")
    def test_upstream_error_exposes_cause_when_debug(self, mock_call):
        """로컬에서는 원인이 보여야 모델명 오타 같은 실수를 잡을 수 있다."""
        mock_call.side_effect = UpstreamAIError(404, "model not found")

        res = self.request_feedback()

        self.assertEqual(res.status_code, 502)
        self.assertEqual(res.json()["upstream_status"], 404)

    @override_settings(AI_API_KEY="dummy", DEBUG=False)
    @patch("ai.views.call_chat_completions")
    def test_upstream_error_falls_back_to_demo_in_production(self, mock_call):
        """
        무료 티어 호출량 초과(429)도 이 경로로 들어온다.
        사용자 잘못이 아니므로 오류 대신 예시 응답을 보여준다.
        """
        mock_call.side_effect = UpstreamAIError(429, "rate limit")

        res = self.request_feedback()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["demo"])

    @override_settings(AI_API_KEY="dummy")
    @patch("ai.views.call_chat_completions")
    def test_successful_call_creates_record(self, mock_call):
        mock_call.return_value = MOCK_AI_RESPONSE

        res = self.request_feedback()

        self.assertEqual(res.status_code, 200)
        self.assertNotIn("demo", res.json())
        self.assertEqual(AIFeedbackRecord.objects.count(), 1)
        self.assertEqual(
            AIFeedbackRecord.objects.first().feedback, "AI 분석 결과입니다."
        )


class ThrottleTest(AIBaseTest):
    """
    사용자당 제한은 429, 전역 상한은 데모.
    사용자 잘못인 경우에만 명시적으로 알린다는 설계다.
    """

    @override_settings(AI_API_KEY="", AI_DAILY_LIMIT=10000)
    def test_user_rate_limit_returns_429(self):
        """
        DEFAULT_THROTTLE_RATES 는 import 시점 클래스 속성이라
        override_settings 로 바꿀 수 없다. 실제 설정값(10/day)을 그대로 쓴다.
        """
        codes = [self.request_feedback().status_code for _ in range(12)]

        self.assertEqual(codes[:10], [200] * 10)
        self.assertEqual(codes[10], 429)

    @override_settings(AI_API_KEY="dummy", AI_DAILY_LIMIT=1)
    @patch("ai.views.call_chat_completions")
    def test_global_limit_falls_back_to_demo(self, mock_call):
        mock_call.return_value = MOCK_AI_RESPONSE

        first = self.request_feedback()
        second = self.request_feedback()

        # 상한 이내 -> 정상 응답
        self.assertEqual(first.status_code, 200)
        self.assertNotIn("demo", first.json())

        # 상한 초과 -> 429 가 아니라 데모
        self.assertEqual(second.status_code, 200)
        self.assertTrue(second.json()["demo"])
        self.assertEqual(AIFeedbackRecord.objects.count(), 1)


@override_settings(AI_API_KEY="", AI_DAILY_LIMIT=100)
class QuotaTest(AIBaseTest):
    def test_quota_reflects_usage(self):
        self.request_feedback()
        self.request_feedback()

        body = self.client.get(QUOTA_URL).json()

        self.assertEqual(body["user_used"], 2)
        self.assertEqual(body["user_remaining"], body["user_limit"] - 2)
        self.assertEqual(body["global_used"], 2)
        self.assertEqual(body["global_remaining"], 98)

    def test_quota_check_does_not_consume_quota(self):
        """잔여량을 확인하는 행위가 잔여량을 소모하면 안 된다."""
        self.request_feedback()
        before = self.client.get(QUOTA_URL).json()["user_used"]

        for _ in range(5):
            self.client.get(QUOTA_URL)

        after = self.client.get(QUOTA_URL).json()["user_used"]
        self.assertEqual(before, after)
