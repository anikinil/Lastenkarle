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
    'password': 'password',
}

user_data_2 = {
    'username': 'Wilderich',
    'password': 'password',
    'contact_data': 'the_voices_in_my_head@gmx.de',
    'year_of_birth': '1901'
}
login_data_2 = {
    'username': 'Wilderich',
    'password': 'password',
}
store_data = {
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


class MigrationTest(TestCase):

    def test_migrations(self):
        equipment = Equipment.objects.all()
        equipment_json = serializers.serialize('json', equipment)
        search_terms = ['Lock And Key', 'Child Safety Seat And Seatbelt', 'Tarp', 'Battery', 'Charger']
        self.find_and_test_terms_in_json(search_terms, equipment_json, 'equipment')

        availabilities_status = Availability_Status.objects.all()
        availabilities_status_json = serializers.serialize('json', availabilities_status)
        search_terms = ['Booked', 'Available']
        self.find_and_test_terms_in_json(search_terms, availabilities_status_json, 'availability_status')

        booking_status = Booking_Status.objects.all()
        booking_status_json = serializers.serialize('json', booking_status)
        search_terms = ['Booked', 'Internal usage', 'Picked up', 'Cancelled', 'Returned']
        self.find_and_test_terms_in_json(search_terms, booking_status_json, 'booking_status')

        user_status = User_Status.objects.all()
        user_status_json = serializers.serialize('json', user_status)
        search_terms = ['Verified', 'Deleted', 'Reminded', 'Administrator', 'Banned', 'Customer']
        self.find_and_test_terms_in_json(search_terms, user_status_json, 'user_status')

    def find_and_test_terms_in_json(self, search_terms, search_json, field_name):
        list = json.loads(search_json)
        found_equipment = [item['fields'][field_name] for item in list]
        for term in search_terms:
            self.assertIn(term, found_equipment)


class ImageExistsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image_url = "https://transport.data.kit.edu/static/media/logo.2f51c6d45972d24d4330.png"

    def test_image_exists(self):
        # Send a GET request to the specified image URL
        response = requests.get(self.image_url)
        # Check if the request was successful (Status code 200)
        self.assertEqual(response.status_code, 200)
        # Check if the content is not empty
        self.assertNotEqual(response.content, b'')
        # Check if the content type of the image is correct (starts with 'image/')
        self.assertTrue(response.headers['Content-Type'] == 'image/png')


class RegistrateUserTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.registrate_url = '/api/user/v1/register'

    def test_valid_user_registration(self):
        request = self.factory.post(self.registrate_url, user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if User is created in Database
        user_exists = User.objects.filter(username=user_data['username']).exists()
        self.assertTrue(user_exists)
        # Check if User Contact data is written into database correctly
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.contact_data, user_data['contact_data'])
        # Check the number of emails, that have been sent
        self.assertEqual(1, len(mail.outbox))
        # Check if subject and body are the expected ones
        first_message = mail.outbox[0]
        subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
        self.assertEqual(first_message.subject, subject)
        registration_link = CANONICAL_HOST + "/email-verification/" + str(user.pk) + "/" + user.verification_string
        html_message = render_to_string("email_templates/UserRegisteredConfirmation.html",
                                        {'username': user.preferred_username,
                                         'lastenkarle_logo_url': lastenkarle_logo_url,
                                         'registration_link': registration_link})
        self.assertEqual(first_message.body, html_message)

    def test_register_with_missing_credentials(self):
        # missing credentials
        invalid_user_data = {
            'username': 'testuser',
        }
        request = self.factory.post(self.registrate_url, invalid_user_data, format='json')
        response = RegistrateUser.as_view()(request)
        # check Status Code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if user is added to database
        user_count = User.objects.filter(username=invalid_user_data['username']).count()
        self.assertEqual(user_count, 0)
        # Check that no emails are sent
        self.assertEqual(0, len(mail.outbox))

    def test_register_same_user_for_the_second_time(self):
        request = self.factory.post(self.registrate_url, user_data, format='json')
        response = RegistrateUser.as_view()(request)
        user = User.objects.get(username=user_data['username'])
        # Try to register same user for the second time
        request = self.factory.post(self.registrate_url, user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if User is doubled in database
        user_count = User.objects.filter(username=user_data['username']).count()
        self.assertEqual(user_count, 1)
        # Check that no emails are sent
        self.assertEqual(1, len(mail.outbox))

    def test_register_user_with_same_username_but_different_contact_data(self):
        request = self.factory.post(self.registrate_url, user_data, format='json')
        response = RegistrateUser.as_view()(request)
        # Try to register user with same username but different contact data
        user_data_with_same_username = {
            'username': 'Wildegard',
            'password': 'password',
            'contact_data': 'pse_email@gmx.de',
            'year_of_birth': '1901'
        }
        request = self.factory.post(self.registrate_url, user_data_with_same_username, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if User is doubled in database
        user_count = User.objects.filter(username=user_data_with_same_username['username']).count()
        self.assertEqual(user_count, 1)
        # Check that no emails are sent
        self.assertEqual(1, len(mail.outbox))

    def test_register_user_with_different_username_but_same_contact_data(self):
        request = self.factory.post(self.registrate_url, user_data, format='json')
        response = RegistrateUser.as_view()(request)
        # Try to register user with different username but same contact data
        user_data_with_same_contact_data = {
            'username': 'Wilderich',
            'password': 'password',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        request = self.factory.post(self.registrate_url, user_data_with_same_contact_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if User is doubled in database
        user_count = User.objects.filter(contact_data=user_data_with_same_contact_data['contact_data']).count()
        self.assertEqual(user_count, 1)
        # Check that no emails are sent
        self.assertEqual(1, len(mail.outbox))


class LoginTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(**user_data)
        self.login_url = '/api/user/v1/login'

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_user(self):
        # Check what happens when logging in nonexistent user
        invalid_user_data = {
            'username': 'nonexistentuser',
            'password': 'invalidpassword'
        }
        response = self.client.post(self.login_url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_login_missing_credentials(self):
        # Check what happens if logging in with empty credentials
        response = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)

    def test_login_with_inactive_user(self):
        # deactivate the user
        self.user = User.objects.get(username=user_data['username'])
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.login_url, login_data, format='json')
        # check that inactive user is not logged in
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)

    def test_login_with_wrong_password(self):
        wrong_password_data = {
            'username': 'Wildegard',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, wrong_password_data, format='json')
        # check that existing user with wrong password is not logged in
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response_data['non_field_errors'], ['Wrong credentials'])

    def test_login_with_different_case_username(self):
        # test if user is logged in when username is written with different case
        dif_case_login_data = {
            'username': 'wildeGard',
            'password': 'password'
        }
        response = self.client.post(self.login_url, dif_case_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)

    def test_login_with_missing_username(self):
        missing_username_data = {
            'password': 'password'
        }
        response = self.client.post(self.login_url, missing_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)

    def test_login_with_blank_username(self):
        blank_username_data = {
            'username': '',
            'password': 'password'
        }
        response = self.client.post(self.login_url, blank_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('username', response.data)
        self.assertEqual(response_data['username'], ['This field may not be blank.'])

    def test_login_with_blank_password(self):
        blank_password_data = {
            'username': 'Wildegard',
            'password': ''
        }
        response = self.client.post(self.login_url, blank_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('password', response.data)
        self.assertEqual(response_data['password'], ['This field may not be blank.'])

    def test_login_with_trailing_whitespace_username(self):
        trailing_whitespace_username_data = {
            'username': 'Wildegard ',
            'password': 'password'
        }
        response = self.client.post(self.login_url, trailing_whitespace_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_trailing_whitespace_password(self):
        trailing_whitespace_password_data = {
            'username': 'Wildegard',
            'password': 'password '
        }
        response = self.client.post(self.login_url, trailing_whitespace_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response_data['non_field_errors'], ['Wrong credentials'])


class LogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.logout_url = "/api/user/v1/logout"

    def test_logout_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # check if user is logged out
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # check if user is logged out
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_invalid_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # check if user is logged out
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutAllTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create User
        self.user = User.objects.create_user(**user_data)
        # Login User 3 times and store tokens
        self.tokens = []
        for _ in range(3):
            response = self.client.post("/api/user/v1/login", login_data)
            response_data = json.loads(response.content.decode('utf-8'))
            token = response_data.get('token', None)
            self.tokens.append(token)
        self.logout_all_url = "/api/user/v1/logout-all"

    def test_logout_all_sessions_with_valid_tokens(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokens[0])
        response = self.client.post(self.logout_all_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # check if user is logged out
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # check if all token are invalid now
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokens[1])
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokens[2])
        response = self.client.get('/api/user/v1/user/data')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_all_without_token(self):
        # Ensure the user is not authenticated
        self.client.credentials()
        response = self.client.post(self.logout_all_url)
        # Check if the status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_all_with_invalid_token(self):
        # Use an invalid token (e.g., a wrong string) for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        # Attempt to log out
        response = self.client.post(self.logout_all_url)
        # Check if the status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.get_user_data_url = "/api/user/v1/user/data"

    def test_get_user_data_valid(self):
        # set token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # try to get user data
        response = self.client.get(self.get_user_data_url)
        # check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['username'], self.user.username)
        self.assertEqual(response_data['contact_data'], self.user.contact_data)
        self.assertNotIn('password', response_data)

    def test_get_user_data_without_token(self):
        # Unauthenticated request, remove the token
        self.client.credentials()
        # Try to get user data
        response = self.client.get(self.get_user_data_url)
        # Check the status code, it should be 401 (UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_data_with_invalid_token(self):
        # Set a token, but it should be invalid
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        # Try to get user data
        response = self.client.get(self.get_user_data_url)
        # Check the status code, it should be 401 (UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.update_user_data_url = "/api/user/v1/user/update"

    def test_update_user_data_with_valid_data(self):
        changed_user_data = {
            "username": "Wilderich",
            "contact_data": "pse_email@gmx.de",
            "password": "password2"
        }
        changed_login_data = {
            "username": "Wilderich",
            "password": "password2"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['username'], changed_user_data['username'])
        self.assertEqual(response_data['contact_data'], changed_user_data['contact_data'])
        # try to login with new login data
        response = self.client.post('/api/user/v1/login', changed_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get user
        user = User.objects.get(username=changed_user_data['username'])
        # check if preferred_username changed
        self.assertEqual(user.preferred_username, changed_user_data['username'])
        # Check the number of emails, that have been sent
        self.assertEqual(1, len(mail.outbox))
        # Check if subject and body are the expected ones
        first_message = mail.outbox[0]
        subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
        self.assertEqual(first_message.subject, subject)
        verification_link = CANONICAL_HOST + "/email-verification/" + str(user.pk) + "/" + user.verification_string
        html_message = render_to_string("email_templates/EmailChangedTemplate.html",
                                        {'username': user.preferred_username,
                                         'lastenkarle_logo_url': lastenkarle_logo_url,
                                         'verification_link': verification_link})
        self.assertEqual(first_message.body, html_message)

    def test_update_username(self):
        user_before_change = User.objects.get(username=user_data['username'])
        reg1 = user_before_change.verification_string
        changed_user_data = {
            "username": "Wilderich"
        }
        changed_login_data = {
            "username": "Wilderich",
            "password": "password"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_after_change = User.objects.get(contact_data=user_before_change.contact_data)
        reg2 = user_after_change.verification_string
        self.assertEqual(reg1, reg2)
        # check if username is changed
        self.assertEqual(changed_login_data['username'], user_after_change.username)

    def test_update_user_data_with_empty_data(self):
        changed_user_data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['username'], user_data['username'])
        self.assertEqual(response_data['contact_data'], user_data['contact_data'])
        # try to log in
        response = self.client.post('/api/user/v1/login', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of emails, that have been sent
        self.assertEqual(0, len(mail.outbox))

    def test_update_user_data_with_invalid_data(self):
        changed_user_data = {
            "username": "",
            "contact_data": "",
            "password": ""
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertNotEqual(response_data['username'], changed_user_data['username'])
        self.assertNotEqual(response_data['contact_data'], changed_user_data['contact_data'])
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.contact_data, user_data['contact_data'])
        # try to log in
        response = self.client.post('/api/user/v1/login', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of emails, that have been sent
        self.assertEqual(0, len(mail.outbox))

    def test_update_user_data_with_username_that_already_exists(self):
        second_user_data = {
            "username": "Gurke",
            "contact_data": "pse_email@gmx.de",
            "password": "password2"
        }
        changed_user_data = {
            "username": "Gurke"
        }
        changed_login_data = {
            "username": "Gurke",
            "password": "password"
        }
        # create second user
        User.objects.create_user(**second_user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertNotEqual(response_data['username'], changed_user_data['username'])
        user = User.objects.get(contact_data=user_data['contact_data'])
        self.assertEqual(user.username, user_data['username'])
        # try to log in with wrong credentials
        response = self.client.post('/api/user/v1/login', changed_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # try to log in with right credentials
        response = self.client.post('/api/user/v1/login', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of emails, that have been sent
        self.assertEqual(0, len(mail.outbox))

    def test_update_user_data_with_contact_data_that_already_exists(self):
        second_user_data = {
            "username": "Gurke",
            "contact_data": "pse_email@gmx.de",
            "password": "password2"
        }
        changed_user_data = {
            "contact_data": "pse_email@gmx.de"
        }
        User.objects.create_user(**second_user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # Try to update user data
        response = self.client.patch(self.update_user_data_url, changed_user_data, format='json')
        # Check the status code, it should be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertNotEqual(response_data['contact_data'], changed_user_data['contact_data'])
        user = User.objects.get(username=user_data['username'])
        self.assertEqual(user.username, user_data['username'])
        # Check the number of emails, that have been sent
        self.assertEqual(0, len(mail.outbox))


class DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.delete_account_url = "/api/user/v1/user/delete-account"
        self.store = initialize_store(store_data)
        self.bike = initialize_bike_of_store(self.store, bike1_data)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_delete_account_valid(self):
        user_id = self.user.pk
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user_id)
        # check if all data is deleted
        self.assertEqual(user.username, None)
        self.assertEqual(user.contact_data, None)
        self.assertEqual(user.year_of_birth, None)
        self.assertEqual(user.assurance_lvl, None)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.preferred_username, None)
        self.assertEqual(user.password, None)
        self.assertEqual(user.verification_string, None)

    def test_delete_account_without_authentication(self):
        # Test account deletion without authentication
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account_twice(self):
        # Test attempting to delete an account twice
        user_id = self.user.pk
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # First deletion
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=user_id)
        self.assertEqual(user.is_active, False)
        # Attempt a second deletion
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_again_after_deleting_without_verification(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.delete(self.delete_account_url)
        self.client.credentials()
        response = self.client.post("/api/user/v1/register", user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_again_after_deleting_with_verification(self):
        user_id = self.user.pk
        # verify user
        response = self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.delete(self.delete_account_url)
        self.client.credentials()
        response = self.client.post("/api/user/v1/register", user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_account_with_inactive_booking(self):
        user_id = self.user.pk
        # verify user to make booking
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        booking_data = {
            "begin": "2023-10-02",
            "end": "2023-10-03",
            "equipment": []
        }
        booking_data_2 = {
            "begin": "2023-10-04",
            "end": "2023-10-05",
            "equipment": []
        }
        booking_data_3 = {
            "begin": "2023-10-09",
            "end": "2023-10-10",
            "equipment": []
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # make bookings
        booking1 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                        booking_data['end'])
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data_2['begin'],
                                                        booking_data_2['end'])
        booking3 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Cancelled', booking_data_3['begin'],
                                                        booking_data_3['end'])

        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deleted_user = User.objects.get(pk=user_id)
        # check if booking of deleted user is cancelled
        self.assertEqual(booking1.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)
        self.assertEqual(booking2.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Returned').booking_status)
        self.assertEqual(booking3.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)
        self.assertTrue(booking1.pk < booking2.pk)
        self.assertTrue(booking2.pk < booking3.pk)

    def test_delete_account_with_active_booking(self):
        # verify user to make booking
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # make booking
        initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data['begin'],
                                             booking_data['end'])
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        expected_json = ['Account deletion not possible whilst having picked up a bike.']
        self.assertEqual(response_data, expected_json)

    def test_delete_the_only_admin(self):
        admin_login_data = {
            'username': 'Caro',
            'password': 'password'
        }
        self.admin = User.objects.create_superuser(username="Caro", password="password",
                                                   contact_data="pse_email@gmx.de")
        admin_status = User_Status.objects.get(user_status="Administrator")
        users_with_admin_status = User.objects.filter(user_status=admin_status)
        self.assertEqual(len(users_with_admin_status), 1)
        response = self.client.post("/api/user/v1/login", admin_login_data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.admin_token = response_data.get('token', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(response.content.decode('utf-8'))
        expected_json = ['Account deletion not possible as only administrator.']
        self.assertEqual(response_data, expected_json)
        self.assertEqual(self.admin.is_active, True)


class GetAllBookingsOfUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and log in user
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.get_all_bookings_of_user_url = '/api/user/v1/user/bookings'
        # create store
        self.store = initialize_store(store_data)
        # create bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_get_all_bookings_of_user_unverified(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_all_bookings_of_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        empty_set = []
        self.assertEqual(response_data, empty_set)

    def test_get_all_bookings_of_verified_user_without_bookings(self):
        # verify user
        response = self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_all_bookings_of_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        empty_set = []
        self.assertEqual(response_data, empty_set)

    def test_get_all_bookings_of_user_with_made_bookings(self):
        # verify user
        response = self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        # make bookings
        # TODO: Hier noch equipment hinzufügen
        booking1 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                        booking_data['end'])
        booking2 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data_2['begin'],
                                                        booking_data_2['end'])
        booking3 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Cancelled', booking_data_3['begin'],
                                                        booking_data_3['end'])
        booking4 = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data_4['begin'],
                                                        booking_data_4['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_all_bookings_of_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        empty_set = []
        # check if booking 1 is correct
        self.assertEqual(response_data[0]['id'], booking1.pk)
        self.assertEqual(response_data[0]['booking_status'][0]['booking_status'],
                         Booking_Status.objects.get(booking_status='Booked').booking_status)
        self.assertEqual(response_data[0]['equipment'], empty_set)
        self.assertEqual(response_data[0]['begin'], booking_data["begin"])
        self.assertEqual(response_data[0]['end'], booking_data["end"])
        self.assertEqual(response_data[0]['begin'], booking_data["begin"])
        self.assertEqual(response_data[0]['bike'], self.bike.pk)

        # check if booking 2 is correct
        # TODO: Hier equipment wieder einkommentieren
        equipment_list = [{
            'id': Equipment.objects.get(equipment='Tarp').pk,
            'equipment': Equipment.objects.get(equipment='Tarp').equipment
        }, {
            'id': Equipment.objects.get(equipment='Charger').pk,
            'equipment': Equipment.objects.get(equipment='Charger').equipment
        }]
        self.assertEqual(response_data[1]['id'], booking2.pk)
        self.assertEqual(response_data[1]['booking_status'][0]['booking_status'],
                         Booking_Status.objects.get(booking_status='Returned').booking_status)
        # self.assertEqual(response_data[1]['equipment'], equipment_list)
        self.assertEqual(response_data[1]['begin'], booking_data_2["begin"])
        self.assertEqual(response_data[1]['end'], booking_data_2["end"])
        self.assertEqual(response_data[1]['begin'], booking_data_2["begin"])
        self.assertEqual(response_data[1]['bike'], self.bike.pk)

        # check booking 3
        self.assertEqual(response_data[2]['id'], booking3.pk)
        self.assertEqual(response_data[2]['booking_status'][0]['booking_status'],
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)
        self.assertEqual(response_data[2]['equipment'], empty_set)
        self.assertEqual(response_data[2]['begin'], booking_data_3["begin"])
        self.assertEqual(response_data[2]['end'], booking_data_3["end"])
        self.assertEqual(response_data[2]['begin'], booking_data_3["begin"])
        self.assertEqual(response_data[2]['bike'], self.bike.pk)

        # check booking 4
        self.assertEqual(response_data[3]['id'], booking4.pk)
        self.assertEqual(response_data[3]['booking_status'][0]['booking_status'],
                         Booking_Status.objects.get(booking_status='Picked up').booking_status)
        self.assertEqual(response_data[3]['equipment'], empty_set)
        self.assertEqual(response_data[3]['begin'], booking_data_4["begin"])
        self.assertEqual(response_data[3]['end'], booking_data_4["end"])
        self.assertEqual(response_data[3]['begin'], booking_data_4["begin"])
        self.assertEqual(response_data[3]['bike'], self.bike.pk)

    def test_get_all_bookings_of_user_without_token(self):
        self.client.credentials()
        response = self.client.get(self.get_all_bookings_of_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_bookings_of_user_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.get(self.get_all_bookings_of_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingDataTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.get_booking_data_url = '/api/user/v1/user/bookings/'
        # verify user
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.store = initialize_store(store_data)
        # create bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_get_booking_data_valid(self):
        # make booking
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        # get Booking data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/user/v1/user/bookings/' + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        equipment_list = [{
            'id': Equipment.objects.get(equipment='Charger').pk,
            'equipment': Equipment.objects.get(equipment='Charger').equipment
        }]
        # check if booking data is correct
        self.assertEqual(response_data['id'], booking.pk)
        self.assertEqual(response_data['booking_status'][0]['booking_status'],
                         Booking_Status.objects.get(booking_status='Booked').booking_status)
        # TODO: Hier equipment wieder einkommentieren
        # self.assertEqual(response_data['equipment'], equipment_list)
        self.assertEqual(response_data['begin'], booking_data['begin'])
        self.assertEqual(response_data['end'], booking_data['end'])
        self.assertEqual(response_data['bike'], self.bike.pk)

    def test_get_booking_data_without_token(self):
        # make booking
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials()
        # get booking data
        response = self.client.get('/api/user/v1/user/bookings/' + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_booking_data_with_wrong_token(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.get('/api/user/v1/user/bookings/' + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_booking_data_of_other_user(self):
        # make booking
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        user2, token_user_2 = initialize_user_with_token(self.client, user_data_2, login_data_2)
        # try to get user1's booking data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_user_2)
        response = self.client.get('/api/user/v1/user/bookings/' + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_booking_data_with_invalid_id(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.get('/api/user/v1/user/bookings/' + '-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CancelBookingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.cancel_booking_url = '/api/user/v1/user/bookings/'  # + booking_id
        # verify user
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.store = initialize_store(store_data)
        # create bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_cancel_booking_valid(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(booking.booking_status.all().first().booking_status,
                         Booking_Status.objects.get(booking_status='Cancelled').booking_status)

    def test_cancel_picked_up_booking(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Picked up', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_finished_booking(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_of_other_user(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        user2, token2 = initialize_user_with_token(self.client, user_data_2, login_data_2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_booking_with_invalid_token(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Returned', booking_data['begin'],
                                                       booking_data['end'])
        # without token
        self.client.credentials()
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cancel_booking_twice(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Cancelled', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.cancel_booking_url + str(booking.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_that_doesnt_exist(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.cancel_booking_url + '-1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBookedBikeTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # register and log in user
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        # verify user
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.store = initialize_store(store_data)
        # create bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        self.get_booked_bike_url = '/api/user/v1/user/bookings/'  # + booking_id + /bike

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_get_booked_bike_valid(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_booked_bike_url + str(booking.pk) + '/bike')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        empty_set = []
        # check Bike
        self.assertEqual(response_data['id'], self.bike.pk)
        self.assertEqual(response_data['equipment'], empty_set)
        self.assertEqual(response_data['name'], self.bike.name)
        self.assertEqual(response_data['description'], self.bike.description)
        self.assertEqual(response_data['store'], self.bike.store.pk)

    def test_get_booked_bike_with_wrong_token(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        # try to get without token
        self.client.credentials()
        response = self.client.get(self.get_booked_bike_url + str(booking.pk) + '/bike')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # try to get with wrong token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.get(self.get_booked_bike_url + str(booking.pk) + '/bike')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_booked_bike_of_booking_of_other_user(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        # register and log in user 2
        user2, token2 = initialize_user_with_token(self.client, user_data_2, login_data_2)
        # verify user 2
        self.client.post('/api/user/v1/' + str(user2.pk) + '/' + str(user2.verification_string))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
        response = self.client.get(self.get_booked_bike_url + str(booking.pk) + '/bike')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_booked_bike_of_non_existent_booking(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_booked_bike_url + '-1' + '/bike')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBookedBikeOfStoreTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        # verify user
        self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        # create store
        self.store = initialize_store(store_data)
        # create bike
        self.bike = initialize_bike_of_store(self.store, bike1_data)
        self.get_store_of_booked_bike = '/api/user/v1/user/bookings/'  # + booking_id + /bike/store

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_get_booked_bike_of_store_valid(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.get_store_of_booked_bike + str(booking.pk) + '/bike/store')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_booked_bike_of_store_with_invalid_token(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])
        # without token
        self.client.credentials()
        response = self.client.get(self.get_store_of_booked_bike + str(booking.pk) + '/bike/store')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data['detail'], 'Authentication credentials were not provided.')
        # with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.get(self.get_store_of_booked_bike + str(booking.pk) + '/bike/store')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data['detail'], 'Invalid token.')

    def test_get_booked_bike_of_store_of_other_user(self):
        booking = initialize_booking_of_bike_with_flag(self.user, self.bike, 'Booked', booking_data['begin'],
                                                       booking_data['end'])

        self.client.post("/api/user/v1/register", user_data_2)
        response = self.client.post("/api/user/v1/login", login_data_2)
        response_data = json.loads(response.content.decode('utf-8'))
        token2 = response_data.get('token', None)
        user2 = User.objects.get(username=user_data_2['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2)
        response = self.client.get(self.get_store_of_booked_bike + str(booking.pk) + '/bike/store')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data['detail'], 'Not found.')


class VerificationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.token = initialize_user_with_token(self.client, user_data, login_data)
        self.verify_url = '/api/user/v1/'  # + user_id + user_verification_string

    def tearDown(self):
        for bike in Bike.objects.all():
            os.remove(os.path.join(BASE_DIR, 'media/', str(bike.image)))
        super().tearDown()

    def test_verify_user_valid(self):
        response = self.client.post(self.verify_url + str(self.user.pk) + '/' + str(self.user.verification_string))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_after_verification = User.objects.get(username=self.user.username)
        self.assertEqual(user_after_verification.verification_string, None)

    def test_verify_user_with_wrong_id(self):
        response = self.client.post(self.verify_url + '-1' + '/' + str(self.user.verification_string))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_user_with_wrong_verification_code(self):
        wrong_verif_code = 'wrong_verification_code'
        response = self.client.post(self.verify_url + str(self.user.pk) + '/' + wrong_verif_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_other_users_id(self):
        user2, token2 = initialize_user_with_token(self.client, user_data_2, login_data_2)
        response = self.client.post(self.verify_url + str(self.user.pk) + '/' + user2.verification_string)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_other_users_verification_code(self):
        user2, token2 = initialize_user_with_token(self.client, user_data_2, login_data_2)
        response = self.client.post(self.verify_url + str(user2.pk) + '/' + self.user.verification_string)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
