from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(blank=True, null=True, max_length=15)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE, related_name="customers")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.mobile_no or 'No Phone'})"

    @property
    def total_orders_count(self):
        return self.orders.count()

    @property
    def total_spent(self):
        return sum(o.total_amount for o in self.orders.all())

    @property
    def total_pending_balance(self):
        return sum(o.balance for o in self.orders.all())

