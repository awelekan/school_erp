from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'hostels', HostelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'student-room-allocations', StudentRoomAllocationViewSet)
router.register(r'hostel-payments', HostelFeePaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
