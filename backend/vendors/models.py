from django.db import models
from django.conf import settings


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.display_name


class PortfolioItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    media_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vendor.display_name} - {self.title}"
