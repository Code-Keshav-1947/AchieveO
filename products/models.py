from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=70)
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    stocks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.owner}"
