from django.db import models
from django.conf import settings
from vendors.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='marketplace_services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_cents = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, default='USD')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.vendor.display_name})"
