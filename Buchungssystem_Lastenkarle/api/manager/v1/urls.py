from django.urls import path
from . import views


urlpatterns = [
    path('user-flag', views.AllUserFlags.as_view()),
    path('enrollment', views.EnrollUser.as_view()),
    path('store-page', views.StorePage.as_view()),
    path('bikes', views.BikesOfStore.as_view()),
    path('bikes/<int:bike_id>', views.SelectedBike.as_view()),
    path('bikes/<int:bike_id>/availability', views.SelectedBikeAvailability.as_view()),
    path('bookings', views.BookingsOfStore.as_view()),
    path('bookings/<int:booking_id>', views.SelectedBookingOfStore.as_view()),
    path('bookings/<int:booking_id>/comment', views.CommentToBooking.as_view()),
    path('bookings/<int:booking_id>/comment/report', views.ReportComment.as_view()),
    path('bikes/<int:bike_id>/internal-booking', views.SelectedBike.as_view()),
    path('bookings/<int:booking_id>/user-info', views.CheckLocalData.as_view()),
    path('bookings/<int:booking_id>/confirmation', views.ConfirmBikeHandOut.as_view()),
    path('bookings/<str:qr_string>', views.FindByQRString.as_view())
]