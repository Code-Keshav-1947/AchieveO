from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=70)
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE, related_name="products")
    price = models.PositiveIntegerField(help_text="Selling price per unit in ₹")
    cost_price = models.PositiveIntegerField(default=0, help_text="Cost/production price per unit in ₹")
    stocks = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    @property
    def unit_profit(self):
        return max(0, self.price - (self.cost_price or 0))

