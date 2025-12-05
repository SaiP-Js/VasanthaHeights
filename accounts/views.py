from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import RegistrationForm, ResidentAccountForm
from .models import EmailOTP

User = get_user_model()

# ----------------------------------------
# 🔄 Resident Registration with Email OTP
# ----------------------------------------

def register_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Store everything needed for OTP verification in session
            request.session["registration_data"] = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "address": form.cleaned_data["address"],
                "password": form.cleaned_data["password"],
            }

            # Create OTP and send email
            otp_obj = EmailOTP.create_otp(form.cleaned_data["email"])
            send_mail(
                subject="Your Vasantha Heights verification code",
                message=f"Your OTP is {otp_obj.code}. It is valid for 10 minutes.",
                from_email="no-reply@vasanthaheights.com",
                recipient_list=[form.cleaned_data["email"]],
            )

            messages.success(request, "We sent a verification code to your email.")
            return redirect("accounts:verify_otp")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_otp(request):
    reg_data = request.session.get("registration_data")
    if not reg_data:
        messages.error(request, "Your session expired. Please start again.")
        return redirect("accounts:register")

    email = reg_data["email"]

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        try:
            otp_obj = EmailOTP.objects.filter(email=email, code=code).latest("created_at")
        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid code. Please check and try again.")
            return render(request, "accounts/verify_otp.html", {"email": email})

        if not otp_obj.is_valid():
            messages.error(request, "This code has expired or was already used.")
            return render(request, "accounts/verify_otp.html", {"email": email})

        otp_obj.is_used = True
        otp_obj.save()

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=reg_data["first_name"],
            last_name=reg_data["last_name"],
        )
        user.set_password(reg_data["password"])
        user.save()

        # Optional: create a profile here with phone/address

        request.session.pop("registration_data", None)
        login(request, user)
        messages.success(request, "Your account has been created and verified.")
        return redirect("tenants:dashboard")

    return render(request, "accounts/verify_otp.html", {"email": email})

# ----------------------------------------
# 🧾 Resident Portal - Manual Account Form
# ----------------------------------------

def create_account_view(request):
    if request.method == 'POST':
        form = ResidentAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/account_success.html')
    else:
        form = ResidentAccountForm()
    return render(request, 'accounts/create_account.html', {'form': form})
