from django.db import models
from users.models import Wholesaler


class Product(models.Model):
    wholesaler = models.ForeignKey(
        Wholesaler,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name