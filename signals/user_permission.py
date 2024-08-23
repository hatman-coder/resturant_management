from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import User
from external.enum import RoleEnum
from external.permission_attributes import (
    owner_permissions,
    user_permissions,
    employee_permissions,
)
from apps.permission.models import Permission, Role, UserRole, Module


@receiver(post_save, sender=User)
def post_save_user_handler(sender, instance, created, **kwargs):
    permission_ids = []

    # Handle Owner Permissions
    if instance.role == RoleEnum.OWNER.value:
        permission_data = owner_permissions.items()
    elif instance.role == RoleEnum.USER.value:
        permission_data = user_permissions.items()
    elif instance.role == RoleEnum.EMPLOYEE.value:
        permission_data = employee_permissions.items()

    for module_name, permissions in permission_data:
        module, _ = Module.objects.get_or_create(name=module_name.capitalize())
        for permission_name in permissions:
            permission, _ = Permission.objects.get_or_create(
                name=permission_name, module=module
            )
            permission_ids.append(permission.id)

    # Assign Permissions to Role and Create UserRole
    role, _ = Role.objects.get_or_create(name=instance.role)
    role.permissions.set(permission_ids)
    UserRole.objects.get_or_create(user=instance, role=role)
