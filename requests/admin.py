from django.contrib import admin
from .models import TenantRequest

@admin.register(TenantRequest)
class TenantRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'tenant', 'unit', 'status', 'created_at')
    list_filter = ('status', 'created_at')
from django.contrib import admin
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "move_in_date", "created_at")
    list_filter = ("move_in_date", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
