from django.urls import path, include

urlpatterns = [
    path('booking/', include('api.booking.urls')),
    path('user/', include('api.user.urls')),
]
