from apps.permission.models import Role
from apps.user import User


def role_validator(role):
    role_obj = Role.objects.filter(name=role).first()
    return True if role_obj else False


def get_user(role):
    if not role_validator(role):
        raise ValueError('Invalid role')
    qs = User.objects.filter(user_role__role__name__contains=role)
    return qs


def get_unauthorized_user():
    qs = User.objects.filter(user_role=None)
    return qs
