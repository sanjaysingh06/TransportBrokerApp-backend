# backend/users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .auth_serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/token/  -> returns { refresh, access, user }
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    """
    POST /api/auth/logout/  with {"refresh": "<token>"} blacklists refresh token.
    Requires 'rest_framework_simplejwt.token_blacklist' in INSTALLED_APPS.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token or blacklist not enabled."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class CookieLoginView(APIView):
    """
    Optional: returns access in JSON and sets refresh token in HttpOnly cookie.
    Use this if you want to keep refresh token out of JS storage.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        resp = Response({
            "access": access,
            "user": UserSerializer(user).data
        })
        # In production set secure=True and adjust samesite as required.
        resp.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 3600
        )
        return resp
