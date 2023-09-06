from django.test import TestCase
from rest_framework.test import APIRequestFactory
from db_model.models import User
from api.admin.v1.views import AddStore
from django.contrib.auth import login
from rest_framework import status
from django.test import Client
import json


class AdminCreateStore(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()
        self.store_data = {
            "region": "KA",
            "phone_number": "0176 000000000",
            "email": "ich_bin_fag@gmx.de",
            "address": "Test",
            "name": "Store1"
        }
        self.bike_data = {

        }
        self.Admin = User.objects.create_superuser(username="Caro", password="password",
                                                   contact_data="wilde.gard@gmx.de")
        response = self.client.post("/api/user/v1/login", {"username": self.Admin.username, "password": "password"})
        # Parse the response content to get the token
        response_data = json.loads(response.content.decode('utf-8'))
        self.Admin.token = response_data.get('token', None)