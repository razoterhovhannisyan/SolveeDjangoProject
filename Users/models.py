from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    user_type_choices = [
        ('Team', 'Team'),
        ('Solo', 'Solo'),
    ]
    user_type = models.CharField(max_length=4, choices=user_type_choices)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class TeamUser(CustomUser):
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Team User'
        verbose_name_plural = 'Team Users'

    def __str__(self):
        return f"{self.username}"


class SoloUser(CustomUser):
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Solo User'
        verbose_name_plural = 'Solo Users'

    def __str__(self):
        return f"{self.username}"
