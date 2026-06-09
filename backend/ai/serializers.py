from rest_framework import serializers
from .models import EventPlan


class EventPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlan
        fields = ('id', 'user', 'input_json', 'output_json', 'provider', 'created_at')
