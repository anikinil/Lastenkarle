import os
from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory
from db_model.models import User_Status, User, Equipment, Availability_Status, Booking_Status, Booking, Store, Bike, \
    Availability, UserManager, generate_random_string
from api.algorithm import split_availabilities_algorithm
from api.user.v1.views import RegistrateUser
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json
from unittest import skip
from django.core import serializers
import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, time, datetime
from send_mail.views import format_opening_hours
from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST, BASE_DIR
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data

from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

image_path = os.path.join(BASE_DIR, 'media/test_image/', 'image.jpg')

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


def initialize_user_with_token(client, user_data, login_data):
    user = User.objects.create_user(**user_data)
    response = client.post("/api/user/v1/login", login_data)
    response_data = json.loads(response.content.decode('utf-8'))
    token_user = response_data.get('token', None)
    return user, token_user


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

