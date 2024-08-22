from django.urls import path
from . import views


urlpatterns = [
    path('<str:store_name>/equipment', views.RegisteredEquipment.as_view()),
    path('<str:store_name>/enrollment', views.EnrollUser.as_view()),
    path('<str:store_name>/store-page', views.StorePage.as_view()),
    path('<str:store_name>/bikes', views.BikesOfStore.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>', views.SelectedBike.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>/delete', views.DeleteBike.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>/update', views.UpdateSelectedBike.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>/availability', views.SelectedBikeAvailability.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>/equipment/add', views.SelectedBikeAddEquipment.as_view()),
    path('<str:store_name>/bikes/<int:bike_id>/equipment/remove', views.SelectedBikeRemoveEquipment.as_view()),
    path('<str:store_name>/bookings', views.BookingsOfStore.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>', views.SelectedBookingOfStore.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>/comment', views.CommentToBooking.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>/comment/report', views.ReportComment.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>/user-info', views.CheckLocalData.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>/hand-out', views.ConfirmBikeHandOut.as_view()),
    path('<str:store_name>/bookings/<int:booking_id>/return', views.ConfirmBikeReturn.as_view()),
    path('<str:store_name>/bookings/by/<str:qr_string>', views.FindByQRString.as_view())
]