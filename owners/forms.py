from django import forms
from .models import Owner

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["name", "email", "mobile_no"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Name / Owner Name", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "business@example.com", "required": True}),
            "mobile_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mobile Number"}),
        }
