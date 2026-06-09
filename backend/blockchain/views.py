from rest_framework import viewsets, permissions
from .models import OnChainTx
from .serializers import OnChainTxSerializer


class OnChainTxViewSet(viewsets.ModelViewSet):
    queryset = OnChainTx.objects.all()
    serializer_class = OnChainTxSerializer
    permission_classes = [permissions.IsAuthenticated]
