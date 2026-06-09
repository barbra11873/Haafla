from rest_framework import generics, permissions
from rest_framework.response import Response


class HealthView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'status': 'ok'})
