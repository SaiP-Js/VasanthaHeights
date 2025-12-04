from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import ContactForm


def index(request):
    return HttpResponse("Requests app base.")
def contact_submit(request):
    if request.method != "POST":
        return redirect("home")  # or wherever your main page is

    form = ContactForm(request.POST)
    if form.is_valid():
        inquiry = form.save()

        # Optional email notification to owner/admin
        subject = "New Vasantha Heights contact inquiry"
        body = (
            f"Name: {inquiry.first_name} {inquiry.last_name}\n"
            f"Email: {inquiry.email}\n"
            f"Phone: {inquiry.phone}\n"
            f"Move-in date: {inquiry.move_in_date}\n"
            f"Beds: {inquiry.beds}, Baths: {inquiry.baths}\n"
            f"Min rent: {inquiry.min_rent}, Max rent: {inquiry.max_rent}\n"
            f"Pets: {inquiry.get_pet_question_display()}\n"
            f"How did you hear about us: {inquiry.how_hear}\n\n"
            f"Message:\n{inquiry.message}"
        )
        try:
            send_mail(
                subject,
                body,
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@vasanthaheights.com"),
                [getattr(settings, "CONTACT_NOTIFICATION_EMAIL", "owner@example.com")],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, "Thank you. We’ve received your enquiry.")
        return redirect("home")

    # If invalid, show a generic error and redirect back
    messages.error(request, "There was a problem with your contact form. Please try again.")
    return redirect("home")
