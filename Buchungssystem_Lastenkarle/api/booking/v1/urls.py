from django.urls import path
from . import views

urlpatterns = [
    path('region', views.AllRegions.as_view()),
    path('availabilities', views.AllAvailabilities.as_view()),
    path('bikes/', views.AllBikes.as_view()),
    path('bikes/<int:bike_id>', views.SelectedBike.as_view()),
    path('bikes/<int:bike_id>/store', views.StoreByBike.as_view()),
    path('bikes/<int:bike_id>/booking', views.MakeBooking.as_view()),
    path('bikes/<int:bike_id>/availability', views.AvailabilityOfBike.as_view()),
]