from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from abstract.base_model import BaseModel
from external.enum import UserRole

class SuperUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email, username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    first_name = models.CharField(_('first_name'), max_length=100)
    last_name = models.CharField(_('last_name'), max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(
        max_length=128, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pic/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    role = models.Charfield(choices=UserRole.choices, default=UserRole.USER.value, max_length=52, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    two_factor = models.BooleanField(default=False)
    login_attempt = models.PositiveIntegerField(
        default=0)

    objects = SuperUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
