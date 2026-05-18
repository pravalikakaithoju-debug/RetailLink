from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    retailer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    STATUS_CHOICES = (

    ('Pending', 'Pending'),

    ('Processing', 'Processing'),

    ('Shipped', 'Shipped'),

    ('Delivered', 'Delivered'),

    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='Pending'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name