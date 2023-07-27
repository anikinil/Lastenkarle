from django.urls import path
from . import views


urlpatterns = [
    path('<int:store_id>/bikes', views.ListBikes.as_view()),
    path('<int:store_id>/bikes/<int:bike_id>', views.DetailBike.as_view()),
]