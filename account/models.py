from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=48, unique=True)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
