from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'customer', 'service', 'start_time', 'end_time', 'status', 'total_cents', 'currency', 'created_at')
