from django import forms
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = [
            "first_name", "last_name", "zip_code", "email", "phone",
            "move_in_date", "beds", "baths", "min_rent", "max_rent",
            "pet_question", "how_hear", "message",
        ]
        widgets = {
            "move_in_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        min_rent = cleaned.get("min_rent")
        max_rent = cleaned.get("max_rent")

        if min_rent and max_rent and min_rent > max_rent:
            self.add_error("max_rent", "Max rent should be greater than or equal to min rent.")
        return cleaned
