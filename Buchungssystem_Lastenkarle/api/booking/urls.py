from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.booking.v1.urls')),
]