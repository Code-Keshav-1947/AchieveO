from django import forms
from .models import Order
from customers.models import Customer
from products.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "customer", "product", "quantity", "advance", "status", "due_date", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 500 Business Cards / Banner 6x3", "required": True}),
            "customer": forms.Select(attrs={"class": "form-control", "required": True}),
            "product": forms.Select(attrs={"class": "form-control", "required": True}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "1", "min": "1", "required": True}),
            "advance": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0", "min": "0"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Special printing / finishing instructions..."}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("owner", None)
        super().__init__(*args, **kwargs)
        if owner:
            self.fields["customer"].queryset = Customer.objects.filter(owner=owner)
            self.fields["product"].queryset = Product.objects.filter(owner=owner)
