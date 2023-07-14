from django.urls import path
from . import views

urlpatterns = [
    path('region', views.ListRegion.as_view()),
    path('bikes/', views.ListBikes.as_view()),
    path('bikes/<int:pk>', views.DetailBike.as_view()),
    path('bikes/<int:pk>/availablity', views.DetailAvailability.as_view())
]