from django.contrib import admin
from .models import TenantApplication, Vehicle, HouseholdMember, TenantDocument

@admin.display(description="Aadhaar")
def aadhaar_masked(obj):
    return obj.masked_aadhaar()

class TenantApplicationAdmin(admin.ModelAdmin):
    list_display = ("application_id", "user", "unit", "status", aadhaar_masked, "created_at")
    search_fields = ("application_id", "user__email", "unit__unit_number")

admin.site.register(TenantApplication, TenantApplicationAdmin)
admin.site.register(Vehicle)
admin.site.register(HouseholdMember)
admin.site.register(TenantDocument)
