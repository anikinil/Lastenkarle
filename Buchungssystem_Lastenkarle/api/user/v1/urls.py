from django.urls import path
from knox.views import LoginView, LogoutAllView
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrateUser.as_view()),
    path('update/data', views.UpdateUserData.as_view()),
    path('update/local/<int:pk>', views.UpdateLocalData.as_view()),
    path('update/login/<int:pk>', views.UpdateLoginData.as_view()),
    path('logout', LoginView.as_view()),
    path('logout-all', LogoutAllView.as_view()),
    path('/user', views.LocalDataOfUser.as_view()),
    path('/user/bookings/', views.AllBookingsFromUser.as_view()),
    path('/user/bookings/<int:booking_id>', views.BookingFromUser.as_view()),
    path('/user/bookings/<int:booking_id>/bike', views.BookedBike.as_view()),
    path('/user/bookings/<int:booking_id>/bike/store', views.StoreOfBookedBike.as_view()),
]