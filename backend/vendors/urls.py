from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'vendors', views.VendorViewSet, basename='vendor')

urlpatterns = router.urls + [
    path('portfolio/', views.PortfolioUploadView.as_view(), name='portfolio-upload'),
    path('portfolio-items/', views.PortfolioListView.as_view(), name='portfolio-list'),
]
