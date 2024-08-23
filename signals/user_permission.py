from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import User
from external.enum import UserRole  # Assuming this is your enum definition
from ..apps.permission.models import Permission, Role, UserRole, Module

@receiver(post_save, sender=User)
def post_save_user_handler(sender, instance, created, **kwargs):
    owner_permissions = ['create_restaurant', 'update_restaurant', 'list_restaurant', 'delete_restaurant']
    user_permissions = ['list_restaurant', 'create_order', 'list_order', 'delete_order']
    
    module, _ = Module.objects.get_or_create(name='Restaurant')

    permission_ids = []
    if instance.role == UserRole.OWNER.value:
        for item in owner_permissions:
            permission, _ = Permission.objects.get_or_create(name=item, module=module)
            permission_ids.append(permission.id)
        
        role, _ = Role.objects.get_or_create(name=instance.role)
        role.permissions.set(permission_ids)
        
        UserRole.objects.get_or_create(user=instance, role=role)
        
    elif instance.role == UserRole.USER.value:
        for item in user_permissions:
            permission, _ = Permission.objects.get_or_create(name=item, module=module)
            permission_ids.append(permission.id)
        
        role, _ = Role.objects.get_or_create(name=instance.role)
        role.permissions.set(permission_ids)
        
        UserRole.objects.get_or_create(user=instance, role=role)
