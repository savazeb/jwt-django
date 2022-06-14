import jwt

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenError

from .models import Account
from .models import OutstandingToken, BlacklistedToken
from .utils import datetime_from_epoch


class Token:
    def __init__(self, token=None):

        # Decode token
        self.token = token
        if self.token is not None:
            try:
                self.payload = jwt.decode(
                    str(self.token), str(settings.SECRET_KEY), str(settings.SIMPLE_JWT["ALGORITHM"])
                )

                self.set_jti()
                self.set_iat()
                self.set_exp()
                self.set_user_id()

            except:
                print("bad token")
        else:
            raise ("token is invalid")

    def set_jti(self, claim="jti"):
        self.jti = self.payload[claim]

    def set_iat(self, claim="iat"):
        self.iat = self.payload[claim]

    def set_exp(self, claim="exp"):
        self.exp = self.payload[claim]

    def set_user_id(self, claim="user_id"):
        self.user_id = self.payload[claim]


class SaveToken(Token):
    token = None

    def __init__(self, token):
        super().__init__(token)
        print(self.jti)

        user = Account.objects.get(id=self.user_id)
        token, _ = OutstandingToken.objects.get_or_create(
            jti=self.jti,
            account=user,
            defaults={
                "token": str(token),
                "created_at": datetime_from_epoch(self.iat),
                "expires_at": datetime_from_epoch(self.exp),
            },
        )


class BlacklistToken(Token):
    def __init__(self, token):
        super().__init__(token)

        token, _ = OutstandingToken.objects.get_or_create(
            jti=self.jti,
            defaults={
                "token": str(self.token),
                "expires_at": datetime_from_epoch(self.exp),
            },
        )

        BlacklistedToken.objects.get_or_create(token=token)


class CheckBlacklist(Token):
    def __init__(self, token):
        super().__init__(token)
        print(self.jti)
        if BlacklistedToken.objects.filter(token__jti=self.jti).exists():
            raise TokenError(_("Token is blacklisted"))
        print("False")
        self.__set_status__(False)

    def __set_status__(self, status):
        self.status = status
