from rest_framework import serializers
from .models import Vendor, PortfolioItem


class PortfolioItemSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = PortfolioItem
        fields = ('id', 'title', 'media_url', 'file', 'description')

    def create(self, validated_data):
        # vendor should be passed by the view
        return super().create(validated_data)

    def validate_file(self, value):
        # server-side validation: only allow certain image types and max size 5MB
        if value is None:
            return value
        allowed = ('image/jpeg', 'image/png', 'image/webp')
        content_type = getattr(value, 'content_type', '')
        if content_type not in allowed:
            raise serializers.ValidationError('Unsupported file type. Allowed: jpg, png, webp.')
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('File too large. Max size is 5MB.')
        return value


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
