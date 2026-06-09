from rest_framework import serializers
from .models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'vendor', 'category', 'title', 'description', 'price_cents', 'currency', 'is_active')
