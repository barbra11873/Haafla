from rest_framework.routers import DefaultRouter
from .views import OnChainTxViewSet

router = DefaultRouter()
router.register(r'tx', OnChainTxViewSet, basename='onchain')

urlpatterns = router.urls
