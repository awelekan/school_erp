from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('academics.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/hr/', include('hr.urls')),
    # path('api/reports/', include('reports.urls')),
    path('api/transport/', include('transport.urls')),
    path('api/hostel/', include('hostel.urls')),

]
