from rest_framework import serializers
from .models import Escrow


class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = ('id', 'booking_id', 'amount_cents', 'currency', 'stripe_payment_intent', 'stripe_status', 'locked', 'released', 'created_at')
