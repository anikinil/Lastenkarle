from django.urls import path
from knox.views import LoginView, LogoutAllView
from . import views

urlpatterns = [
    path('status', views.UserStatusView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', views.RegistrateUser.as_view()),
    path('update/data/<int:pk>', views.UpdateUserData.as_view()),
    path('update/local/<int:pk>', views.UpdateLocalData.as_view()),
    path('update/login/<int:pk>', views.UpdateLoginData.as_view()),
    path('logout', LoginView.as_view()),
    path('logout-all', LogoutAllView.as_view()),
    path('<int:user_id>/user', views.DetailUserData.as_view()),
    path('<int:user_id>/user/bookings/', views.ListBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>', views.DetailBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>/bike', views.DetailBikeByBooking.as_view()),
    path('<int:user_id>/user/bookings/<int:booking_id>/bike/store', views.DetailStoreByBike.as_view()),
]