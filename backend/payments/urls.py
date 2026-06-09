from rest_framework.routers import DefaultRouter
from .views import EscrowViewSet

router = DefaultRouter()
router.register(r'escrow', EscrowViewSet, basename='escrow')

urlpatterns = router.urls
