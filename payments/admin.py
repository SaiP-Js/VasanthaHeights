from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'amount', 'mode', 'paid_at')
    list_filter = ('mode', 'paid_at')
