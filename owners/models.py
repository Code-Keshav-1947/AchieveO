from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    mobile_no = models.CharField(blank=True, null=True, max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return f"{self.name} ({self.email})"

