import requests
from rest_framework import response, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.compat import authenticate
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

# __all__ = (
#     'AuthTokenView',
# )
from members.serializers import UserSerializer, AccessTokenSerializer


class AuthTokenForFacebookAccessTokenView(APIView):
    def post(self, request):
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class AuthTokenView(APIView):
    def post(self, request):
        # URL : /api/members/auth-token/
        # username , password를받아 인증 성공하면
        # 토근은 생성하거나 있으면 존재하는 걸 가져와서
        # response로 돌려줌
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)

        # username = request.data.get('username')
        # password = request.data.get('password')
        # user = authenticate(username=username, password=password)
        # if user is not None:
        #
        # # raise APIException('authenticate failure')
        # raise AuthenticationFailed()
        #


class MyUserDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
