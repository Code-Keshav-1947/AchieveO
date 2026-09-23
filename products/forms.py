from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "cost_price", "stocks"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. ID Card, Letterhead, Banner", "required": True}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Selling price per unit (₹)", "required": True, "min": "0"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Cost price per unit (₹)", "min": "0"}),
            "stocks": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Current stock count (optional)"}),
        }
