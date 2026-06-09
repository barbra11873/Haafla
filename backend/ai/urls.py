from rest_framework.routers import DefaultRouter
from .views import EventPlanViewSet

router = DefaultRouter()
router.register(r'plans', EventPlanViewSet, basename='eventplan')

urlpatterns = router.urls
