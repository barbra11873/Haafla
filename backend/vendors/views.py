from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Vendor, PortfolioItem
from .serializers import VendorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PortfolioItemSerializer
from rest_framework import generics


class PortfolioListView(generics.ListAPIView):
    queryset = PortfolioItem.objects.all().order_by('-id')
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.AllowAny]


class PortfolioUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if getattr(request.user, 'role', None) != 'vendor':
            return Response({'detail': 'Only vendor users may upload portfolio items.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            vendor = request.user.vendor
        except Exception:
            return Response({'detail': 'Vendor profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PortfolioItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=vendor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
