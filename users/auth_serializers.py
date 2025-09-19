# backend/users/auth_serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends TokenObtainPairSerializer to include user info in response and
    optionally add custom JWT claims.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add simple claims
        token["username"] = user.username
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # attach user info in response JSON
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": getattr(self.user, "email", ""),
        }
        return data
