from django.urls import path
from . import views

app_name = "requests"

urlpatterns = [
    # ... your existing urls
    path("contact-submit/", views.contact_submit, name="contact_submit"),
]
