from django.db import models
from django.contrib.auth.models import User


class Wholesaler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.company_name


class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    wholesaler = models.ForeignKey(
        Wholesaler,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.shop_name