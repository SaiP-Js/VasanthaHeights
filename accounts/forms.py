from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Create password"
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Re-enter password"
        })
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email", "address"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "address": forms.Textarea(attrs={"placeholder": "Current address", "rows": 2}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")

        if pwd and cpwd and pwd != cpwd:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned
