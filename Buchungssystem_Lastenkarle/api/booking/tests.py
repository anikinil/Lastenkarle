import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory

from api.serializer import BikeSerializer
from db_model.models import *
from api.user.v1.views import RegistrateUser
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json
from unittest import skip
from django.core import serializers

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST, BASE_DIR
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data

from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

image_path = os.path.join(BASE_DIR, 'media/test_image/', 'image.jpg')

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

user_data_hilda = {
    'username': 'Hilda',
    'password': 'password',
    'contact_data': 'pse_email@gmx.de',
    'year_of_birth': '1901'
}

login_data_hilda = {
    'username': 'Hilda',
    'password': 'password',
}

store_data_store1 = {
    "region": "KA",
    "address": "Storestr. 1",
    "phone_number": "012345",
    "email": "pse_email@gmx.de",
    "name": "Store1",
    "prep_time": "02:00:00",
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
    "sat_opened": True,
    "sat_open": "08:00:00",
    "sat_close": "20:00:00",
    "sun_opened": True,
    "sun_open": "08:00:00",
    "sun_close": "20:00:00"
}

store_data_store2 = {
    "region": "KA",
    "address": "Str. 12",
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
    'name': ['Bike1'],
    'description': ['Es ist schnell']
}

bike_data_bike2 = {
    'name': ['Bike2'],
    'description': ['Es ist weniger schnell']
}

bike_data_bike3 = {
    'name': ['Bike3'],
    'description': ['Mag ich nicht essen']
}

@skip
def initialize_user_with_token(client, user_data, login_data):
    user = User.objects.create_user(**user_data)
    response = client.post("/api/user/v1/login", login_data)
    response_data = json.loads(response.content.decode('utf-8'))
    token_user = response_data.get('token', None)
    return user, token_user

@skip
def add_verified_flag_to_user(user):
    user.user_status.add(User_Status.objects.get(user_status='Verified'))
    user.save()

@skip
def initialize_store(store_data):
    store = Store.objects.create(**store_data)
    store_flag = User_Status.custom_create_store_flags(store)
    store.store_flag = store_flag
    store.save()
    return store

@skip
def initialize_bike_of_store(store, bike_data):
    with open(image_path, 'rb') as image_file:
        image = SimpleUploadedFile("bike_image.jpg", image_file.read(), content_type="image/jpeg")
    bike = Bike.objects.create(name=bike_data.get('name')[0], description=bike_data.get('description')[0], image=image, store=store)
    Availability.create_availability(store, bike)
    return bike



class Test_all_regions(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )

    def check_region_response_payload_format\
                    (self):
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

    @skip
    def test_region_response_payload_format_various_user_authentication(self):
        self.check_region_response_payload_format()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_region_response_payload_format()


class Test_all_availabilities(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def check_amount_of_availabilities(self):
        response = self.client.get('/api/booking/v1/availabilities')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Availability.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    @skip
    def test_availabilities_amount_various_user_authentication(self):
        self.check_amount_of_availabilities()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_amount_of_availabilities()

    @skip
    def test_availabilities_response_payload_format(self):
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


class Test_all_bikes(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def check_amount_of_bikes(self):
        response = self.client.get('/api/booking/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Bike.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    @skip
    def test_bikes_amount_various_user_authentication(self):
        self.check_amount_of_bikes()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_amount_of_bikes()

    @skip
    def test_bikes_response_payload_format(self):
        response = self.client.get('/api/booking/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("name"), str))
            self.assertTrue(isinstance(item.get("description"), str))
            self.assertTrue(isinstance(item.get("store"), int))
            self.assertTrue(isinstance(item.get("image"), str))

            equipment = item.get("equipment", [])
            self.assertTrue(isinstance(equipment, list))
            for equip in equipment:
                self.assertTrue(isinstance(equip, str))


class Test_all_stores(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.store2 = initialize_store(store_data_store2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def check_store_amount(self):
        response = self.client.get('/api/booking/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Store.objects.count()
        self.assertEqual(len(response_data), expected_object_count)

    @skip
    def test_stores_amount_various_user_authentication(self):
        self.check_store_amount()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_store_amount()

    @skip
    def test_stores_response_payload_format(self):
        response = self.client.get('/api/booking/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("region"), str))
            self.assertTrue(isinstance(item.get("address"), str))
            self.assertTrue(isinstance(item.get("phone_number"), str))
            self.assertTrue(isinstance(item.get("email"), str))
            self.assertTrue(isinstance(item.get("name"), str))
            self.assertTrue(isinstance(item.get("prep_time"), str))
            self.assertTrue(isinstance(item.get("mon_opened"), bool))
            self.assertTrue(isinstance(item.get("mon_open"), str))
            self.assertTrue(isinstance(item.get("mon_close"), str))
            self.assertTrue(isinstance(item.get("tue_opened"), bool))
            self.assertTrue(isinstance(item.get("tue_open"), str))
            self.assertTrue(isinstance(item.get("tue_close"), str))
            self.assertTrue(isinstance(item.get("wed_opened"), bool))
            self.assertTrue(isinstance(item.get("wed_open"), str))
            self.assertTrue(isinstance(item.get("wed_close"), str))
            self.assertTrue(isinstance(item.get("thu_opened"), bool))
            self.assertTrue(isinstance(item.get("thu_open"), str))
            self.assertTrue(isinstance(item.get("thu_close"), str))
            self.assertTrue(isinstance(item.get("fri_opened"), bool))
            self.assertTrue(isinstance(item.get("fri_open"), str))
            self.assertTrue(isinstance(item.get("fri_close"), str))
            self.assertTrue(isinstance(item.get("sat_opened"), bool))
            self.assertTrue(isinstance(item.get("sat_open"), str))
            self.assertTrue(isinstance(item.get("sat_close"), str))
            self.assertTrue(isinstance(item.get("sun_opened"), bool))
            self.assertTrue(isinstance(item.get("sun_open"), str))
            self.assertTrue(isinstance(item.get("sun_close"), str))


class Test_selected_bike(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def check_bike_response_payload_format(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(isinstance(response_data.get("id"), int))
        self.assertTrue(isinstance(response_data.get("name"), str))
        self.assertTrue(isinstance(response_data.get("description"), str))
        self.assertTrue(isinstance(response_data.get("store"), int))
        self.assertTrue(isinstance(response_data.get("image"), str))
        equipment = response_data.get("equipment", [])
        self.assertTrue(isinstance(equipment, list))
        for equip in equipment:
            self.assertTrue(isinstance(equip, str))

    @skip
    def test_bike_response_payload_format_various_user_authentication(self):
        self.check_bike_response_payload_format()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_bike_response_payload_format()

    @skip
    def test_bike_response(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        expected_json = {
            'id': self.bike1.pk,
            'store': self.bike1.store.pk,
            'name': 'Bike1',
            'description': 'Es ist schnell',
            'image': self.bike1.image.url,
            'equipment': [],
        }
        self.assertEqual(response_data, expected_json)

    @skip
    def test_bike_id_in_uri_incorrect(self):
        response = self.client.get('/api/booking/v1/bikes/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/api/booking/v1/bikes/0xF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/api/booking/v1/bikes/ ')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_store_by_bike(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.store2 = initialize_store(store_data_store2)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store2, bike_data_bike2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def check_response_data_format(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}/store')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(isinstance(response_data.get("id"), int))
        self.assertTrue(isinstance(response_data.get("region"), str))
        self.assertTrue(isinstance(response_data.get("address"), str))
        self.assertTrue(isinstance(response_data.get("phone_number"), str))
        self.assertTrue(isinstance(response_data.get("email"), str))
        self.assertTrue(isinstance(response_data.get("name"), str))
        self.assertTrue(isinstance(response_data.get("prep_time"), str))
        self.assertTrue(isinstance(response_data.get("mon_opened"), bool))
        self.assertTrue(isinstance(response_data.get("mon_open"), str))
        self.assertTrue(isinstance(response_data.get("mon_close"), str))
        self.assertTrue(isinstance(response_data.get("tue_opened"), bool))
        self.assertTrue(isinstance(response_data.get("tue_open"), str))
        self.assertTrue(isinstance(response_data.get("tue_close"), str))
        self.assertTrue(isinstance(response_data.get("wed_opened"), bool))
        self.assertTrue(isinstance(response_data.get("wed_open"), str))
        self.assertTrue(isinstance(response_data.get("wed_close"), str))
        self.assertTrue(isinstance(response_data.get("thu_opened"), bool))
        self.assertTrue(isinstance(response_data.get("thu_open"), str))
        self.assertTrue(isinstance(response_data.get("thu_close"), str))
        self.assertTrue(isinstance(response_data.get("fri_opened"), bool))
        self.assertTrue(isinstance(response_data.get("fri_open"), str))
        self.assertTrue(isinstance(response_data.get("fri_close"), str))
        self.assertTrue(isinstance(response_data.get("sat_opened"), bool))
        self.assertTrue(isinstance(response_data.get("sat_open"), str))
        self.assertTrue(isinstance(response_data.get("sat_close"), str))
        self.assertTrue(isinstance(response_data.get("sun_opened"), bool))
        self.assertTrue(isinstance(response_data.get("sun_open"), str))
        self.assertTrue(isinstance(response_data.get("sun_close"), str))

    @skip
    def test_store_of_bike_response_payload_format_various_user_authentication(self):
        self.check_response_data_format()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_response_data_format()

    @skip
    def test_store_of_bike_response(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}/store')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, {**store_data_store1, **{"id":self.store1.pk}})
        self.assertNotEqual(response_data, {**store_data_store2, **{"id":self.store2.pk}})

    @skip
    def test_bike_id_in_uri_incorrect(self):
        response = self.client.get('/api/booking/v1/bikes/-1/store')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/api/booking/v1/bikes/0xF/store')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/api/booking/v1/bikes/ /store')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_bike_availability(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.store1 = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def check_availabilities_of_bike_amount(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Availability.objects.filter(bike=self.bike1).count()
        self.assertEqual(len(response_data), expected_object_count)

    @skip
    def test_availabilities_amount_various_user_authentication(self):
        self.check_availabilities_of_bike_amount()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        self.check_availabilities_of_bike_amount()

    @skip
    def test_availabilities_response_payload_format(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}/availability')
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

    @skip
    def test_availability_of_bike_response(self):
        response = self.client.get(f'/api/booking/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        # Check if {'bike': self.bike1.pk} exists in any dictionary within response_data
        self.assertTrue(any(item.get("bike") == self.bike1.pk for item in response_data))


class Test_make_booking(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store1 = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store1, bike_data_bike2)
        self.store2 = initialize_store(store_data_store2)
        self.bike3 = initialize_bike_of_store(self.store2, bike_data_bike3)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    @skip
    def test_make_booking_various_user_authentication(self):
        booking_data1_bike1 = {
            'begin': '2100-01-04',
            'end': '2100-01-11',
            'equipment': []
        }
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike1.pk}/booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike1.pk}/booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike1.pk}/booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @skip
    def test_make_booking_various_request_payloads(self):
        booking_data_for_past = {
            'begin': '1100-01-03',
            'end': '1100-01-10',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store does not provide bike this early."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike1.pk}/booking', booking_data_for_past,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_for_time_travel = {
            'begin': '2200-01-10',
            'end': '2200-01-03',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Time travel is not permitted."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike1.pk}/booking', booking_data_for_time_travel,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_for_closed_on_begin_day = {
            'begin': '2200-01-11',
            'end': '2200-01-16',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store closed on starting day of booking."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking', booking_data_for_closed_on_begin_day,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_for_closed_on_end_day = {
            'begin': '2200-01-10',
            'end': '2200-01-12',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store closed on ending day of booking."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking', booking_data_for_closed_on_end_day,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_successful = {
            'begin': '2100-01-04',
            'end': '2100-01-11',
            'equipment': []
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking', booking_data_successful,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking_data_customer_booking_duration_restriction = {
            'begin': '2100-01-15',
            'end': '2100-01-25',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Customers are not allowed to make booking of attempted length."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking', booking_data_customer_booking_duration_restriction,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_availability_end_not_found = {
            'begin': '2100-01-01',
            'end': '2100-01-08',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Bike not available in selected time frame."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking', booking_data_availability_end_not_found,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_availability_begin_not_found = {
            'begin': '2100-01-08',
            'end': '2100-01-14',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Bike not available in selected time frame."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/booking/v1/bikes/{self.bike3.pk}/booking',
                                    booking_data_availability_begin_not_found,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
