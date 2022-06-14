from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import AllowAny

from .serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from .data.config import ResponseMessage

# Create your views here.


class TokenObtainPair(APIView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        response = serializer.validated_data

        if not response:
            return Response(ResponseMessage.TOKEN_INVALID, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response, status=status.HTTP_200_OK)


class TokenRefresh(APIView):
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        response = serializer.validated_data

        if not response:
            return Response(ResponseMessage.TOKEN_INVALID, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response, status=status.HTTP_200_OK)


class TokenBlacklist(APIView):
    serializer_class = TokenBlacklistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        response = serializer.validated_data

        return Response(response, status=status.HTTP_200_OK)
