from django.urls import path
from knox.views import LogoutView, LogoutAllView
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrateUser.as_view()),
    path('logout', LogoutView.as_view()),
    path('logout-all', LogoutAllView.as_view()),
    path('user/data', views.UserDataOfUser.as_view()),
    path('user/update', views.UpdateUserData.as_view()),
    path('user/bookings/', views.AllBookingsFromUser.as_view()),
    path('user/bookings/<int:booking_id>', views.BookingFromUser.as_view()),
    path('user/bookings/<int:booking_id>/bike', views.BookedBike.as_view()),
    path('user/bookings/<int:booking_id>/bike/store', views.StoreOfBookedBike.as_view()),
    path('user/delete-account', views.DeleteUserAccount.as_view()),
    path('helmholtz/login', views.helmholtzLogin),
    path('helmholtz/auth', views.HelmholtzAuthView.as_view()),
]