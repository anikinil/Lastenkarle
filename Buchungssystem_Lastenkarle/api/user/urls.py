from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.user.v1.urls')),
]
