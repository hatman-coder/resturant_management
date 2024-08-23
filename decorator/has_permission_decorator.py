from functools import wraps
from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.response import Response

from apps.permission.models import UserRole


def get_user_role(user):
    user_role = UserRole.objects.filter(user__id=user.id).first()
    return user_role if user_role else None


def has_permission(perm_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.request.user.is_authenticated:
                user_role = get_user_role(request.request.user)
                if user_role and (
                        user_role.role.permissions.filter(name=perm_name).exists() or user_role.permissions.filter(
                        name=perm_name).exists()):
                    return view_func(request, *args, **kwargs)
            return Response({"message": "You don't have permission to do this action."}, status.HTTP_403_FORBIDDEN)

        return _wrapped_view

    return decorator
