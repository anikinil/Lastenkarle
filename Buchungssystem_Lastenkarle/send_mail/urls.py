from django.urls import path
from . import views

urlpatterns = [
    path('send-mail/', views.send_test_emails, name='send_mail'),
]
