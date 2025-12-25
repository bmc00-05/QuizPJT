from django.db import migrations

def seed_badges(apps, schema_editor):
    Badge = apps.get_model("profiles", "Badge")
    badges = [
        {"code": "WELCOME_HOME", "name": "첫 발걸음", "description": "회원가입 후 홈(프로필) 첫 방문"},
        {"code": "FIRST_CLEAR", "name": "첫 클리어", "description": "처음으로 게임 세션을 완료"},
        {"code": "LEVEL_10", "name": "Lv.10 달성", "description": "레벨 10 달성"},
    ]
    for b in badges:
        Badge.objects.update_or_create(
            code=b["code"],
            defaults={"name": b["name"], "description": b["description"]},
        )

def unseed_badges(apps, schema_editor):
    Badge = apps.get_model("profiles", "Badge")
    Badge.objects.filter(code__in=["WELCOME_HOME", "FIRST_CLEAR", "LEVEL_10"]).delete()

class Migration(migrations.Migration):
    dependencies = [
        # ✅ 핵심: 0002를 공통 조상으로 "강제 연결"
        ("profiles", "0002_remove_profile_greeting_profile_memo"),
    ]

    operations = [
        migrations.RunPython(seed_badges, reverse_code=unseed_badges),
    ]