from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    mobile_no = models.CharField(blank=True, null=True, max_length=10)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=70, null=True, blank=True)
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.owner}"
