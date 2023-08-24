from django.urls import path, include

urlpatterns = [
    path('booking/', include('api.booking.urls')),
    path('user/', include('api.user.urls')),
    path('manager/', include('api.manager.urls')),
    path('admin/', include('api.admin.urls')),
]
