import datetime

from django.contrib.auth import logout
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers.serializers_v1 import LoginSerializer, LogoutSerializer
from external.time_checker import time_checker
from apps.user.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = str(user.id)
        token['name'] = str(user.get_full_name())
        token['username'] = str(user.username)

        # Add custom claims
        data = dict()
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)

        return data


class LoginViewSet(ModelViewSet):
    model_class = User
    permission_classes = []

    def get_serializer_class(self):
        return LoginSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            return Response({'message': 'Username and password is required'}, status=HTTP_406_NOT_ACCEPTABLE)

        instance = self.model_class.objects.filter(username=username).first()

        if not instance:
            return Response({'message': 'Invalid username or password'}, status=HTTP_400_BAD_REQUEST)

        if not instance.is_active:
            return Response({'message': 'Your account is currently inactive. Please contact IT support for '
                                        'assistance.'}, status=HTTP_403_FORBIDDEN)

        if instance.login_attempt >= 10:

            if time_checker(instance.updated_at, hour=24):
                instance.login_attempt = 0
                instance.save()
                pass
            else:
                return Response({'message': 'You have exceeded the maximum number of unsuccessful attempts. '
                                            'Please try again after 24 hours.'},
                                status=HTTP_403_FORBIDDEN)

        serializer_class = LoginSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            if instance.check_password(serializer.validated_data['password']):
                instance.login_attempt = 0
                instance.save()
                token = CustomTokenObtainPairSerializer.get_token(instance)
                token['message'] = 'Login successful'
                return Response(token, status=HTTP_202_ACCEPTED)
            else:
                instance.login_attempt += 1
                instance.save()
                return Response({'message': 'Invalid username or password'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LogoutViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        if 'refresh' not in request.data:
            return Response({'message': 'Token is required'}, HTTP_406_NOT_ACCEPTABLE)
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({"message": "Logout successful"}, status=HTTP_202_ACCEPTED)
        except (TokenError, TokenBackendError):
            return Response({"message": "Token is already blacklisted"}, status=HTTP_406_NOT_ACCEPTABLE)


class LogoutFromEveryWhereViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        now = timezone.now()

        outstanding_token_qs = OutstandingToken.objects.filter(
            user=request.user,
            expires_at__gt=now
        )

        for token in outstanding_token_qs:
            # Create BlacklistedToken or get existing one
            get, create = BlacklistedToken.objects.get_or_create(token=token)

        logout(request)
        return Response({'message': 'Your active sessions have been removed'}, status=HTTP_202_ACCEPTED)

