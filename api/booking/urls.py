from django.urls import path
from . import views

urlpatterns = [
    path('/region', ''),
    path('/bikes', ''),
    path('bikes/<int:pk>', '')
]