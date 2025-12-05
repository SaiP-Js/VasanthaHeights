from django import forms
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    # EXTRA FIELDS that are NOT part of User model
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone number"})
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Current address", "rows": 2})
    )

    # PASSWORD FIELDS
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Create password"})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"})
    )

    class Meta:
        model = User
        # Only fields that actually exist on User model
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
        }

    # EMAIL VALIDATION
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    # PASSWORD MATCH VALIDATION
    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")

        if pwd and cpwd and pwd != cpwd:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned
# accounts/forms.py

from django import forms
from .models import ResidentAccount

class ResidentAccountForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, label="I accept the Terms & Conditions")
    promotional_opt_in = forms.BooleanField(required=False, label="Send me promotional emails")

    class Meta:
        model = ResidentAccount
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'address_line3',
            'city', 'state', 'zip_code', 'country',
            'terms_accepted', 'promotional_opt_in'
        ]


class VHLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'class': 'vh-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'vh-input',
            'id': 'password'
        })
    )
