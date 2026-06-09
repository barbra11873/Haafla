from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Vendor
from .serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'vendor':
            raise PermissionDenied('Only vendors can create profiles')
        # prevent multiple vendor profiles per user
        if Vendor.objects.filter(user=self.request.user).exists():
            raise PermissionDenied('Vendor profile already exists for this user')
        serializer.save(user=self.request.user)
