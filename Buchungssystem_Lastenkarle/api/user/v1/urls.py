from django.urls import path
from . import views

urlpatterns = [
    path('login', views.UserRegistration.as_view()),
#    path('register', ),
    path('<int:user_id>/user', views.DetailUserData.as_view()),
    path('<int:user_id>/user/bookings/', views.ListBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>', views.DetailBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>/bike', views.DetailBikeByBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>/bike/store', views.DetailStoreByBike.as_view()),
]