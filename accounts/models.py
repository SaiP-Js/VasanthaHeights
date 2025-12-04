from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
import random


class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    @classmethod
    def create_otp(cls, email: str):
        code = f"{random.randint(100000, 999999)}"
        return cls.objects.create(email=email, code=code)

    def is_valid(self):
        return (
            not self.is_used and
            timezone.now() - self.created_at < datetime.timedelta(minutes=10)
        )

    def __str__(self):
        return f"{self.email} - {self.code}"
