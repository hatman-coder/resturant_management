from rest_framework.serializers import *


class LoginSerializer(Serializer):
    username = CharField(max_length=15, allow_blank=False, allow_null=False)
    password = CharField(max_length=128, allow_blank=False, allow_null=False)


class LogoutSerializer(Serializer):
    refresh = CharField(max_length=128, allow_blank=False, allow_null=False)
