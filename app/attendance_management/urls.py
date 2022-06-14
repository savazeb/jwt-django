from django.urls import path
from .views import *

urlpatterns = [
    # uri for authentications
    path("v0/authentications", TokenObtainPair.as_view(), name="TokenObtainPair"),
    path("v0/authentications/refresh", TokenRefresh.as_view(), name="TokenRefresh"),
    path("v0/authentications/blacklist", TokenBlacklist.as_view(), name="TokenBlacklist"),
]
