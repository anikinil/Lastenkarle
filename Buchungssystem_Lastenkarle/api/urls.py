from django.urls import path, include

urlpatterns = [
    path('booking/', include('api.booking.v1.urls')),
    path('user/', include('api.user.v1.urls')),
    path('manager/', include('api.manager.v1.urls')),
    path('admin/', include('api.admin.v1.urls')),
]
