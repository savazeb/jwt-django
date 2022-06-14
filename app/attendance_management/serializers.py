from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, Account
from .authentication import authenticate
from .tokens import CheckBlacklist, SaveToken, BlacklistToken


class ProductSerializer(serializers.ModelSerializer):
    division = serializers.ReadOnlyField(source="division.name")
    division_rank = serializers.ReadOnlyField(source="division_rank.name")
    duty = serializers.ReadOnlyField(source="duty.name")
    duty_rank = serializers.ReadOnlyField(source="duty_rank.name")

    class Meta:
        model = Employee
        # fields = '__all__'
        fields = ("id", "first_name", "last_name", "email", "division", "division_rank", "duty", "duty_rank")


class TokenObtainPairSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(max_length=128, write_only=True)
    refresh = serializers.CharField(max_length=260, read_only=True)
    access = serializers.CharField(max_length=260, read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("password", None)

        user = authenticate(Account, id, password)

        if user is None:
            return {}

        token = RefreshToken.for_user(user)

        access_token = token.access_token

        SaveToken(access_token)
        SaveToken(token)

        response = {
            "id": id,
            "first_name": user.employee.first_name,
            "last_name": user.employee.first_name,
            "token": {
                "access": str(access_token),
                "refresh": str(token),
            },
        }
        return response


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=260)

    def validate(self, data):
        refresh_token = data.get("refresh", None)

        try:
            result = CheckBlacklist(refresh_token)
            if not result.status:
                token = RefreshToken(refresh_token)

                BlacklistToken(refresh_token)

                token.set_exp()
                token.set_iat()
                token.set_jti()

                access_token = token.access_token

                SaveToken(access_token)
                SaveToken(token)

                return {
                    "access": str(access_token),
                    "refresh": str(token),
                }

        except:
            return {}


class TokenBlacklistSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=260)
    refresh = serializers.CharField(max_length=260)

    def validate(self, data):
        refresh_token = data.get("refresh", None)
        access_token = data.get("access", None)

        try:
            BlacklistToken(refresh_token)
            print("refresh token ok")
        except:
            print("refresh token failed")
        try:
            BlacklistToken(access_token)
            print("access token ok")
        except:
            print("access token failed")

        return {}
