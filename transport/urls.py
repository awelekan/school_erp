from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransportFeeViewSet

router = DefaultRouter()
router.register(r'transport-fees', TransportFeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
