from rest_framework import viewsets, permissions
from .models import Escrow
from .serializers import EscrowSerializer


class EscrowViewSet(viewsets.ModelViewSet):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer
    permission_classes = [permissions.IsAuthenticated]
