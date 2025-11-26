from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()  # 토큰 삭제
    return Response({'success': 'Logged out'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = RegisterSerializer(request.user)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request):
    user = request.user
    user.delete()
    return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)