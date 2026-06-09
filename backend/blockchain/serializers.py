from rest_framework import serializers
from .models import OnChainTx


class OnChainTxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnChainTx
        fields = ('id', 'related_type', 'related_id', 'tx_hash', 'network', 'status', 'created_at')
