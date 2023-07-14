from django.urls import path, include

urlpatterns = [
    path('booking/', include('api.v1.booking.urls')),
]