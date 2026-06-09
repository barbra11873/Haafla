from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'vendor', 'title', 'description', 'price', 'currency', 'created_at')
