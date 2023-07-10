from django.urls import path, include
from api.booking import views

urlpatterns = [
    path('booking/', include('api.booking.urls')),
    #path('admin/', include('')),
    #path('manager/', include('')),
    #path('', include('')),  # for user rest api
]
