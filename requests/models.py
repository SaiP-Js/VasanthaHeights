from django.db import models
from django.conf import settings
from properties.models import Unit



class TenantRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.tenant}"
from django.db import models


class ContactInquiry(models.Model):
    PET_CHOICES = [
        ("have_pets", "I have pets"),
    ("no_pets", "No pets"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    move_in_date = models.DateField()
    beds = models.CharField(max_length=20, blank=True)
    baths = models.CharField(max_length=20, blank=True)
    min_rent = models.IntegerField(null=True, blank=True)
    max_rent = models.IntegerField(null=True, blank=True)
    pet_question = models.CharField(max_length=20, choices=PET_CHOICES)
    how_hear = models.CharField(max_length=100)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
