from django.db import models
from django.conf import settings


class Escrow(models.Model):
    booking_id = models.IntegerField()
    amount_cents = models.IntegerField()
    currency = models.CharField(max_length=10, default='USD')
    stripe_payment_intent = models.CharField(max_length=200, blank=True, null=True)
    stripe_status = models.CharField(max_length=50, blank=True, null=True)
    locked = models.BooleanField(default=False)
    released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Escrow for booking {self.booking_id} - {self.amount_cents} {self.currency}"
