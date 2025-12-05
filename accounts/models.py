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

# accounts/models.py (or residents/models.py)

from django.db import models

class ResidentAccount(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    address_line3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    terms_accepted = models.BooleanField(default=False)
    promotional_opt_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
