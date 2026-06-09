from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import VendorViewSet, PortfolioUploadView

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')

urlpatterns = router.urls + [
	path('portfolio/', PortfolioUploadView.as_view(), name='portfolio-upload'),
]
