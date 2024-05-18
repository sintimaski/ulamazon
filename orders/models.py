from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    items = models.ManyToManyField(Product, through="OrderItem")

    address = models.TextField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} for {self.address}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (("order", "product"),)
