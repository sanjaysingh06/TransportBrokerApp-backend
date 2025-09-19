# backend/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    CurrentUserView,
    LogoutView,
    CookieLoginView,
)

urlpatterns = [
    # Obtain tokens (login)
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Refresh access using refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Current user
    path("me/", CurrentUserView.as_view(), name="current_user"),
    # Logout (blacklist refresh)
    path("logout/", LogoutView.as_view(), name="token_logout"),
    # Optional cookie-based login
    path("cookie-login/", CookieLoginView.as_view(), name="cookie_login"),
]
