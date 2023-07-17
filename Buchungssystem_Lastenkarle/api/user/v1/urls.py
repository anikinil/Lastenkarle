from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/booking/', views.ListBooking.as_view()),
    path('<int:user_id>/booking/<int:booking_id>', views.DetailBooking.as_view())
]