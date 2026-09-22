from django.db import models


# Create your models here.
class Order(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("designing", "Designing"),
        ("printing", "Printing"),
        ("ready", "Ready"),
        ("delivered", "Delivered"),
    ]
    name = models.CharField(max_length=50)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    advance = models.PositiveIntegerField()
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    date_get = models.DateField(auto_now_add=True)
