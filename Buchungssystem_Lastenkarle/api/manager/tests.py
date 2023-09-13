import os
from datetime import timedelta

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

user_data = {
    'username': 'Wildegard',
    'password': 'password',
    'contact_data': 'wilde.gard@gmx.de',
    'year_of_birth': '1901'
}
login_data = {
    'username': 'Wildegard',
    'password': 'password'
}
user_data_2 = {
    'username': 'Wilderich',
    'password': 'password',
    'contact_data': 'the_voices_in_my_head@gmx.de',
    'year_of_birth': '1901'
}
login_data_2 = {
    'username': 'Wilderich',
    'password': 'password'
}
manager_data_1 = {
    'username': 'Hildegard',
    'password': 'password',
    'contact_data': 'koeri_werk@gmx.de',
    'year_of_birth': '1901'
}
manager_login_data_1 = {
    'username': 'Hildegard',
    'password': 'password'
}
manager_data_2 = {
    'username': 'Hilderich',
    'password': 'password',
    'contact_data': 'mathebau@gmx.de',
    'year_of_birth': '1901'
}
manager_login_data_2 = {
    'username': 'Hilderich',
    'password': 'password'
}

store_data1 = {
    'name': 'Store1',
    'address': 'Storestr. 1',
    'email': 'pse_email@gmx.de',
    'region': 'KA',
    'phone_number': '012345',
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

store_data2 = {
    'name': 'Store2',
    'address': 'Storestr. 2',
    'email': 'bitte_toete_mich@gmx.de',
    'region': 'KA',
    'phone_number': '012345',
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

bike1_data = {
    'name': ['Bike1'],
    'description': ['Es ist schnell']
}
booking_data = {
    "begin": "2023-10-02",
    "end": "2023-10-03",
    "equipment": []
}
booking_data_2 = {
    "begin": "2023-10-04",
    "end": "2023-10-05",
    "equipment": ["Tarp", "Charger"]
}
booking_data_3 = {
    "begin": "2023-10-09",
    "end": "2023-10-10",
    "equipment": []
}
booking_data_4 = {
    "begin": "2023-10-11",
    "end": "2023-10-12",
    "equipment": []
}
local_user_data = {
    "first_name": "Wildegard",
    "last_name": "Wilde",
    "address": "Wildestraße 1, 01235 Wildhausen",
    "id_number": "123"
}

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


def initializer_local_data_of_user(user, local_data):
    data = LocalData.objects.create(user=user, date_of_verification=datetime.now().date() + timedelta(days=180),
                                    **local_data)
    return data


def random_exclude_key_value_pairs(data, num_to_exclude):
    keys_to_exclude = random.sample(list(data.keys()), num_to_exclude)
    excluded_data = {key: data[key] for key in data if key not in keys_to_exclude}
    return excluded_data


class Test_bike_deletion_as_store_manager(TestCase):
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

    def test_bike_deletion_as_store_manager_various_user_authentication(self):
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bike_deletion_as_store_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(not Bike.objects.filter(name=self.bike1_of_store1.name).exists())
        self.assertTrue(not Availability.objects.filter(bike=self.bike1_of_store1).exists())

    def test_bike_deletion_as_store_manager_bike_id_in_uri_incorrect(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/-1/delete')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/0x32A/delete')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/ /delete')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes//delete')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bike_deletion_as_store_manager_when_bike_picked_up(self):
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-04',
                                                       '2100-01-11')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)
        booking = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Picked up', '2100-01-18',
                                                       '2100-01-25')
        booking.booking_status.add(Booking_Status.objects.filter(booking_status='Internal usage')[0].pk)
        booking.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(booking.bike, None)

    def test_bike_deletion_as_store_manager_amount_bookings(self):
        booking1 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-04',
                                                        '2100-01-11')
        booking2 = initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store1, 'Booked', '2100-01-18',
                                                        '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike2_of_store1, 'Booked', '2100-01-18', '2100-01-25')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-04', '2100-01-11')
        initialize_booking_of_bike_with_flag(self.caro, self.bike1_of_store2, 'Booked', '2100-01-18', '2100-01-25')
        amount_bookings = Booking.objects.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.delete(f'/api/manager/v1/bikes/{self.bike1_of_store1.pk}/delete')
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


class Test_cancel_booking_as_store_manager(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store1)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.other_store = initialize_store(store_data_store2)
        self.bike_other_store = initialize_bike_of_store(self.other_store, bike_data_bike3)
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

    def test_cancel_booking_as_store_manager_various_user_authentication(self):
        response = self.client.post(f'/api/manager/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/manager/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/manager/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/manager/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{self.booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_booking_as_store_manager_availabilities(self):
        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '4999-12-27', '5000-01-01')
        self.assertEqual(availability_count_before_booking, Availability.objects.filter(bike=self.bike2).count() - 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_before_booking)

    def test_cancel_booking_of_other_store_as_store_manager(self):
        booking_other_store = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike_other_store, 'Booked', '2100-01-04', '2100-01-08')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking_other_store.pk}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_booking_as_store_manager(self):
        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2100-01-04', '2100-01-08')
        availability_count_afer_cancel_request = availability_count_before_booking
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_afer_cancel_request)

        availability_count_before_booking = Availability.objects.filter(bike=self.bike2).count()
        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Internal usage', '2100-01-11', '2100-01-15')
        availability_count_afer_cancel_request = availability_count_before_booking
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_afer_cancel_request)

        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Picked up', '2100-01-18', '2100-01-22')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Cancelled', '2100-01-25', '2100-01-29')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

        booking = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Returned', '2100-02-01', '2100-02-05')
        availability_count_after_booking = Availability.objects.filter(bike=self.bike2).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        availability_count_compare = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_compare, availability_count_after_booking)

    #TODO email check


class Test_make_internal_booking_as_store_manager(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store = initialize_store(store_data_store2)
        self.bike1 = initialize_bike_of_store(self.store, bike_data_bike1)
        self.bike2 = initialize_bike_of_store(self.store, bike_data_bike2)
        self.other_store = initialize_store(store_data_store1)
        self.bike_other_store = initialize_bike_of_store(self.other_store, bike_data_bike3)
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
        self.booking1 = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2100-01-04',
                                                       '2100-01-08')
        self.booking2 = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Booked', '2100-01-11',
                                                       '2100-01-15')
        self.booking3 = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Picked up', '2100-01-18',
                                                       '2100-01-22')
        self.booking4 = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Cancelled', '2100-01-25',
                                                       '2100-01-29')
        self.booking5 = initialize_booking_of_bike_with_flag(self.hilda_verified, self.bike2, 'Returned', '2100-02-01',
                                                       '2100-02-05')

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_make_internal_booking_various_user_authentication(self):
        booking_data1_bike1 = {
            'from_date': '2100-01-04',
            'until_date': '2100-01-11',
            'equipment': []
        }
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_wildegard)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_hilda_verified)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.caro_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_internal_booking_availability_handling_edge_case(self):
        booking_data1_bike1 = {
            'from_date': '4999-12-27',
            'until_date': '5000-01-01',
            'equipment': []
        }
        availability_count_after_booking = Availability.objects.all().count() + 1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data1_bike1,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(availability_count_after_booking, Availability.objects.all().count())

    def test_make_internal_booking_invalid_time_frames_various_request_payloads(self):
        booking_data_for_past = {
            'from_date': '1100-01-03',
            'until_date': '1100-01-10',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store does not provide bike this early."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_for_past,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_for_time_travel = {
            'from_date': '2200-01-10',
            'until_date': '2200-01-03',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Time travel is not permitted."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_for_time_travel,
                                    format='json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_json)
        booking_data_for_closed_on_begin_day = {
            'from_date': '2200-01-11',
            'until_date': '2200-01-16',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store closed on starting day of booking."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_for_closed_on_begin_day,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        booking_data_for_closed_on_end_day = {
            'from_date': '2200-01-10',
            'until_date': '2200-01-12',
            'equipment': []
        }
        expected_json = {
            "non_field_errors": [
                "Store closed on ending day of booking."
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_for_closed_on_end_day, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)

    def test_make_internal_booking_valid_time_frames_various_request_payloads(self):
        booking_status_cancelled = Booking_Status.objects.get(booking_status='Cancelled').booking_status
        availability_count_before = Availability.objects.filter(bike=self.bike2).count()
        booking_data_successful = {
            'from_date': '2100-01-01',
            'until_date': '2100-01-15',
            'equipment': []
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_successful,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        availability_count_now = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_before - 2, availability_count_now)
        self.assertEqual(booking_status_cancelled, self.booking1.booking_status.all().first().booking_status)
        availability_count_before = Availability.objects.filter(bike=self.bike2).count()

        booking_data_successful = {
            'from_date': '2100-01-25',
            'until_date': '2100-02-19',
            'equipment': []
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_successful,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        availability_count_now = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_before + 2, availability_count_now)


    def test_make_internal_booking_not_possible(self):
        availability_count_before = Availability.objects.filter(bike=self.bike2).count()
        booking_data_no_time_restriction = {
            'from_date': '2100-01-15',
            'until_date': '2100-01-25',
            'equipment': []
        }
        expected_json = {
            "error": "Please select a different time frame in which the bike is available."
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.store_manager_token)
        response = self.client.post(f'/api/manager/v1/bikes/{self.bike2.pk}/internal-booking', booking_data_no_time_restriction, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_json)
        availability_count_now = Availability.objects.filter(bike=self.bike2).count()
        self.assertEqual(availability_count_before, availability_count_now)


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.store_data = {
            'region': 'KA',
            'address': 'Test Address',
            'phone_number': '1234567890',
            'email': 'koeri_werk@gmx.de',
            'name': 'Test Store',
            'prep_time': '01:00',
            'mon_opened': True,
            'mon_open': '08:00',
            'mon_close': '17:00',
        }
        # Create a test store
        self.store = Store.objects.create(**self.store_data)
        self.store_flag = User_Status.custom_create_store_flags(self.store)
        self.store.store_flag = self.store_flag
        self.store.save()
        # Create a test user with the necessary permissions
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # login user
        response = self.client.post('/api/user/v1/login', self.login_data)
        # Parse the response content to get the token
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
        self.user.is_staff = True
        self.user.user_status.add(User_Status.objects.get(user_status='Verified'))
        self.user.user_status.add(User_Status.objects.get(user_status='Store: Test Store'))
        self.user.save()

        # Create the second store and its manager (who does not meet the requirements)
        self.store2 = Store.objects.create(name='Test Store 2')
        self.store_flag2 = User_Status.custom_create_store_flags(self.store2)
        self.store2.store_flag = self.store_flag2
        self.store2.save()
        # Manager for store2
        self.user_data2 = {
            'username': 'testuser2',
            'password': 'testpassword2',
            'contact_data': 'pse_email@gmx.de',
            'year_of_birth': '1990'
        }
        self.login_data2 = {
            'username': 'testuser2',
            'password': 'testpassword2'
        }

        self.user2 = User.objects.create_user(**self.user_data2)
        response2 = self.client.post("/api/user/v1/login", self.login_data2)
        response_data2 = json.loads(response2.content.decode('utf-8'))
        self.token2 = response_data2.get('token', None)
        self.user2.is_staff = True
        self.user2.user_status.add(User_Status.objects.get(user_status='Verified'))
        self.user2.user_status.add(User_Status.objects.get(user_status='Store: Test Store 2'))
        # User without permissions whatsoever
        self.user_data3 = {
            'username': 'testuser3',
            'password': 'testpassword3',
            'contact_data': 'ich_bin_fag@gmx.de',
            'year_of_birth': '1990'
        }
        self.login_data3 = {
            'username': 'testuser3',
            'password': 'testpassword3'
        }

        self.user3 = User.objects.create_user(**self.user_data3)
        response3 = self.client.post("/api/user/v1/login", self.login_data3)
        response_data3 = json.loads(response3.content.decode('utf-8'))
        self.token3 = response_data3.get('token', None)
        self.user3.is_staff = True
        self.user3.user_status.add(User_Status.objects.get(user_status='Verified'))


class RegisteredEquipmentTestCase(BaseTestCase):
    # user is shop owner and meets requirements
    def setUp(self):
        super().setUp()
        # Create a bike associated with the store
        self.bike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')

        # Create equipment for bike
        self.equipment1 = Equipment.objects.create(equipment='Klingel')
        self.equipment2 = Equipment.objects.create(equipment='Schloss')

        # Add the equipment items to the bike's equipment field
        self.bike.equipment.add(self.equipment1, self.equipment2)

    def test_registered_equipment_api(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Make a GET request to the API endpoint
        response = self.client.get('/api/manager/v1/equipment')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data is a list
        self.assertIsInstance(response.data, list)

        self.assertEqual(len(response.data),
                         7)  # We have two equipment items in the set up, 5 default Equipment + 2 new
        self.assertEqual(response.data[5]['equipment'], 'Klingel')
        self.assertEqual(response.data[6]['equipment'], 'Schloss')

    def test_user_without_permissions(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)

        # Make a GET request to the API endpoint
        response = self.client.get('/api/manager/v1/equipment')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StorePageTestCase(BaseTestCase):
    # user meets requirements
    def setUp(self):
        super().setUp()

    def test_store_page_api(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Make a GET request to the API endpoint
        response = self.client.get('/api/manager/v1/store-page')
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data matches the store data
        response_data = response.json()
        self.assertEqual(response_data['id'], self.store.pk)
        self.assertEqual(response_data['name'], self.store.name)

    def test_store_page_api_wrong_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)

        # Make a GET request to the API endpoint for store
        response = self.client.get('/api/manager/v1/store-page')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expect a 403 Forbidden

    def test_store_page_api_not_a_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)

        # Make a GET request to the API endpoint of store2
        response = self.client.get('/api/manager/v1/store-page')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expect a 403 Forbidden

    def test_store_page_api_user_has_no_permissions(self):
        self.user3.is_staff = False

        response = self.client.get('/api/manager/v1/store-page')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StorePagePatchTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Simulate PATCH request with updated data
        self.patch_data = {
            'mon_opened': False,
            'email': 'bitte_toete_mich@gmx.de',
        }

    def test_patch_store(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Make the PATCH request
        response = self.client.patch('/api/manager/v1/store-page', self.patch_data, fromat='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the store object from the database and assert field updates
        self.store.refresh_from_db()
        assert self.store.mon_opened == self.patch_data['mon_opened']
        assert self.store.email == self.patch_data['email']
        assert self.store.region == self.store_data['region']  # to check if the unchanged data stayed the same
        assert self.store.address == self.store_data['address']

    def test_patch_store_wrong_manager(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)

        # Make the PATCH request
        response = self.client.patch('/api/manager/v1/store-page', self.patch_data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # access shouldn't be possible

        # Refresh the store object
        self.store.refresh_from_db()
        assert self.store.mon_opened == self.store_data['mon_opened']
        assert self.store.email == self.store_data['email']
        assert self.store.email != self.patch_data['email']
        assert self.store.mon_opened != self.patch_data['mon_opened']

    def test_patch_store_no_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)
        response = self.client.patch('/api/manager/v1/store-page', self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Refresh the store object
        self.store.refresh_from_db()
        assert self.store.mon_opened == self.store_data['mon_opened']
        assert self.store.email == self.store_data['email']
        assert self.store.email != self.patch_data['email']
        assert self.store.mon_opened != self.patch_data['mon_opened']


class EnrollUserTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user3.is_staff = False

    def test_enroll_user_not_manager_yet(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'contact_data': self.user3.contact_data
        }
        response = self.client.post('/api/manager/v1/enrollment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the user is now a staff member
        self.user3.refresh_from_db()
        self.assertTrue(self.user3.is_staff, msg='User3 is now staff')
        assert self.user3.is_staff_of_store() == self.store

    def test_enroll_user_already_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'contact_data': self.user2.contact_data
        }
        response = self.client.post('/api/manager/v1/enrollment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if user2 is still manager of store2 and not store
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.user_status.all().filter(user_status='Store: Test Store').exists())
        self.assertTrue(self.user2.user_status.all().filter(user_status='Store: Test Store 2').exists())


class GetAllBikesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a bike associated with the store
        self.boomBike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')
        self.niceBike = Bike.objects.create(store=self.store, name='NiceBike', description='NonExplosive')

        # Create a bike associated with store 2
        self.otherBike = Bike.objects.create(store=self.store2, name='OtherBike', description='Mean')

    def test_get_bikes_of_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Make a GET request to the BikesOfStore API view
        response = self.client.get('/api/manager/v1/bikes')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the expected bike names
        self.assertContains(response, self.boomBike.name)
        self.assertContains(response, self.niceBike.name)

    def test_get_bikes_of_other_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Make a GET request to the BikesOfStore API view
        response = self.client.get('/api/manager/v1/bikes')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data does not contain bikes from the other store
        self.assertNotContains(response, self.otherBike)


class AddBikeToStoreTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.bike_data = {
            'name': 'NewBi',
            'description': 'SmolBebi',
            'image': open(image_path, 'rb')
        }

    def test_create_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/manager/v1/bikes', data=self.bike_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            new_bike = Bike.objects.get(name='NewBi')
            self.assertEqual(new_bike.description, 'SmolBebi')
            self.assertEqual(new_bike.store, self.store)
        except Bike.DoesNotExist:
            self.fail("Newly created bike does not exist")

    def test_create_bike_without_permission(self):
        # Authenticate as a user without the necessary permissions
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)
        # Get the count of bikes before making the request
        initial_bike_count = Bike.objects.count()

        response = self.client.post('/api/manager/v1/bikes', data=self.bike_data, format='multipart')
        # Check that unauthorized access is denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure that the bike count in the database has not changed
        self.assertEqual(Bike.objects.count(), initial_bike_count)


class AddEquipmentToBikeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a bike associated with the store
        self.boomBike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')
        self.niceBike = Bike.objects.create(store=self.store, name='NiceBike', description='NonExplosive')

        # Create a bike associated with store 2
        self.otherBike = Bike.objects.create(store=self.store2, name='MeanBike', description='Mean')

    def test_add_equipment_to_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Define the equipment label you want to add to the bike (e.g., 'Lock And Key')
        equipment_label = 'Lock And Key'
        # Send a POST request to add the equipment to the boomBike
        equipment_data = {'equipment': equipment_label}
        response = self.client.post(f'/api/manager/v1/bikes/{self.boomBike.pk}/equipment', equipment_data,
                                    format='multipart')

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the boomBike instance from the database and check if the equipment with the specified label exists in the bike's equipment list
        self.boomBike.refresh_from_db()
        self.assertTrue(self.boomBike.equipment.filter(equipment=equipment_label).exists())

    def test_add_equipment_to_bike_wrong_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        equipment_label = 'Lock And Key'

        equipment_data = {'equipment': equipment_label}
        response = self.client.post(f'/api/manager/v1/bikes/{self.otherBike.pk}/equipment', equipment_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.otherBike.refresh_from_db()
        self.assertFalse(self.otherBike.equipment.filter(equipment=equipment_label).exists())


class SelectBikeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a bike associated with the store
        self.boomBike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')
        self.niceBike = Bike.objects.create(store=self.store, name='NiceBike', description='NonExplosive')

        # Create a bike associated with store 2
        self.otherBike = Bike.objects.create(store=self.store2, name='MeanBike', description='Mean')

    def test_get_selected_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f'/api/manager/v1/bikes/{self.boomBike.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'name': 'BoomBike',
            'description': 'Explodiert',
        }
        self.assertEqual(expected_data['name'], response.data['name'])
        self.assertEqual(expected_data['description'], response.data['description'])

    def test_get_selected_bike_from_wrong_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)

        response = self.client.get(f'/api/manager/v1/bikes/{self.boomBike.pk}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertNotEqual(response.data, {'name': 'BoomBike', 'description': 'Explodiert'})


class UpdateBikeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a bike associated with the store
        self.boomBike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')
        self.niceBike = Bike.objects.create(store=self.store, name='NiceBike', description='NonExplosive')

        # Create a bike associated with store 2
        self.otherBike = Bike.objects.create(store=self.store2, name='MeanBike', description='Mean')
        self.updated_data = {
            'name': 'BoomBoomBike',
            'description': 'Explodiert weniger',
        }
        self.updated_data2 = {
            'name': ' ',
            'description': ' ',
        }
        self.updated_data3 = {
            'name': 'BoomBike',
            'description': 'Explodiert',
        }

    def test_update_selected_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.patch(f'/api/manager/v1/bikes/{self.boomBike.pk}/update', self.updated_data,
                                     format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.boomBike.refresh_from_db()
        self.assertEqual(self.boomBike.name, self.updated_data['name'])
        self.assertEqual(self.boomBike.description, self.updated_data['description'])

    def test_update_selected_bike_no_legal_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.patch(f'/api/manager/v1/bikes/{self.boomBike.pk}/update', self.updated_data2,
                                     format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.boomBike.refresh_from_db()
        self.assertNotEqual(self.boomBike.name, self.updated_data2['name'])
        self.assertNotEqual(self.boomBike.description, self.updated_data2['description'])
        self.assertEqual(self.boomBike.name, 'BoomBike')
        self.assertEqual(self.boomBike.description, 'Explodiert')

    def test_update_selected_bike_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.patch(f'/api/manager/v1/bikes/{self.otherBike.pk}/update', self.updated_data3,
                                     format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.otherBike.refresh_from_db()
        self.assertNotEqual(self.otherBike.name, self.boomBike.name)
        self.assertNotEqual(self.otherBike.description, self.boomBike.description)


class GetAvailabilityOfSelectedBikeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage', '2023-10-01', '2023-10-02')
        initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23', '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage', '2023-10-01', '2023-10-02')
        initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23', '2023-09-24')

    def test_get_availability_of_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f'/api/manager/v1/bikes/{self.boomBike.pk}/availability', format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Iterate through the availabilities stored in response and check if they all belong to boomBike
        for i in range(len(response.data)):
            availability = response.data[i]
            self.assertEqual(availability['bike'], self.boomBike.pk)
        # Make sure that the amount of availabilities in the response data is the same as the amount of availabilites in the database that belong to boomBike
        self.assertEqual(len(response.data), Availability.objects.filter(bike=self.boomBike).count())

    def test_get_availability_of_bike_does_not_belong(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'/api/manager/v1/bikes/{self.smolBebi.pk}/availability', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBookingsOfStore(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage', '2023-10-01', '2023-10-02')
        initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23', '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage', '2023-10-01', '2023-10-02')
        initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23', '2023-09-24')

    def get_bookings_of_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get('/api/manager/v1/bookings', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(len(response.data)):
            booking = response.data[i]
            self.assertEqual(booking['bike'], self.boomBike.pk)

        # Make sure that the amount of availabilities in the response data is the same as the amount of availabilites in the database that belong to boomBike
        self.assertEqual(len(response.data), Booking.objects.filter(bike=self.boomBike).count())


class GetSelectedBookingOfStoreTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        self.booking_of_Boom1 = initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Boom2 = initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23',
                                                                     '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        self.booking_of_Bebi1 = initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Bebi2 = initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23',
                                                                     '2023-09-24')

    def test_get_selected_booking_of_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f'/api/manager/v1/bookings/{self.booking_of_Boom1.pk}', format='json')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        booking = Booking.objects.get(pk=self.booking_of_Boom1.pk)
        self.assertEqual(response_data.get('preferred_username'), booking.user.preferred_username)
        booking_status = response_data.get("booking_status", [])
        booking_status_label = [status.get("booking_status") for status in booking_status]
        for status in booking_status:
            self.assertIn(status.get("booking_status"), booking_status_label)
        equipment = response_data.get("equipment", [])
        equipment_strings = [value.get("equipment") for value in equipment]
        for value in equipment:
            self.assertIn(value.get("equipment"), equipment_strings)
        self.assertEqual(datetime.strptime(response_data.get("begin"), "%Y-%m-%d").date(), booking.begin)
        self.assertEqual(datetime.strptime(response_data.get("end"), "%Y-%m-%d").date(), booking.end)
        self.assertEqual(response_data.get('comment'), booking.comment)
        self.assertEqual(response_data.get('bike'), booking.bike.pk)

    def test_get_selected_booking_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get(f'/api/manager/v1/bookings/{self.booking_of_Bebi1.pk}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBookingByQRTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        self.booking_of_Boom1 = initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Boom2 = initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23',
                                                                     '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        self.booking_of_Bebi1 = initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Bebi2 = initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23',
                                                                     '2023-09-24')

    def test_find_booking_by_qr_string(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Boom1.pk)
        response = self.client.get(f'/api/manager/v1/bookings/by/{booking.string}', format='json')
       # self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data.get('id'), booking.pk)
        self.assertEqual(response_data.get('preferred_username'), booking.user.preferred_username)
        self.assertEqual(response_data.get('assurance_lvl'), booking.user.assurance_lvl)
        self.assertEqual(response_data.get('bike'), booking.bike.pk)
        self.assertEqual(datetime.strptime(response_data.get("begin"), "%Y-%m-%d").date(), booking.begin)
        self.assertEqual(datetime.strptime(response_data.get("end"), "%Y-%m-%d").date(), booking.end)
        equipment = response_data.get("equipment", [])
        equipment_strings = [value.get("equipment") for value in equipment]
        for value in equipment:
            self.assertIn(value.get("equipment"), equipment_strings)

        booking_status = response_data.get("booking_status", [])
        booking_status_labels = ['Internal usage', 'Booked']
        user_status = response_data.get("user_status", [])
        self.assertIsInstance(user_status, list)
        user_status_strings = [status.user_status for status in booking.user.user_status.all()]
        for status in user_status:
            self.assertIn(status.get("user_status"), user_status_strings)



    def test_find_booking_by_qr_string_wrong_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Bebi1.pk)
        response = self.client.get(f'/api/manager/v1/bookings/by/{booking.string}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PatchUpdateCommentTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        self.booking_of_Boom1 = initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Boom2 = initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23',
                                                                     '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        self.booking_of_Bebi1 = initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Bebi2 = initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23',
                                                                     '2023-09-24')

    def test_update_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Boom1.pk)
        new_comment_data = {
            'comment': 'Hat Massenkarambolage verursacht'
        }
        response = self.client.patch(f'/api/manager/v1/bookings/{booking.pk}/comment', new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        other_booking = Booking.objects.get(pk=self.booking_of_Boom2.pk)
        self.assertEqual(booking.comment, new_comment_data['comment'])
        self.assertNotEqual(other_booking.comment, new_comment_data['comment'])

    def test_update_comment_of_booking_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Bebi1.pk)
        new_comment_data = {
            'comment': 'Hat Massenkarambolage verursacht'
        }
        response = self.client.patch(f'/api/manager/v1/bookings/{booking.pk}/comment', new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        booking.refresh_from_db()
        other_booking = Booking.objects.get(pk=self.booking_of_Bebi2.pk)
        self.assertNotEqual(booking.comment, new_comment_data['comment'])
        self.assertNotEqual(other_booking.comment, new_comment_data['comment'])


class PostReportCommentToAdmin(BaseTestCase):
    def setUp(self):
        super().setUp()
        # initialize bike and bookings for store of user
        bike_data = {
            'name': ['BoomBike'],
            'description': ['Explodiert'],
        }
        self.boomBike = initialize_bike_of_store(self.store, bike_data)
        self.booking_of_Boom1 = initialize_booking_of_bike_with_flag(self.user, self.boomBike, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Boom2 = initialize_booking_of_bike_with_flag(self.user3, self.boomBike, 'Booked', '2023-09-23',
                                                                     '2023-09-24')
        # initialize bike and bookings for store2
        bike_data2 = {
            'name': ['SmolBebi'],
            'description': ['Smol'],
        }
        self.smolBebi = initialize_bike_of_store(self.store2, bike_data2)
        self.booking_of_Bebi1 = initialize_booking_of_bike_with_flag(self.user2, self.smolBebi, 'Internal usage',
                                                                     '2023-10-01', '2023-10-02')
        self.booking_of_Bebi2 = initialize_booking_of_bike_with_flag(self.user, self.smolBebi, 'Booked', '2023-09-23',
                                                                     '2023-09-24')

    def test_post_comment_to_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Boom1.pk)
        user = booking.user
        booking.comment = "Comment"
        booking.save()
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}/comment/report', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.user_status.all().filter(user_status='Reminded').exists())

    def test_post_comment_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        booking = Booking.objects.get(pk=self.booking_of_Bebi1.pk)
        user = booking.user
        booking.comment = "Comment"
        booking.save()
        response = self.client.post(f'/api/manager/v1/bookings/{booking.pk}/comment/report', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(user.user_status.all().filter(user_status='Reminded').exists())


class ConfirmBikeHandOutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and login User and manager
        self.user, self.user_token = initialize_user_with_token(self.client, user_data, login_data)
        self.manager, self.manager_token = initialize_user_with_token(self.client, manager_data_1, manager_login_data_1)
        # initialize store
        self.store = initialize_store(store_data1)
        # initialize bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        # enroll and verify manager
        add_verified_flag_to_user(self.manager)
        add_store_manager_flag_to_user(self.manager, self.store)
        # verify user
        add_verified_flag_to_user(self.user)
        # make booking
        self.booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                            booking_data['end'])
        self.confirm_bike_hand_out_url = f'/api/manager/v1/bookings/{self.booking.pk}/hand-out'

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_confirm_bike_handout_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post(self.confirm_bike_hand_out_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Picked up').booking_status)

    def test_confirm_bike_handout_without_permission(self):
        # user tries
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.post(self.confirm_bike_hand_out_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_bike_handout_with_wrong_token(self):
        # without token
        self.client.credentials()
        response = self.client.post(self.confirm_bike_hand_out_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # with wrong token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.post(self.confirm_bike_hand_out_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_confirm_bike_handout_from_other_store(self):
        # register new store
        store2 = initialize_store(store_data2)
        # register new manager
        manager2, manager_token_2 = initialize_user_with_token(self.client, manager_data_2, manager_login_data_2)
        add_verified_flag_to_user(manager2)
        add_store_manager_flag_to_user(manager2, store2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + manager_token_2)
        response = self.client.post(self.confirm_bike_hand_out_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_confirm_bike_handout_of_cancelled_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Cancelled', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/hand-out')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)

    def test_confirm_bike_handout_of_returned_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/hand-out')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Returned').booking_status)

    def test_confirm_bike_handout_of_internal_usage(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Internal usage', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/hand-out')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(booking2.booking_status.all()[1].booking_status,
                         Booking_Status.objects.get(booking_status='Picked up').booking_status)

    def test_confirm_bike_handout_of_picked_up_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/hand-out')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Picked up').booking_status)

    def test_confirm_bike_handout_with_invalid_booking_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(int(self.booking.pk) + 1) + '/hand-out')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ConfirmBikeReturnTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and login User and manager
        self.user, self.user_token = initialize_user_with_token(self.client, user_data, login_data)
        self.manager, self.manager_token = initialize_user_with_token(self.client, manager_data_1, manager_login_data_1)
        # initialize store
        self.store = initialize_store(store_data1)
        # initialize bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        # enroll and verify manager
        add_verified_flag_to_user(self.manager)
        add_store_manager_flag_to_user(self.manager, self.store)
        # verify user
        add_verified_flag_to_user(self.user)
        # make booking
        self.booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data['begin'],
                                                            booking_data['end'])
        self.confirm_bike_return_url = f'/api/manager/v1/bookings/{self.booking.pk}/return'

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_confirm_bike_return_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post(self.confirm_bike_return_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Returned').booking_status)

    def test_confirm_bike_return_without_permission(self):
        # user tries
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.post(self.confirm_bike_return_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_bike_return_with_wrong_token(self):
        # without token
        self.client.credentials()
        response = self.client.post(self.confirm_bike_return_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # with wrong token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.post(self.confirm_bike_return_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_confirm_bike_return_from_other_store(self):
        # register new store
        store2 = initialize_store(store_data2)
        # register new manager
        manager2, manager_token_2 = initialize_user_with_token(self.client, manager_data_2, manager_login_data_2)
        add_verified_flag_to_user(manager2)
        add_store_manager_flag_to_user(manager2, store2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + manager_token_2)
        response = self.client.post(self.confirm_bike_return_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_confirm_bike_return_of_cancelled_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Cancelled', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/return')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)

    def test_confirm_bike_return_of_returned_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/return')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Returned').booking_status)

    def test_confirm_bike_return_of_internal_usage(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data_2['begin'],
                                                        booking_data_2['end'])
        booking2.booking_status.add(Booking_Status.objects.filter(booking_status='Internal usage')[0].pk)
        booking2.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/return')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(booking2.booking_status.all()[1].booking_status,
                         Booking_Status.objects.get(booking_status='Returned').booking_status)

    def test_confirm_bike_return_of_booked_booking(self):
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data_2['begin'],
                                                        booking_data_2['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(booking2.pk) + '/return')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Booked').booking_status)

    def test_confirm_bike_return_with_invalid_booking_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/' + str(int(self.booking.pk) + 1) + '/return')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetLocalDataOfUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and login User and manager
        self.user, self.user_token = initialize_user_with_token(self.client, user_data, login_data)
        self.manager, self.manager_token = initialize_user_with_token(self.client, manager_data_1, manager_login_data_1)
        # initialize store
        self.store = initialize_store(store_data1)
        # initialize bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        # enroll and verify manager
        add_verified_flag_to_user(self.manager)
        add_store_manager_flag_to_user(self.manager, self.store)
        # verify user
        add_verified_flag_to_user(self.user)
        # make booking
        self.booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                            booking_data['end'])
        initializer_local_data_of_user(self.user, local_user_data)
        self.get_user_data_of_booking1 = f'/api/manager/v1/bookings/{self.booking.pk}/user-info'

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_get_user_data_of_booking_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.get(self.get_user_data_of_booking1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['first_name'], local_user_data['first_name'])
        self.assertEqual(response_data['last_name'], local_user_data['last_name'])
        self.assertEqual(response_data['address'], local_user_data['address'])
        self.assertEqual(response_data['id_number'], local_user_data['id_number'])
        self.assertNotEqual(response_data['date_of_verification'], None)

    def test_get_user_data_without_permission(self):
        # without token
        self.client.credentials()
        response = self.client.get(self.get_user_data_of_booking1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # with user token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.get(self.get_user_data_of_booking1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.get(self.get_user_data_of_booking1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_data_of_booking_from_other_store(self):
        store2 = initialize_store(store_data2)
        manager2, token_manager_2 = initialize_user_with_token(self.client, manager_data_2, manager_login_data_2)
        add_store_manager_flag_to_user(manager2, store2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_manager_2)
        response = self.client.get(self.get_user_data_of_booking1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_data_with_invalid_booking_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.get('/api/manager/v1/bookings/-1/user-info')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateLocalDataOfUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and login User and manager
        self.user, self.user_token = initialize_user_with_token(self.client, user_data, login_data)
        self.manager, self.manager_token = initialize_user_with_token(self.client, manager_data_1, manager_login_data_1)
        # initialize store
        self.store = initialize_store(store_data1)
        # initialize bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        # enroll and verify manager
        add_verified_flag_to_user(self.manager)
        add_store_manager_flag_to_user(self.manager, self.store)
        # verify user
        add_verified_flag_to_user(self.user)
        # make booking
        self.booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                            booking_data['end'])
        self.create_local_user_data = f'/api/manager/v1/bookings/{self.booking.pk}/user-info'

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_create_local_user_data_that_is_already_created(self):
        initializer_local_data_of_user(self.user, local_user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post(self.create_local_user_data, local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_local_user_data_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post(self.create_local_user_data, local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['first_name'], local_user_data['first_name'])
        self.assertEqual(response_data['last_name'], local_user_data['last_name'])
        self.assertEqual(response_data['address'], local_user_data['address'])
        self.assertEqual(response_data['id_number'], local_user_data['id_number'])
        self.assertNotEqual(response_data['date_of_verification'], None)

    def test_create_local_user_data_of_invalid_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.post('/api/manager/v1/bookings/-1/user-info', local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_data_of_booking_from_other_store(self):
        store2 = initialize_store(store_data2)
        manager2, token_manager_2 = initialize_user_with_token(self.client, manager_data_2, manager_login_data_2)
        add_store_manager_flag_to_user(manager2, store2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_manager_2)
        response = self.client.post(self.create_local_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_data_of_booking_without_permission(self):
        # try to create as user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.post(self.create_local_user_data, local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # try without token
        self.client.credentials()
        response = self.client.post(self.create_local_user_data, local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # try with invalid
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.post(self.create_local_user_data, local_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateLocalDataOfUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and login User and manager
        self.user, self.user_token = initialize_user_with_token(self.client, user_data, login_data)
        self.manager, self.manager_token = initialize_user_with_token(self.client, manager_data_1, manager_login_data_1)
        # initialize store
        self.store = initialize_store(store_data1)
        # initialize bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        # enroll and verify manager
        add_verified_flag_to_user(self.manager)
        add_store_manager_flag_to_user(self.manager, self.store)
        # verify user
        add_verified_flag_to_user(self.user)
        # make booking
        self.booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                            booking_data['end'])
        self.update_local_user_data = f'/api/manager/v1/bookings/{self.booking.pk}/user-info'
        self.changed_user_data = {
            "first_name": "Ursula",
            "last_name": "Steckerleiste",
            "address": "PSEstr. 1, 67890 PSEhausen",
            "id_number": "456"
        }

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_update_local_user_data_that_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.patch(self.update_local_user_data, self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_local_user_data_valid(self):
        initializer_local_data_of_user(self.user, local_user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.patch(self.update_local_user_data, self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['first_name'], self.changed_user_data['first_name'])
        self.assertEqual(response_data['last_name'], self.changed_user_data['last_name'])
        self.assertEqual(response_data['address'], self.changed_user_data['address'])
        self.assertEqual(response_data['id_number'], self.changed_user_data['id_number'])

    def test_update_local_user_data_of_invalid_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token)
        response = self.client.patch('/api/manager/v1/bookings/-1/user-info', self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_data_of_booking_from_other_store(self):
        store2 = initialize_store(store_data2)
        manager2, token_manager_2 = initialize_user_with_token(self.client, manager_data_2, manager_login_data_2)
        add_store_manager_flag_to_user(manager2, store2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_manager_2)
        response = self.client.patch(self.update_local_user_data, self.changed_user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_data_of_booking_without_permission(self):
        # try to update as user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = self.client.patch(self.update_local_user_data, self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # try without token
        self.client.credentials()
        response = self.client.patch(self.update_local_user_data, self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # try with invalid
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.patch(self.update_local_user_data, self.changed_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)