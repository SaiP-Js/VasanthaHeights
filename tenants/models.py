from django.db import models
from django.conf import settings
from properties.models import Unit
import uuid


class TenantApplication(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    HOME_TYPE_CHOICES = [
        ('APT', 'Apartment'),
        ('HOUSE', 'Independent House'),
        ('OTHER', 'Other'),
    ]

    application_id = models.CharField(
        max_length=20,
        unique=True,
        default=lambda: uuid.uuid4().hex[:20].upper()
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='applications')

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    applicant_type = models.CharField(max_length=50)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    current_address = models.TextField()
    current_home_type = models.CharField(max_length=10, choices=HOME_TYPE_CHOICES)
    reason_for_leaving = models.TextField()
    current_move_in_date = models.DateField()
    current_monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

    area_name = models.CharField(max_length=255)

    aadhaar_number = models.CharField(max_length=20)
    driving_license_number = models.CharField(max_length=30)

    employer_name = models.CharField(max_length=255, blank=True)
    employer_address = models.TextField(blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def masked_aadhaar(self):
        if len(self.aadhaar_number) < 4:
            return '****'
        return 'XXXX-XXXX-' + self.aadhaar_number[-4:]

    def masked_dl(self):
        if len(self.driving_license_number) < 4:
            return '****'
        return 'XXXX-' + self.driving_license_number[-4:]

    def __str__(self):
        return f"{self.application_id} - {self.user}"


class Vehicle(models.Model):
    application = models.ForeignKey(TenantApplication, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20)
    registered_state = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class HouseholdMember(models.Model):
    application = models.ForeignKey(TenantApplication, on_delete=models.CASCADE, related_name='household_members')
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.EmailField(blank=True)
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.relationship}"


def tenant_document_path(instance, filename):
    return f"tenants/{instance.tenant.id}/{filename}"


class TenantDocument(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=tenant_document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.tenant} - {self.file.name}"
