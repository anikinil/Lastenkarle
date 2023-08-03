from django.urls import path
from knox.views import LoginView, LogoutView, LogoutAllView
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrateUser.as_view()),
    path('update/data', views.UpdateUserData.as_view()),
    path('update/local', views.UpdateLocalData.as_view()),
    path('update/login', views.UpdateLoginData.as_view()),
    path('logout', LogoutView.as_view()),
    path('logout-all', LogoutAllView.as_view()),
    path('user/data', views.UserDataOfUser.as_view()),
    path('user/local', views.LocalDataOfUser.as_view()),
    path('user/credentials', views.LoginDataOfUser.as_view()),
    path('user/bookings/', views.AllBookingsFromUser.as_view()),
    path('user/bookings/<int:booking_id>', views.BookingFromUser.as_view()),
    path('user/bookings/<int:booking_id>/bike', views.BookedBike.as_view()),
    path('user/bookings/<int:booking_id>/bike/store', views.StoreOfBookedBike.as_view()),
]