from rest_framework import serializers
from .models import Vendor, PortfolioItem


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ('id', 'title', 'media_url', 'description')


class VendorSerializer(serializers.ModelSerializer):
    portfolio = PortfolioItemSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = ('id', 'display_name', 'bio', 'location', 'verified', 'rating', 'portfolio')

    def validate(self, attrs):
        # ensure display_name not empty
        display_name = attrs.get('display_name')
        if not display_name:
            raise serializers.ValidationError({'display_name': 'Business name is required.'})
        return attrs

    def create(self, validated_data):
        # user will be provided via viewset perform_create as serializer.save(user=...)
        return super().create(validated_data)
