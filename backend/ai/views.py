from rest_framework import viewsets, permissions
from .models import EventPlan
from .serializers import EventPlanSerializer


class EventPlanViewSet(viewsets.ModelViewSet):
    queryset = EventPlan.objects.all()
    serializer_class = EventPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
