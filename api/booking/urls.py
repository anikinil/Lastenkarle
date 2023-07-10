from django.urls import path
from . import views

urlpatterns = [
    path('bikes/', views.getAllBikes),
    #path('/region', ''),
    #path('/bikes', ''),
    #path('bikes/', '')
]