from rest_framework import serializers

from apps.user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        exclude = [
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'login_attempt',
            'user_permissions',
            'groups'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'login_attempt',
            'user_permissions',
            'groups'
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'get_full_name', 'email', 'username', 'profile_pic']


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'id',
            'password',
            'two_factor',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'login_attempt',
            'user_permissions',
            'groups'
        ]
