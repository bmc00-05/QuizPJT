from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile


class ExperienceTest(TestCase):
    """
    Profile.add_experience 의 경험치·레벨업 계산 검증.

    레벨업 규칙: required_exp_for_level(level) = level * 100
        레벨 1 -> 100, 레벨 2 -> 200, 레벨 3 -> 300 ...

    수동으로 확인하려면 문제를 수십 개 풀어야 하는 로직이라 테스트 가치가 높다.
    """

    def setUp(self):
        # Profile 은 profiles/signals.py 의 post_save 시그널로 자동 생성된다.
        user = get_user_model().objects.create_user(
            username="exp_tester", password="pw12345!"
        )
        self.profile = user.profile

    # ------------------------------------------------------------ 입력 방어

    def test_zero_amount_changes_nothing(self):
        result = self.profile.add_experience(0)

        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.experience, 0)
        self.assertEqual(self.profile.total_experience, 0)
        self.assertFalse(result["leveled_up"])

    def test_negative_amount_is_ignored(self):
        result = self.profile.add_experience(-50)

        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.total_experience, 0)
        self.assertFalse(result["leveled_up"])

    # ------------------------------------------------------------ 레벨업 경계

    def test_below_threshold_does_not_level_up(self):
        result = self.profile.add_experience(50)

        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.experience, 50)
        self.assertFalse(result["leveled_up"])

    def test_exact_threshold_levels_up(self):
        """
        경계값. while 조건이 >= 가 아니라 > 였다면 여기서 실패한다.
        """
        result = self.profile.add_experience(100)

        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.experience, 0)
        self.assertEqual(self.profile.total_experience, 100)
        self.assertTrue(result["leveled_up"])

    def test_surplus_carries_over_after_level_up(self):
        self.profile.add_experience(150)

        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.experience, 50)

    def test_multi_level_up_in_single_call(self):
        """
        100 + 200 + 300 + 400 = 1000 이므로 레벨 5, 잔여 경험치 0.
        while 루프가 4회 도는 것과 경계 처리를 함께 검증한다.
        """
        result = self.profile.add_experience(1000)

        self.assertEqual(self.profile.level, 5)
        self.assertEqual(self.profile.experience, 0)
        self.assertEqual(self.profile.total_experience, 1000)
        self.assertTrue(result["leveled_up"])

    # ------------------------------------------------------------ 누적·반환값

    def test_total_experience_accumulates_across_calls(self):
        self.profile.add_experience(50)
        self.profile.add_experience(50)

        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.experience, 0)
        self.assertEqual(self.profile.total_experience, 100)

    def test_return_value_reports_before_and_after(self):
        result = self.profile.add_experience(100)

        self.assertEqual(result["level_before"], 1)
        self.assertEqual(result["level_after"], 2)
        self.assertEqual(result["total_before"], 0)
        self.assertEqual(result["total_after"], 100)

    # ------------------------------------------------------------ 영속성

    def test_changes_are_persisted(self):
        """
        add_experience 는 save(update_fields=[...]) 를 호출한다.
        메모리 객체만 확인하면 update_fields 누락을 잡을 수 없다.
        """
        self.profile.add_experience(100)
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.experience, 0)
        self.assertEqual(self.profile.total_experience, 100)


class RequiredExpTest(TestCase):
    def test_required_exp_scales_with_level(self):
        self.assertEqual(Profile.required_exp_for_level(1), 100)
        self.assertEqual(Profile.required_exp_for_level(3), 300)

    def test_required_exp_guards_invalid_level(self):
        # level < 1 은 1 로 보정된다
        self.assertEqual(Profile.required_exp_for_level(0), 100)
        self.assertEqual(Profile.required_exp_for_level(-5), 100)
