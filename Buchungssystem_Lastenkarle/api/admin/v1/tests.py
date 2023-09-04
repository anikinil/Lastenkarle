from django.test import TestCase
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory
from db_model.models import User_Status, User
from api.admin.v1.views import AllUserFlags


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        self.assertEqual("Hello, World!", "Hello, World!")
