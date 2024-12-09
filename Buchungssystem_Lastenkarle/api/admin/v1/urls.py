from django.urls import path
from . import views

urlpatterns = [
    path('equipment', views.RegisteredEquipment.as_view()),
    path('user-flags', views.AllUserFlags.as_view()),
    path('ban-user', views.BanUser.as_view()),
    path('create/store', views.AddStore.as_view()),
    path('create/store/<str:store_name>/bike', views.AddBike.as_view()),
    path('delete/bike/<int:bike_id>', views.DeleteBike.as_view()),
    path('delete/store/<str:store_name>', views.DeleteStore.as_view()),
    path('users', views.AllUsers.as_view()),
    path('users/<int:user_id>', views.SelectedUser.as_view()),
    path('users/<int:user_id>/bookings', views.AllBookingsOfUser.as_view()),
    path('bookings', views.AllBookings.as_view()),
    path('bookings/<int:booking_id>', views.SelectedBooking.as_view()),
    path('bikes', views.AllBikes.as_view()),
    path('bikes/<int:bike_id>', views.SelectedBike.as_view()),
    path('bikes/<int:bike_id>/update', views.UpdateSelectedBike.as_view()),
    path('bikes/<int:bike_id>/equipment', views.EquipmentOfBike.as_view()),#
    path('bikes/<int:bike_id>/availability', views.AvailabilityOfBike.as_view()),
    path('stores', views.AllStores.as_view()),
    path('stores/<str:store_name>', views.SelectedStore.as_view()),
    path('stores/<str:store_name>/update', views.UpdateSelectedStore.as_view()),
    path('stores/<str:store_name>/availability', views.AvailabilityOfBikesFromStore.as_view())
]