from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .serializers import UserSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=7*24*60*60,
        )
        response.data['access'] = str(refresh.access_token)
        return response

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signin_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=7*24*60*60,
        )
        response.data = {
            'access': str(refresh.access_token),
            'username': user.username,
        }
        return response
    return Response({"error": "Invalid Credentials"}, status=401)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def signout_view(request):
    response = Response()
    response.delete_cookie('refresh_token')
    response.data = {"message": "Logged out successfully"}
    return response

class CookieTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({"error": "Authentication credentials were not provided."}, status=401)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)
        return Response({"access": access_token})
