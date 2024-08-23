from rest_framework.serializers import *


class PasswordChangeSerializer(Serializer):
    old_password = CharField(max_length=128, allow_blank=False, allow_null=False)
    new_password = CharField(max_length=128, allow_blank=False, allow_null=False)
    confirm_password = CharField(max_length=128, allow_blank=False, allow_null=False)


class PasswordResetSerializer(Serializer):
    email = EmailField(allow_blank=False, allow_null=False)
