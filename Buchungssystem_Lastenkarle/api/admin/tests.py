import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory

from api.algorithm import split_availabilities_algorithm
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
image_path_update = os.path.join(BASE_DIR, 'media/test_image/', 'update_image.jpg')

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

user_data_store_manager = {
    'username': 'Harry',
    'password': 'password',
    'contact_data': 'bitte_toete_mich@gmx.de',
    'year_of_birth': '1992'
}

login_data_store_manager = {
    'username': 'Harry',
    'password': 'password'
}

user_data_caro = {
    'username': 'Caro',
    'password': 'password',
    'contact_data': 'koeri_werk@gmx.de',
    'year_of_birth': '1901'
}

login_data_caro = {
    'username': 'Caro',
    'password': 'password'
}

update_store_data = {
        "address": "Brunnenstr. 31",
        "phone_number": "49159",
        "email": "koeri_werk@gmx.de",
        "prep_time": "06:00:00",
        "mon_opened": True,
        "mon_open": "12:00:00",
        "mon_close": "18:00:00",
        "tue_opened": True,
        "tue_open": "12:00:00",
        "tue_close": "18:00:00",
        "wed_opened": True,
        "wed_open": "12:00:00",
        "wed_close": "18:00:00",
        "thu_opened": True,
        "thu_open": "12:00:00",
        "thu_close": "18:00:00",
        "fri_opened": True,
        "fri_open": "18:00:00",
        "fri_close": "12:00:00",
        "sat_opened": True,
        "sat_open": "12:00:00",
        "sat_close": "18:00:00",
        "sun_opened": True,
        "sun_open": "12:00:00",
        "sun_close": "18:00:00"
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
    'description': ['Es ist schnell'],
}

bike_data_bike2 = {
    'name': ['Bike2'],
    'description': ['Es ist weniger schnell'],
}

bike_data_bike3 = {
    'name': ['Bike3'],
    'description': ['Mag ich nicht essen'],
}

equipment_data_lock_and_key = {
    'equipment': 'Lock And Key'
}

equipment_data_mother = {
    'equipment': 'Mother Gudelgunde'
}

def initialize_user_with_token(client, user_data, login_data):
    user = User.objects.create_user(**user_data)
    response = client.post("/api/user/v1/login", login_data)
    response_data = json.loads(response.content.decode('utf-8'))
    token_user = response_data.get('token', None)
    return user, token_user


def add_verified_flag_to_user(user):
    user.user_status.add(User_Status.objects.get(user_status='Verified'))
    user.save()


def add_store_manager_flag_to_user(user, store):
    user.user_status.add(store.store_flag)
    user.is_staff = True
    user.save()


def add_admin_flag_to_user(user):
    user.user_status.add(User_Status.objects.get(user_status='Administrator'))
    user.is_superuser = True
    user.save()


def initialize_store(store_data):
    store = Store.objects.create(**store_data)
    store_flag = User_Status.custom_create_store_flags(store)
    store.store_flag = store_flag
    store.save()
    return store


def initialize_bike_of_store(store, bike_data):
    with open(image_path, 'rb') as image_file:
        image = SimpleUploadedFile("bike_image.jpg", image_file.read(), content_type="image/jpg")
    bike = Bike.objects.create(name=bike_data.get('name')[0], description=bike_data.get('description')[0], image=image,
                               store=store)
    Availability.create_availability(store, bike)
    return bike


def initialize_booking_of_bike_with_flag(user, bike, booking_status_label, begin, end):
    booking = Booking.objects.create(user=user, bike=bike,
                                     begin=datetime.strptime(begin, '%Y-%m-%d').date(),
                                     end=datetime.strptime(end, '%Y-%m-%d').date())
    booking.booking_status.add(Booking_Status.objects.filter(booking_status=booking_status_label)[0].pk)
    if booking_status_label == 'Internal usage':
        booking.booking_status.add(Booking_Status.objects.filter(booking_status='Booked')[0].pk)
    booking_string = generate_random_string(5)
    booking.string = booking_string
    booking.save()
    booking_status_labels_split = ['Booked', 'Internal usage', 'Picked up']
    if booking_status_label in booking_status_labels_split:
        split_availabilities_algorithm(booking)
    return booking


def add_equipment_to_bike(bike, equipment):
    bike.equipment.add(Equipment.objects.get(equipment=equipment))
    bike.save()


def random_exclude_key_value_pairs(data, num_to_exclude):
    keys_to_exclude = random.sample(list(data.keys()), num_to_exclude)
    excluded_data = {key: data[key] for key in data if key not in keys_to_exclude}
    return excluded_data


class Test_registered_equipment(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_all_equipment_various_user_authentication(self):
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_equipment_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/equipment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Equipment.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_equipment_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/equipment')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("equipment"), str))


class Test_user_flags_interactions(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_all_user_flags_various_user_authentication(self):
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_all_user_flags_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/user-flags')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = User_Status.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_user_flag_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/user-flags')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("user_status"), str))

    def test_enrollment_various_user_authentication(self):
        enrollment_data_for_hilda_verified_flag = {
            'contact_data': 'pse_email@gmx.de',
            'user_status': 'Verified'
        }
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_hilda_verified_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_hilda_verified_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_hilda_verified_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_hilda_verified_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_hilda_verified_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        enrollment_data_store1_flag = {
            'contact_data': self.hilda_verified.contact_data,
            'user_status': 'Store: Store1'
        }
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_store1_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_enroll_user_with_flag_already_attached(self):
        enrollment_data_for_caro_as_administrator = {
            'contact_data': self.caro.contact_data,
            'user_status': 'Administrator'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_for_caro_as_administrator,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enrollment_with_various_request_payloads(self):
        enrollment_data_store1_flag = {
            'contact_data': self.hilda_verified.contact_data,
            'user_status': 'Store: Store1'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_store1_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_store1_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        invalid_flags = ['Verified', 'Deleted', 'Reminded', 'Banned', 'Customer']
        for flag in invalid_flags:
            enrollment_data_invalid_user_flag = {
                'contact_data': self.hilda_verified.contact_data,
                'user_status': flag
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
            response = self.client.post('/api/admin/v1/user-flags', enrollment_data_invalid_user_flag, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        enrollment_data_admin_flag = {
            'contact_data': self.hilda_verified.contact_data,
            'user_status': 'Administrator'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_admin_flag, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        enrollment_data_flag_does_not_exist = {
            'contact_data': self.hilda_verified.contact_data,
            'user_status': 'PARTY: YEAH'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_flag_does_not_exist, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        enrollment_data_invalid_contact_data = {
            'contact_data': 'somewhere on campus',
            'user_status': 'Administrator'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_invalid_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        enrollment_data_user_with_contact_data_does_not_exists = {
            'contact_data': 'the_voices_in_my_head@gmx.de',
            'user_status': 'Administrator'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/user-flags', enrollment_data_user_with_contact_data_does_not_exists,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_user_banning(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_ban_user_various_user_authentication(self):
        contact_data_of_user_to_ban = {
            'contact_data': self.hilda_verified.contact_data
        }
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_as_banned_user(self):
        contact_data_of_user_to_ban = {
            'contact_data': self.hilda_verified.contact_data
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post('/api/user/v1/login', login_data_hilda, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = json.loads(response.content.decode('utf-8'))
        expected_json = {
            'detail': 'User inactive or deleted.'
        }
        self.assertEqual(response_data, expected_json)

    def test_ban_user_various_request_payloads(self):
        contact_data_of_user_to_ban = {
            'contact_data': self.hilda_verified.contact_data
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_of_user_to_ban, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact_data_ban_banned_user = {
            'contact_data': self.hilda_verified.contact_data
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_ban_banned_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        contact_data_invalid_contact_data = {
            'contact_data': 'get mad independent'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_invalid_contact_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        contact_data_user_with_contact_data_does_not_exists = {
            'contact_data': 'the_voices_in_my_head@gmx.de'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/ban-user', contact_data_user_with_contact_data_does_not_exists,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #TODO check mail

class Test_store_creation(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_store_creation_various_user_authentication(self):
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_store_creation_various_request_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        store = Store.objects.get(name='Store2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {"id": store.pk, **store_data_store2, "store_flag": store.store_flag.pk})
        store_data_store3 = {
            "region": "KA",
            "address": "Str. 12",
            "phone_number": "012345",
            "email": "pse_email@gmx.de",
            "name": "Store3"
        }
        expected_json = {
            "region": "KA",
            "address": "Str. 12",
            "phone_number": "012345",
            "email": "pse_email@gmx.de",
            "name": "Store3",
            "prep_time": "00:00:00",
            "mon_opened": False,
            "mon_open": "00:00:00",
            "mon_close": "00:00:00",
            "tue_opened": False,
            "tue_open": "00:00:00",
            "tue_close": "00:00:00",
            "wed_opened": False,
            "wed_open": "00:00:00",
            "wed_close": "00:00:00",
            "thu_opened": False,
            "thu_open": "00:00:00",
            "thu_close": "00:00:00",
            "fri_opened": False,
            "fri_open": "00:00:00",
            "fri_close": "00:00:00",
            "sat_opened": False,
            "sat_open": "00:00:00",
            "sat_close": "00:00:00",
            "sun_opened": False,
            "sun_open": "00:00:00",
            "sun_close": "00:00:00",
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store3, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        store = Store.objects.get(name='Store3')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {"id": store.pk, **expected_json, "store_flag": store.store_flag.pk})
        expected_json = {
            "name": [
                "store with this name already exists."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store3, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        store_data_missing_region = {
            "address": "Str. 12",
            "email": "pse_email@gmx.de",
            "name": "Store4"
        }
        expected_json = {
            "region": [
                "This field is required."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_missing_region, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        store_data_missing_address = {
            "region": "KA",
            "email": "pse_email@gmx.de",
            "name": "Store4"
        }
        expected_json = {
            "address": [
                "This field is required."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_missing_address, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        store_data_missing_email = {
            "region": "KA",
            "address": "Str. 12",
            "name": "Store4"
        }
        expected_json = {
            "email": [
                "This field is required."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_missing_email, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        store_data_missing_name = {
            "region": "KA",
            "address": "Str. 12",
            "email": "pse_email@gmx.de"
        }
        expected_json = {
            "name": [
                "This field is required."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_missing_name, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        store_data_missing_address = {
            "region": "KA",
            "address": "Str. 12",
            "email": "I am email if I believe in it!",
            "name": "Store4"
        }
        expected_json = {
            "email": [
                "Enter a valid email address."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_missing_address, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)

    def test_store_creation_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store', store_data_store2, format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        self.assertTrue(isinstance(response_data.get("store_flag"), int))


class Test_create_bike_of_store(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_bike_creation_for_store_various_user_authentication(self):
        bike_data = {
            'name': 'Bike',
            'description': 'Keep trying!',
            'image': open(image_path, 'rb')
        }
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        bike_data = {
            'name': 'Bike',
            'description': 'Keep trying!',
            'image': open(image_path, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_bike(self):
        bike_data = {
            'name': 'Bike',
            'description': 'Keep trying!',
            'image': open(image_path, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bike_creation_for_store_store_id_in_uri_incorrect(self):
        bike_data = {
            'name': 'Bike',
            'description': 'Keep trying!',
            'image': open(image_path, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store/-1/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store/0xF/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store//bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post('/api/admin/v1/create/store/ /bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bike_creation_for_store_various_request_payloads(self):
        bike_data = {
            'name': 'Bike',
            'description': 'Keep trying!',
            'image': open(image_path, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content.decode('utf-8'))
        expected_json = {
            "id": Bike.objects.get(name='Bike').pk,
            "equipment": [],
            "image": Bike.objects.get(name='Bike').image.url,
            "name": "Bike",
            "description": "Keep trying!",
            "store": self.store.pk
        }
        self.assertEqual(response_data, expected_json)
        bike_data_missing_name = {
            'description': 'Keep trying!',
            'image': open(image_path, 'rb'),
        }
        expected_json = {
            "name": [
                "This field may not be null."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data_missing_name,
                                    format='multipart')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        bike_data_missing_description = {
            'name': 'Bike',
            'image': open(image_path, 'rb'),
        }
        expected_json = {
            "description": [
                "This field may not be null."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data_missing_description,
                                    format='multipart')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        bike_data_missing_image = {
            'name': 'Bike',
            'description': 'Keep trying!',
        }
        expected_json = {
            "image": [
                "This field may not be null."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike', bike_data_missing_image,
                                    format='multipart')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)

    def test_bike_creation_for_store_response_payload_format(self):
        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile("bike_image.jpg", image_file.read(), content_type="image/jpg")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/create/store/{self.store.pk}/bike',
                                    {**bike_data_bike1, "image": image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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


class Test_bike_deletion_via_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store1 = initialize_store(store_data_store1)
        self.bike1_of_store1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2_of_store1 = initialize_bike_of_store(self.store1, bike_data_bike2)
        self.store2 = initialize_store(store_data_store2)
        self.bike1_of_store2 = initialize_bike_of_store(self.store2, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store1)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_bike_deletion_via_admin_various_user_authentication(self):
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bike_deletion_via_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(not Bike.objects.filter(name=self.bike1_of_store1.name).exists())
        self.assertTrue(not Availability.objects.filter(bike=self.bike1_of_store1).exists())

    def test_bike_deletion_via_admin_bike_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/0xFFFFFFF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bike_deletion_via_admin_when_bike_picked_up(self):
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-04',
                                                       '2100-01-11')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-18',
                                                       '2100-01-25')
        booking.booking_status.add(Booking_Status.objects.filter(booking_status='Internal usage')[0].pk)
        booking.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)

    def test_bike_deletion_amount_bookings(self):
        booking1 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-04',
                                                        '2100-01-11')
        booking2 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-18',
                                                        '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-18', '2100-01-25')
        amount_bookings = Booking.objects.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/bike/{self.bike1_of_store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking1.refresh_from_db()
        booking2.refresh_from_db()
        expected_booking_status = Booking_Status.objects.get(booking_status='Cancelled')
        self.assertEqual(amount_bookings, Booking.objects.all().count())
        self.assertEqual(booking1.bike, None)
        self.assertIn(expected_booking_status, booking1.booking_status.all())
        self.assertEqual(booking2.bike, None)
        self.assertIn(expected_booking_status, booking2.booking_status.all())

    #TODO check mail

class Test_store_deletion_via_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store1 = initialize_store(store_data_store1)
        self.bike1_of_store1 = initialize_bike_of_store(self.store1, bike_data_bike1)
        self.bike2_of_store1 = initialize_bike_of_store(self.store1, bike_data_bike2)
        self.store2 = initialize_store(store_data_store2)
        self.bike1_of_store2 = initialize_bike_of_store(self.store2, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store1)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_store_deletion_via_admin_various_user_authentication(self):
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_store_deletion_via_admin(self):
        bikes = Bike.objects.filter(store=self.store1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for bike in bikes:
            self.assertTrue(not Bike.objects.filter(name=bike.name).exists())
            self.assertTrue(not Availability.objects.filter(bike=bike).exists())
        self.assertTrue(not Store.objects.filter(name=self.store1.name))

    def test_store_deletion_via_admin_bike_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/0xFFFFFFF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_store_deletion_via_admin_when_bike_picked_up(self):
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-04',
                                                       '2100-01-11')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-18',
                                                       '2100-01-25')
        booking.booking_status.add(Booking_Status.objects.filter(booking_status='Internal usage')[0].pk)
        booking.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)

    def test_store_deletion_amount_bookings(self):
        booking1 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-04',
                                                        '2100-01-11')
        booking2 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-18',
                                                        '2100-01-25')
        booking3 = initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-04',
                                                        '2100-01-11')
        booking4 = initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-18',
                                                        '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-18', '2100-01-25')
        amount_bookings = Booking.objects.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/delete/store/{self.store1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking1.refresh_from_db()
        booking2.refresh_from_db()
        booking3.refresh_from_db()
        booking4.refresh_from_db()
        expected_booking_status = Booking_Status.objects.get(booking_status='Cancelled')
        self.assertEqual(amount_bookings, Booking.objects.all().count())
        self.assertEqual(booking1.bike, None)
        self.assertIn(expected_booking_status, booking1.booking_status.all())
        self.assertEqual(booking2.bike, None)
        self.assertIn(expected_booking_status, booking2.booking_status.all())
        self.assertEqual(booking3.bike, None)
        self.assertIn(expected_booking_status, booking3.booking_status.all())
        self.assertEqual(booking4.bike, None)
        self.assertIn(expected_booking_status, booking4.booking_status.all())

    #TODO check mail

class Test_all_users(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_all_users_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieving_all_users_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = User.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_retrieve_all_user_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("assurance_lvl"), str))
            self.assertTrue(isinstance(item.get("year_of_birth"), int))
            self.assertTrue(isinstance(item.get("contact_data"), str))
            self.assertTrue(isinstance(item.get("username"), str))
            self.assertTrue(isinstance(item.get("preferred_username"), str))
            user_status = item.get("user_status", [])
            for status in user_status:
                self.assertTrue(isinstance(status.get("user_status"), str))

    def test_retrieve_all_users_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            user = User.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), user.pk)
            self.assertEqual(item.get("assurance_lvl"), user.assurance_lvl)
            self.assertEqual(item.get("year_of_birth"), user.year_of_birth)
            self.assertEqual(item.get("contact_data"), user.contact_data)
            self.assertEqual(item.get("username"), user.username)
            self.assertEqual(item.get("preferred_username"), user.preferred_username)
            user_status = item.get("user_status", [])
            self.assertIsInstance(user_status, list)
            user_status_strings = [status.user_status for status in user.user_status.all()]
            for status in user_status:
                self.assertIn(status.get("user_status"), user_status_strings)


class test_retrieve_one_user_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_one_user_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_one_user_user_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/0xFAF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/ ')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_one_user_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(isinstance(response_data.get("assurance_lvl"), str))
        self.assertTrue(isinstance(response_data.get("year_of_birth"), int))
        self.assertTrue(isinstance(response_data.get("contact_data"), str))
        self.assertTrue(isinstance(response_data.get("username"), str))
        self.assertTrue(isinstance(response_data.get("preferred_username"), str))
        user_status = response_data.get("user_status", [])
        for status in user_status:
            self.assertTrue(isinstance(status.get("user_status"), str))

    def test_retrieve_one_user_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.wildegard.pk}')
        response_data = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(contact_data=response_data.get("contact_data"))
        self.assertEqual(response_data.get("assurance_lvl"), user.assurance_lvl)
        self.assertEqual(response_data.get("year_of_birth"), user.year_of_birth)
        self.assertEqual(response_data.get("contact_data"), user.contact_data)
        self.assertEqual(response_data.get("username"), user.username)
        self.assertEqual(response_data.get("preferred_username"), user.preferred_username)
        user_status = response_data.get("user_status", [])
        self.assertIsInstance(user_status, list)
        user_status_strings = [status.user_status for status in user.user_status.all()]
        for status in user_status:
            self.assertIn(status.get("user_status"), user_status_strings)


class Test_all_bookings_of_user_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike3, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike3, 'Booked', '2100-01-18', '2100-01-25')

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_all_bookings_from_user_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieving_all_bookings_from_user_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Booking.objects.filter(user=self.caro).count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_retrieving_all_bookings_from_user_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("bike"), int))
            self.assertTrue(isinstance(item.get("begin"), str))
            self.assertTrue(isinstance(item.get("end"), str))
            self.assertTrue(isinstance(item.get("comment"), str))
            booking_status = item.get("booking_status", [])
            for status in booking_status:
                self.assertTrue(isinstance(status.get("booking_status"), str))
            equipment = item.get("equipment", [])
            for value in equipment:
                self.assertTrue(isinstance(value.get("equipment"), str))
            self.assertIsInstance(item.get("assurance_lvl"), str)
            self.assertIsInstance(item.get("preferred_username"), str)
            user_status = item.get("user_status", [])
            for status in user_status:
                self.assertTrue(isinstance(status.get("user_status"), str))

    def test_retrieving_all_bookings_from_user_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/users/{self.caro.pk}/bookings')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            booking = Booking.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), booking.pk)
            self.assertEqual(datetime.strptime(item.get("begin"), "%Y-%m-%d").date(), booking.begin)
            self.assertEqual(datetime.strptime(item.get("end"), "%Y-%m-%d").date(), booking.end)
            self.assertEqual(item.get("comment"), booking.comment)
            self.assertEqual(item.get("bike"), booking.bike.pk)
            self.assertEqual(item.get("assurance_lvl"), booking.user.assurance_lvl)
            self.assertEqual(item.get("preferred_username"), booking.user.preferred_username)
            booking_status = item.get("booking_status", [])
            booking_status_label = [status.get("booking_status") for status in booking_status]
            for status in booking_status:
                self.assertIn(status.get("booking_status"), booking_status_label)
            equipment = item.get("equipment", [])
            equipment_strings = [value.get("equipment") for value in equipment]
            for value in equipment:
                self.assertIn(value.get("equipment"), equipment_strings)


class Test_all_bookings_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike1, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike3, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike3, 'Booked', '2100-01-18', '2100-01-25')

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_all_bookings_various_user_authentication(self):
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieving_all_bookings_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bookings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Booking.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_retrieving_all_bookings_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bookings')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            self.assertTrue(isinstance(item.get("id"), int))
            self.assertTrue(isinstance(item.get("bike"), int))
            self.assertTrue(isinstance(item.get("begin"), str))
            self.assertTrue(isinstance(item.get("end"), str))
            self.assertTrue(isinstance(item.get("assurance_lvl"), str))
            self.assertTrue(isinstance(item.get("preferred_username"), str))
            booking_status = item.get("booking_status", [])
            for status in booking_status:
                self.assertTrue(isinstance(status.get("booking_status"), str))
            equipment = item.get("equipment", [])
            for value in equipment:
                self.assertTrue(isinstance(value.get("equipment"), str))
            user_status = item.get("user_status", [])
            for status in user_status:
                self.assertTrue(isinstance(status.get("user_status"), str))

    def test_retrieving_all_bookings_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bookings')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            booking = Booking.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), booking.pk)
            self.assertEqual(datetime.strptime(item.get("begin"), "%Y-%m-%d").date(), booking.begin)
            self.assertEqual(datetime.strptime(item.get("end"), "%Y-%m-%d").date(), booking.end)
            self.assertEqual(item.get("comment"), booking.comment)
            self.assertEqual(item.get("bike"), booking.bike.pk)
            self.assertEqual(item.get("assurance_lvl"), booking.user.assurance_lvl)
            self.assertEqual(item.get("preferred_username"), booking.user.preferred_username)
            booking_status = item.get("booking_status", [])
            booking_status_label = [status.get("booking_status") for status in booking_status]
            for status in booking_status:
                self.assertIn(status.get("booking_status"), booking_status_label)
            equipment = item.get("equipment", [])
            equipment_strings = [value.get("equipment") for value in equipment]
            for value in equipment:
                self.assertIn(value.get("equipment"), equipment_strings)


class Test_retrieve_booking_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)
        self.booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2900-01-04',
                                                            '2900-01-11')

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieving_booking_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_booking_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_booking_as_admin_booking_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/0xFAF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/ ')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieving_booking_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(isinstance(response_data.get("bike"), int))
        self.assertTrue(isinstance(response_data.get("begin"), str))
        self.assertTrue(isinstance(response_data.get("end"), str))
        self.assertTrue(isinstance(response_data.get("assurance_lvl"), str))
        self.assertTrue(isinstance(response_data.get("preferred_username"), str))
        booking_status = response_data.get("booking_status", [])
        for status in booking_status:
            self.assertTrue(isinstance(status.get("booking_status"), str))
        equipment = response_data.get("equipment", [])
        for value in equipment:
            self.assertTrue(isinstance(value.get("equipment"), str))
        user_status = response_data.get("user_status", [])
        for status in user_status:
            self.assertTrue(isinstance(status.get("user_status"), str))

    def test_retrieving_booking_as_admin_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bookings/{self.booking.pk}')
        response_data = json.loads(response.content.decode('utf-8'))
        booking = Booking.objects.get(pk=self.booking.pk)
        self.assertEqual(datetime.strptime(response_data.get("begin"), "%Y-%m-%d").date(), booking.begin)
        self.assertEqual(datetime.strptime(response_data.get("end"), "%Y-%m-%d").date(), booking.end)
        self.assertEqual(response_data.get("comment"), booking.comment)
        self.assertEqual(response_data.get("bike"), booking.bike.pk)
        self.assertEqual(response_data.get("assurance_lvl"), booking.user.assurance_lvl)
        self.assertEqual(response_data.get("preferred_username"), booking.user.preferred_username)
        booking_status = response_data.get("booking_status", [])
        booking_status_label = [status.get("booking_status") for status in booking_status]
        for status in booking_status:
            self.assertIn(status.get("booking_status"), booking_status_label)
        equipment = response_data.get("equipment", [])
        equipment_strings = [value.get("equipment") for value in equipment]
        for value in equipment:
            self.assertIn(value.get("equipment"), equipment_strings)

    def test_cancel_booking_as_admin_various_user_authentication(self):
        response = self.client.post(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_booking_as_admin_availabilities(self):
        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking_booked = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '4999-12-27', '5000-01-01')
        self.assertEqual(availability_count_before_booking, Availability.objects.filter(bike=self.bike2).count() - 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_booked.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_before_booking)

    def test_cancel_booking_as_admin(self):
        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking_booked = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2100-01-04', '2100-01-08')
        availability_count_afer_cancel_request = availability_count_before_booking
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_booked.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_afer_cancel_request)

        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking_internal = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Internal usage', '2100-01-11', '2100-01-15')
        availability_count_afer_cancel_request = availability_count_before_booking
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_internal.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_afer_cancel_request)

        booking_picked_up = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Picked up', '2100-01-18', '2100-01-22')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_picked_up.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

        booking_cancelled = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Cancelled', '2100-01-25', '2100-01-29')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_cancelled.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

        booking_returned = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Returned', '2100-02-01', '2100-02-05')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bookings/{booking_returned.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

    #TODO email check


class Test_retrieve_all_bikes_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieve_all_bikes_various_user_authentication(self):
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_bikes_amount_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Bike.objects.all().count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_all_bikes_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bikes')
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

    def test_all_bikes_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/admin/v1/bikes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            bike = Bike.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), bike.pk)
            self.assertEqual(item.get("store"), bike.store.pk)
            self.assertEqual(item.get("name"), bike.name)
            self.assertEqual(item.get("description"), bike.description)
            self.assertEqual(item.get("image"), bike.image.url)
            equipment = item.get("equipment", [])
            equipment_strings = [value.get("equipment") for value in equipment]
            for value in equipment:
                self.assertIn(value.get("equipment"), equipment_strings)


class Test_retrieve_bike_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieve_bike_as_admin_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bike_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
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

    def test_bike_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        bike = Bike.objects.get(pk=response_data.get("id"))
        self.assertEqual(response_data.get("id"), bike.pk)
        self.assertEqual(response_data.get("store"), bike.store.pk)
        self.assertEqual(response_data.get("name"), bike.name)
        self.assertEqual(response_data.get("description"), bike.description)
        self.assertEqual(response_data.get("image"), bike.image.url)
        equipment = response_data.get("equipment", [])
        equipment_strings = [value.get("equipment") for value in equipment]
        for value in equipment:
            self.assertIn(value.get("equipment"), equipment_strings)

    def test_bike_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/booking/v1/bikes/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/booking/v1/bikes/0xF')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get('/api/booking/v1/bikes/ ')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_retrieve_availabilities_of_bike_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieve_availabilities_of_bike_as_admin_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_availabilities_of_bike_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
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

    def test_retrieve_availabilities_of_bike_amount_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Availability.objects.filter(bike=self.bike1).count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_retrieve_availabilities_of_bike_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/bikes/{self.bike1.pk}/availability')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            availability = Availability.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), availability.pk)
            self.assertEqual(datetime.strptime(item.get("from_date"), "%Y-%m-%d").date(), availability.from_date)
            self.assertEqual(datetime.strptime(item.get("until_date"), "%Y-%m-%d").date(), availability.until_date)
            self.assertEqual(item.get("store"), availability.store.pk)
            self.assertEqual(item.get("bike"), availability.bike.pk)
            availability_status = item.get("availability_status", [])
            availability_strings = [value.get("availability_status") for value in availability_status]
            for value in availability_status:
                self.assertIn(value.get("availability_status"), availability_strings)


class Test_all_stores_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_all_stores_as_admin_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_stores_amount_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Store.objects.count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_all_stores_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores')
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
            self.assertTrue(isinstance(item.get("store_flag"), int))

    def test_all_stores_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            store = Store.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), store.id)
            self.assertEqual(item.get("region"), store.region)
            self.assertEqual(item.get("address"), store.address)
            self.assertEqual(item.get("phone_number"), store.phone_number)
            self.assertEqual(item.get("email"), store.email)
            self.assertEqual(item.get("name"), store.name)
            self.assertEqual(item.get("prep_time"), str(store.prep_time))
            self.assertEqual(item.get("mon_opened"), store.mon_opened)
            self.assertEqual(item.get("mon_open"), str(store.mon_open))
            self.assertEqual(item.get("mon_close"), str(store.mon_close))
            self.assertEqual(item.get("tue_opened"), store.tue_opened)
            self.assertEqual(item.get("tue_open"), str(store.tue_open))
            self.assertEqual(item.get("tue_close"), str(store.tue_close))
            self.assertEqual(item.get("wed_opened"), store.wed_opened)
            self.assertEqual(item.get("wed_open"), str(store.wed_open))
            self.assertEqual(item.get("wed_close"), str(store.wed_close))
            self.assertEqual(item.get("thu_opened"), store.thu_opened)
            self.assertEqual(item.get("thu_open"), str(store.thu_open))
            self.assertEqual(item.get("thu_close"), str(store.thu_close))
            self.assertEqual(item.get("fri_opened"), store.fri_opened)
            self.assertEqual(item.get("fri_open"), str(store.fri_open))
            self.assertEqual(item.get("fri_close"), str(store.fri_close))
            self.assertEqual(item.get("sat_opened"), store.sat_opened)
            self.assertEqual(item.get("sat_open"), str(store.sat_open))
            self.assertEqual(item.get("sat_close"), str(store.sat_close))
            self.assertEqual(item.get("sun_opened"), store.sun_opened)
            self.assertEqual(item.get("sun_open"), str(store.sun_open))
            self.assertEqual(item.get("sun_close"), str(store.sun_close))
            self.assertEqual(item.get("store_flag"), store.store_flag.pk)


class Test_retrieve_store_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieve_store_as_admin_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_store_as_admin_store_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/0xf69F')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/ ')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_store_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
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
        self.assertTrue(isinstance(response_data.get("store_flag"), int))

    def test_retrieve_store_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        store = Store.objects.get(pk=response_data.get("id"))
        self.assertEqual(response_data.get("id"), store.id)
        self.assertEqual(response_data.get("region"), store.region)
        self.assertEqual(response_data.get("address"), store.address)
        self.assertEqual(response_data.get("phone_number"), store.phone_number)
        self.assertEqual(response_data.get("email"), store.email)
        self.assertEqual(response_data.get("name"), store.name)
        self.assertEqual(response_data.get("prep_time"), str(store.prep_time))
        self.assertEqual(response_data.get("mon_opened"), store.mon_opened)
        self.assertEqual(response_data.get("mon_open"), str(store.mon_open))
        self.assertEqual(response_data.get("mon_close"), str(store.mon_close))
        self.assertEqual(response_data.get("tue_opened"), store.tue_opened)
        self.assertEqual(response_data.get("tue_open"), str(store.tue_open))
        self.assertEqual(response_data.get("tue_close"), str(store.tue_close))
        self.assertEqual(response_data.get("wed_opened"), store.wed_opened)
        self.assertEqual(response_data.get("wed_open"), str(store.wed_open))
        self.assertEqual(response_data.get("wed_close"), str(store.wed_close))
        self.assertEqual(response_data.get("thu_opened"), store.thu_opened)
        self.assertEqual(response_data.get("thu_open"), str(store.thu_open))
        self.assertEqual(response_data.get("thu_close"), str(store.thu_close))
        self.assertEqual(response_data.get("fri_opened"), store.fri_opened)
        self.assertEqual(response_data.get("fri_open"), str(store.fri_open))
        self.assertEqual(response_data.get("fri_close"), str(store.fri_close))
        self.assertEqual(response_data.get("sat_opened"), store.sat_opened)
        self.assertEqual(response_data.get("sat_open"), str(store.sat_open))
        self.assertEqual(response_data.get("sat_close"), str(store.sat_close))
        self.assertEqual(response_data.get("sun_opened"), store.sun_opened)
        self.assertEqual(response_data.get("sun_open"), str(store.sun_open))
        self.assertEqual(response_data.get("sun_close"), str(store.sun_close))
        self.assertEqual(response_data.get("store_flag"), store.store_flag.pk)


class Test_retrieve_availabilities_of_store_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_retrieve_availabilities_of_store_as_admin_various_user_authentication(self):
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_availabilities_of_store_amount_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(response_data, list)
        expected_object_count = Availability.objects.filter(bike__store=self.store).count()
        self.assertEqual(len(response_data), expected_object_count)

    def test_retrieve_availabilities_of_store_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        initialize_booking_of_bike_with_flag(self.caro, self.bike1, 'Booked', '2100-01-04', '2100-01-11')
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
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

    def test_retrieve_availabilities_of_store_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.get(f'/api/admin/v1/stores/{self.store.pk}/availability')
        response_data = json.loads(response.content.decode('utf-8'))
        for item in response_data:
            availability = Availability.objects.get(pk=item.get("id"))
            self.assertEqual(item.get("id"), availability.pk)
            self.assertEqual(datetime.strptime(item.get("from_date"), "%Y-%m-%d").date(), availability.from_date)
            self.assertEqual(datetime.strptime(item.get("until_date"), "%Y-%m-%d").date(), availability.until_date)
            self.assertEqual(item.get("store"), availability.store.pk)
            self.assertEqual(item.get("bike"), availability.bike.pk)
            availability_status = item.get("availability_status", [])
            availability_strings = [value.get("availability_status") for value in availability_status]
            for value in availability_status:
                self.assertIn(value.get("availability_status"), availability_strings)


class Test_partial_update_of_store_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_partial_update_of_store_as_admin(self):
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_of_store_as_admin_store_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/-666/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/0x29A/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/ /update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores//update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_of_store_as_admin_response_payload_format(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
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
        self.assertTrue(isinstance(response_data.get("store_flag"), int))

    def test_partial_update_of_store_as_admin_response_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        store = Store.objects.get(pk=response_data.get("id"))
        self.assertEqual(response_data.get("id"), store.id)
        self.assertEqual(response_data.get("region"), store.region)
        self.assertEqual(response_data.get("address"), store.address)
        self.assertEqual(response_data.get("phone_number"), store.phone_number)
        self.assertEqual(response_data.get("email"), store.email)
        self.assertEqual(response_data.get("name"), store.name)
        self.assertEqual(response_data.get("prep_time"), str(store.prep_time))
        self.assertEqual(response_data.get("mon_opened"), store.mon_opened)
        self.assertEqual(response_data.get("mon_open"), str(store.mon_open))
        self.assertEqual(response_data.get("mon_close"), str(store.mon_close))
        self.assertEqual(response_data.get("tue_opened"), store.tue_opened)
        self.assertEqual(response_data.get("tue_open"), str(store.tue_open))
        self.assertEqual(response_data.get("tue_close"), str(store.tue_close))
        self.assertEqual(response_data.get("wed_opened"), store.wed_opened)
        self.assertEqual(response_data.get("wed_open"), str(store.wed_open))
        self.assertEqual(response_data.get("wed_close"), str(store.wed_close))
        self.assertEqual(response_data.get("thu_opened"), store.thu_opened)
        self.assertEqual(response_data.get("thu_open"), str(store.thu_open))
        self.assertEqual(response_data.get("thu_close"), str(store.thu_close))
        self.assertEqual(response_data.get("fri_opened"), store.fri_opened)
        self.assertEqual(response_data.get("fri_open"), str(store.fri_open))
        self.assertEqual(response_data.get("fri_close"), str(store.fri_close))
        self.assertEqual(response_data.get("sat_opened"), store.sat_opened)
        self.assertEqual(response_data.get("sat_open"), str(store.sat_open))
        self.assertEqual(response_data.get("sat_close"), str(store.sat_close))
        self.assertEqual(response_data.get("sun_opened"), store.sun_opened)
        self.assertEqual(response_data.get("sun_open"), str(store.sun_open))
        self.assertEqual(response_data.get("sun_close"), str(store.sun_close))
        self.assertEqual(response_data.get("store_flag"), store.store_flag.pk)

    def test_partial_update_of_store_as_admin_various_request_payloads(self):
        for i in range(1, 25):
            update_store_random_data = random_exclude_key_value_pairs(update_store_data, i)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
            response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_random_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = json.loads(response.content.decode('utf-8'))
            store = Store.objects.get(pk=response_data.get("id"))
            self.assertEqual(response_data.get("id"), store.id)
            self.assertEqual(response_data.get("region"), store.region)
            self.assertEqual(response_data.get("address"), store.address)
            self.assertEqual(response_data.get("phone_number"), store.phone_number)
            self.assertEqual(response_data.get("email"), store.email)
            self.assertEqual(response_data.get("name"), store.name)
            self.assertEqual(response_data.get("prep_time"), str(store.prep_time))
            self.assertEqual(response_data.get("mon_opened"), store.mon_opened)
            self.assertEqual(response_data.get("mon_open"), str(store.mon_open))
            self.assertEqual(response_data.get("mon_close"), str(store.mon_close))
            self.assertEqual(response_data.get("tue_opened"), store.tue_opened)
            self.assertEqual(response_data.get("tue_open"), str(store.tue_open))
            self.assertEqual(response_data.get("tue_close"), str(store.tue_close))
            self.assertEqual(response_data.get("wed_opened"), store.wed_opened)
            self.assertEqual(response_data.get("wed_open"), str(store.wed_open))
            self.assertEqual(response_data.get("wed_close"), str(store.wed_close))
            self.assertEqual(response_data.get("thu_opened"), store.thu_opened)
            self.assertEqual(response_data.get("thu_open"), str(store.thu_open))
            self.assertEqual(response_data.get("thu_close"), str(store.thu_close))
            self.assertEqual(response_data.get("fri_opened"), store.fri_opened)
            self.assertEqual(response_data.get("fri_open"), str(store.fri_open))
            self.assertEqual(response_data.get("fri_close"), str(store.fri_close))
            self.assertEqual(response_data.get("sat_opened"), store.sat_opened)
            self.assertEqual(response_data.get("sat_open"), str(store.sat_open))
            self.assertEqual(response_data.get("sat_close"), str(store.sat_close))
            self.assertEqual(response_data.get("sun_opened"), store.sun_opened)
            self.assertEqual(response_data.get("sun_open"), str(store.sun_open))
            self.assertEqual(response_data.get("sun_close"), str(store.sun_close))
            self.assertEqual(response_data.get("store_flag"), store.store_flag.pk)
        expected_json = [
            "Updating field is not allowed."
        ]
        update_store_data_invalid_field = {
            "region": "MAL"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data_invalid_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        update_store_data_invalid_field = {
            "id": 666
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data_invalid_field,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        update_store_data_invalid_field = {
            "store_flag": 999
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data_invalid_field,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        update_store_data_invalid_field = {
            "name": "Compilerbau"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/stores/{self.store.pk}/update', update_store_data_invalid_field,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)


class Test_partial_update_of_bike_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_partial_update_of_bike_as_admin_various_user_authentication(self):
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_of_bike_as_admin_response_payload_format(self):
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
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

    def test_partial_update_of_bike_as_admin_response_payload(self):
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        bike = Bike.objects.get(pk=response_data.get("id"))
        self.assertEqual(response_data.get("id"), bike.pk)
        self.assertEqual(response_data.get("store"), bike.store.pk)
        self.assertEqual(response_data.get("name"), bike.name)
        self.assertEqual(response_data.get("description"), bike.description)
        self.assertEqual(response_data.get("image"), bike.image.url)
        equipment = response_data.get("equipment", [])
        equipment_strings = [value.get("equipment") for value in equipment]
        for value in equipment:
            self.assertIn(value.get("equipment"), equipment_strings)

    def test_partial_update_of_bike_bike_id_in_uri_incorrect(self):
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/-3/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/0x27A/update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/ /update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes//update', update_bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_of_bike_as_admin_various_request_payloads(self):
        update_bike_data = {
            'name': 'Up to date',
            'description': 'at 3 am',
            'image': open(image_path_update, 'rb')
        }
        for i in range(1, 3):
            update_bike_random_data = random_exclude_key_value_pairs(update_bike_data, i)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
            response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_random_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = json.loads(response.content.decode('utf-8'))
            bike = Bike.objects.get(pk=response_data.get("id"))
            self.assertEqual(response_data.get("id"), bike.pk)
            self.assertEqual(response_data.get("store"), bike.store.pk)
            self.assertEqual(response_data.get("name"), bike.name)
            self.assertEqual(response_data.get("description"), bike.description)
            self.assertEqual(response_data.get("image"), bike.image.url)
            equipment = response_data.get("equipment", [])
            equipment_strings = [value.get("equipment") for value in equipment]
            for value in equipment:
                self.assertIn(value.get("equipment"), equipment_strings)
        expected_json = [
            "Updating field is not allowed."
        ]
        update_bike_data_invalid_field = {
            "store": 69
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data_invalid_field, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        update_bike_data_invalid_field = {
            "equipment": ["Food"]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data_invalid_field, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        update_bike_data_invalid_field = {
            "id": 6996
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.patch(f'/api/admin/v1/bikes/{self.bike1.pk}/update', update_bike_data_invalid_field, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)


class Test_equipment_to_bike_as_admin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.bike3 = initialize_bike_of_store(self.store, bike_data_bike3)
        self.wildegard, self.token_wildegard = initialize_user_with_token(
            self.client, user_data_wildegard, login_data_wildegard
        )
        self.hilda_verified, self.token_hilda_verified = initialize_user_with_token(
            self.client, user_data_hilda, login_data_hilda
        )
        add_verified_flag_to_user(self.hilda_verified)
        self.store_manager, self.store_manager_token = initialize_user_with_token(
            self.client, user_data_store_manager, login_data_store_manager
        )
        add_verified_flag_to_user(self.store_manager)
        add_store_manager_flag_to_user(self.store_manager, self.store)
        self.caro, self.caro_token = initialize_user_with_token(
            self.client, user_data_caro, login_data_caro
        )
        add_verified_flag_to_user(self.caro)
        add_admin_flag_to_user(self.caro)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_add_equipment_to_bike_as_admin_various_user_authentication(self):
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_equipment_to_bike_as_admin_amount(self):
        equipment_amount_start = Equipment.objects.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(equipment_amount_start, Equipment.objects.all().count())
        self.assertEqual(self.bike1.equipment.count(), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_mother, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(equipment_amount_start + 1, Equipment.objects.all().count())
        self.assertEqual(self.bike1.equipment.count(), 2)

    def test_add_equipment_to_bike_as_admin_bike_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/-8/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/0x27A/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes//equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/admin/v1/bikes/ /equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_equipment_from_bike_as_admin_various_user_authentication(self):
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_equipment_from_bike_as_admin_amount(self):
        add_equipment_to_bike(self.bike1, 'Lock And Key')
        add_equipment_to_bike(self.bike1, 'Tarp')
        bike_equipment_before = self.bike1.equipment.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes/{self.bike1.pk}/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.bike1.equipment.count(), bike_equipment_before - 1)

    def test_remove_equipment_from_bike_as_admin_bike_id_in_uri_incorrect(self):
        add_equipment_to_bike(self.bike1, 'Lock And Key')
        add_equipment_to_bike(self.bike1, 'Tarp')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes/-8/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes/0x27A/equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes//equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/admin/v1/bikes/ /equipment', equipment_data_lock_and_key, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)