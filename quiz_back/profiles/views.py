from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import UserProfileSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    로그인한 유저의 현재 프로필 정보를 반환
    (user store fetchUser 용)
    """
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={"username": request.user.username},
    )

    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)