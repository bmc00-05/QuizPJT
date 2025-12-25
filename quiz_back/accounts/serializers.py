from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=50, write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("email", "password", "username", "nickname")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data.pop("username")
        nickname = validated_data.pop("nickname", "")

        # ✅ User 모델에 username 필드가 있으면 같이 생성(기본 User 호환)
        create_kwargs = dict(validated_data)
        user_field_names = {f.name for f in User._meta.get_fields()}
        if "username" in user_field_names:
            create_kwargs["username"] = username

        user = User.objects.create_user(**create_kwargs)

        # ✅ Profile 생성 (Profile에 nickname 필드가 있는 경우만 저장)
        profile_kwargs = {"user": user, "username": username}
        profile_field_names = {f.name for f in Profile._meta.get_fields()}
        if "nickname" in profile_field_names:
            profile_kwargs["nickname"] = nickname

        Profile.objects.create(**profile_kwargs)

        return user