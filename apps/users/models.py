from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.urls import reverse
from apps.common.model import BaseModel
from .managers import CustomUserManeger


class CustomUser(BaseModel, AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)

    objects = CustomUserManeger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
    
    def get_full_name(self) -> str:
        return super().get_full_name()

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"id": self.id})
    