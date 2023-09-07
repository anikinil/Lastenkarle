from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory
from db_model.models import *
from api.user.v1.views import RegistrateUser
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json
from unittest import skip
from django.core import serializers

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data

from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

user_data_wildegard = {
    'username': 'Wildegard',
    'password': 'password',
    'contact_data': 'wilde.gard@gmx.de',
    'year_of_birth': '1901'
}

login_data_wildegard = {
    'username': 'Wildegard',
    'password': 'password',
}

store_data_store1 = {
    "region": "KA",
    "address": "Storestr. 1",
    "phone_number": "012345",
    "email": "pse_email@gmx.de",
    "name": "Store1",
    "prep_time": "00:00:00",
    "mon_opened": True,
    "mon_open": "08:00:00",
    "mon_close": "20:00:00",
    "tue_opened": True,
    "tue_open": "08:00:00",
    "tue_close": "20:00:00",
    "wed_opened": True,
    "wed_open": "08:00:00",
    "wed_close": "20:00:00",
    "thu_opened": True,
    "thu_open": "08:00:00",
    "thu_close": "20:00:00",
    "fri_opened": True,
    "fri_open": "08:00:00",
    "fri_close": "20:00:00",
    "sat_opened": False,
    "sat_open": "08:00:00",
    "sat_close": "20:00:00",
    "sun_opened": False,
    "sun_open": "08:00:00",
    "sun_close": "20:00:00"
}

store_data_store2 = {
    "region": "KA",
    "address": "Storestr. 1123",
    "phone_number": "012345",
    "email": "pse_email@gmx.de",
    "name": "Store2",
    "prep_time": "00:00:00",
    "mon_opened": True,
    "mon_open": "08:00:00",
    "mon_close": "20:00:00",
    "tue_opened": True,
    "tue_open": "08:00:00",
    "tue_close": "20:00:00",
    "wed_opened": True,
    "wed_open": "08:00:00",
    "wed_close": "20:00:00",
    "thu_opened": True,
    "thu_open": "08:00:00",
    "thu_close": "20:00:00",
    "fri_opened": True,
    "fri_open": "08:00:00",
    "fri_close": "20:00:00",
    "sat_opened": False,
    "sat_open": "08:00:00",
    "sat_close": "20:00:00",
    "sun_opened": False,
    "sun_open": "08:00:00",
    "sun_close": "20:00:00"
}

bike_data_bike1 = {
    'name': 'Bike1',
    'description': 'Es ist schnell'
}

bike_data_bike2 = {
    'name': 'Bike2',
    'description': 'Es ist weniger schnell'
}


def initialize_user_with_token(client, user_data, login_data):
    user = User.objects.create_user(**user_data)
    response = client.post("/api/user/v1/login", login_data)
    response_data = json.loads(response.content.decode('utf-8'))
    token_user = response_data.get('token', None)
    return user, token_user


def intialize_store(store_data):
    store = Store.objects.create(**store_data)
    store_flag = User_Status.custom_create_store_flags(store)
    store.store_flag = store_flag
    store.save()
    return store


def initialize_bike_of_store(store, bike_data):
    bike = Bike.create_bike(store, **bike_data)
    return bike


class test_all_regions(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.region_url = '/region'

    def test_region_content_not_logged_in(self):
        response = self.client.get('/api/booking/v1/region')
        expected_json = [
            ["KA", "Karlsruhe"],
            ["ETT", "Ettlingen"],
            ["BAD", "Baden-Baden"],
            ["BRU", "Bruchsal"],
            ["MAL", "Malsch"]
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)

    def test_region_content_logged_in(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/booking/v1/region')
        expected_json = [
            ["KA", "Karlsruhe"],
            ["ETT", "Ettlingen"],
            ["BAD", "Baden-Baden"],
            ["BRU", "Bruchsal"],
            ["MAL", "Malsch"]
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)


class test_all_availabilities(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = intialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)
        self.region_url = '/availabilities'

    def test_availabilities_amount_not_logged_in(self):
        response = self.client.get('/api/booking/v1/availabilities')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)

    def test_availabilities_amount_logged_in(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/booking/v1/availabilities')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)

    def test_availabilities_content(self):
        response = self.client.get('/api/booking/v1/availabilities')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("from_date"), str))
            self.assertTrue(isinstance(item.get("until_date"), str))
            self.assertTrue(isinstance(item.get("store"), int))
            self.assertTrue(isinstance(item.get("bike"), int))
            availability_status = item.get("availability_status", [])
            for status in availability_status:
                self.assertTrue(isinstance(status.get("availability_status"), str))


class test_all_bikes(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = intialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)
        self.region_url = '/bikes'

    def test_bikes_amount_not_logged_in(self):
        response = self.client.get('/api/booking/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)

    def test_bikes_amount_logged_in(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/booking/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)


class test_all_stores(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = intialize_store(store_data_store1)
        self.store2 = intialize_store(store_data_store2)
        self.region_url = '/stores'

    def test_stores_amount_not_logged_in(self):
        response = self.client.get('/api/booking/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)

    def test_stores_amount_logged_in(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/booking/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = 2
        self.assertEqual(len(response_data), expected_object_count)