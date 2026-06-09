from rest_framework import serializers
from .models import Vendor, PortfolioItem
from .image_utils import validate_uploaded_image, build_thumbnail


class PortfolioItemSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=False, allow_null=True)
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = PortfolioItem
        fields = ('id', 'title', 'media_url', 'file', 'thumbnail', 'description')

    def create(self, validated_data):
        uploaded_file = validated_data.pop('file', None)
        portfolio_item = PortfolioItem.objects.create(**validated_data)
        if uploaded_file:
            portfolio_item.file.save(uploaded_file.name, uploaded_file, save=False)
            thumbnail_file = build_thumbnail(uploaded_file, uploaded_file.name)
            portfolio_item.thumbnail.save(thumbnail_file.name, thumbnail_file, save=False)
        portfolio_item.save()
        return portfolio_item

    def validate_file(self, value):
        if value is None:
            return value
        validate_uploaded_image(value)
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
