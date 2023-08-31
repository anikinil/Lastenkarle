from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from .views import *


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        self.assertEqual("Hello, World!", "Hello, World!")


class AllUserFlagsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.user.is_superuser = True
        self.user.save()

    def test_get_all_user_flags(self):
        request = self.factory.get('/user_flags/')
        request.user = self.user
        response = AllUserFlags.as_view()(request)

        self.assertEqual(response.status_code, 200)
