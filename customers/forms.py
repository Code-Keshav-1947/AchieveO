from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "mobile_no", "email", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. John Doe / School Name", "required": True}),
            "mobile_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 9876543210"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "e.g. customer@example.com"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 123 Main St, City"}),
        }
