from django.urls import path
from .views import UserDetailView, CustomTokenObtainPairView, RegisterUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserDetailView.as_view(), name='user_detail'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
]
