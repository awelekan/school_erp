from django.urls import path
from .views import DashboardAPIView

urlpatterns = [
    path('admin-dashboard/', DashboardAPIView.as_view({'get': 'list'}), name="admin-dashboard"),
]
