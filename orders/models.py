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
    name = models.CharField(max_length=100, help_text="Job title or order description")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    advance = models.PositiveIntegerField(default=0, help_text="Advance payment received in ₹")
    owner = models.ForeignKey("owners.Owner", on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    notes = models.TextField(blank=True, null=True, help_text="Custom print notes / instructions")
    due_date = models.DateField(blank=True, null=True, help_text="Target completion or delivery date")
    date_get = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Order #{self.id} - {self.name} ({self.customer.name})"

    @property
    def total_amount(self):
        if self.product and self.quantity:
            return self.product.price * self.quantity
        return 0

    @property
    def balance(self):
        return max(0, self.total_amount - (self.advance or 0))

    @property
    def payment_status(self):
        total = self.total_amount
        adv = self.advance or 0
        if total == 0 or adv >= total:
            return "paid"
        elif adv > 0:
            return "partial"
        return "due"

    @property
    def estimated_profit(self):
        if self.product and self.quantity:
            return self.product.unit_profit * self.quantity
        return 0

    @property
    def is_active(self):
        return str(self.status).lower() != "delivered"

