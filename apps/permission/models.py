from abstract.base_model import BaseModel
from django.db import models

from apps.user.models import User


class Module(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Permission(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} --{self.module}'


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} --{self.role}'
