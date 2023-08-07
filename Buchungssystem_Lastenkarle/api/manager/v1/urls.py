from django.urls import path
from . import views


urlpatterns = [
    path('user-flag', views.AllUserFlags.as_view()),
    path('bikes', views.BikesOfStore.as_view()),
    path('bikes/<int:bike_id>', views.SelectedBike.as_view()),
    path('bikes/<int:bike_id>/availability', views.SelectedBikeAvailability.as_view()),
    path('bookings', views.BookingsOfStore.as_view()),
    path('bookings/<int:booking_id>', views.SelectedBookingOfStore.as_view()),
    path('bookings/<int:booking_id>/comment', views.CommentToBooking.as_view())
]