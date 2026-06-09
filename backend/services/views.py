from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure only vendor users can create services
        if not hasattr(self.request.user, 'vendor') and self.request.user.role != 'vendor':
            raise PermissionError('Only vendors can create services')
        vendor = getattr(self.request.user, 'vendor', None)
        serializer.save(vendor=vendor)
