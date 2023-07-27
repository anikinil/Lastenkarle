from django.urls import path
from . import views

urlpatterns = [
    path('availabilities', views.ListAvailabilities.as_view()),
    path('region', views.ListRegion.as_view()),
    path('bikes/', views.ListBikes.as_view()),
    path('bikes/<int:bike_id>', views.DetailBike.as_view()),
    path('bikes/<int:bike_id>/store', views.DetailStore.as_view()),
    path('bikes/<int:bike_id>/booking', views.DetailBooking.as_view()),
    path('bikes/<int:bike_id>/availability', views.DetailBikeAvailability.as_view()),
]