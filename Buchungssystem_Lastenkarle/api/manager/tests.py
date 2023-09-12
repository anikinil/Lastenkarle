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

