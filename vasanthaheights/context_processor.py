from django.conf import settings


def site_contact(request):
    return {
        "CONTACT_PHONE": getattr(settings, "CONTACT_PHONE", ""),
        "CONTACT_EMAIL": getattr(settings, "CONTACT_EMAIL", ""),
        "LEASING_NAME": getattr(settings, "LEASING_NAME", ""),
        "LEASING_ADDRESS": getattr(settings, "LEASING_ADDRESS", ""),
        "LEASING_PHONE": getattr(settings, "LEASING_PHONE", ""),
        "LEASING_EMAIL": getattr(settings, "LEASING_EMAIL", ""),
    }
