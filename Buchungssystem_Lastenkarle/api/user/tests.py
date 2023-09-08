from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory
from db_model.models import User_Status, User, Equipment, Availability_Status, Booking_Status, Booking, Store, Bike, \
    Availability
from api.user.v1.views import RegistrateUser
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json
from unittest import skip
from django.core import serializers
import requests

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data

from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

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
        self.user_data = user_data
        self.registrate_url = '/api/user/v1/register'

    def test_valid_user_registration(self):
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if User is created in Database
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertTrue(user_exists)
        # Check if User Contact data is written into database correctly
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.contact_data, self.user_data['contact_data'])
        # Check the number of emails, that have been sent
        self.assertEqual(1, len(mail.outbox))
        # Check if subject and body are the expected ones
        first_message = mail.outbox[0]
        subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
        self.assertEqual(first_message.subject, subject)
        registration_link = CANONICAL_HOST + "email-verification/" + str(user.pk) + "/" + user.verification_string
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
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
        response = RegistrateUser.as_view()(request)
        user = User.objects.get(username=self.user_data['username'])
        # Try to register same user for the second time
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if User is doubled in database
        user_count = User.objects.filter(username=self.user_data['username']).count()
        self.assertEqual(user_count, 1)
        # Check that no emails are sent
        self.assertEqual(1, len(mail.outbox))

    def test_register_user_with_same_username_but_different_contact_data(self):
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
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
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
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
        self.user_data = user_data
        self.login_data = login_data
        self.user = User.objects.create_user(**self.user_data)
        self.token, _ = AuthToken.objects.create(self.user)
        self.login_url = '/api/user/v1/login'

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, self.login_data, format='json')
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
        self.user = User.objects.get(username=self.user_data['username'])
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.login_url, self.login_data, format='json')
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
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)
        self.assertIn('non_field_errors', response.data)

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
        self.assertIn('username', response.data)

    def test_login_with_blank_password(self):
        blank_password_data = {
            'username': 'Wildegard',
            'password': ''
        }
        response = self.client.post(self.login_url, blank_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

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
        self.assertIn('non_field_errors', response.data)


class LogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = user_data
        self.login_data = login_data
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.login_data)
        # Parse the response content to get the token
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
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
        self.user_data = user_data
        self.login_data = login_data
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # Login User 3 times and store tokens
        self.tokens = []
        for _ in range(3):
            response = self.client.post("/api/user/v1/login", self.login_data)
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
        self.user_data = user_data
        self.login_data = login_data
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.login_data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
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
        # TODO: sobald API gefixt, diesen Test wieder anschalten
        # self.assertNotIn('password', response_data)

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
        self.user_data = user_data
        self.login_data = login_data
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.login_data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
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
        # try to login with wrong credentials
        response = self.client.post('/api/user/v1/login', changed_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # try to login with right credentials
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
        self.user_data = user_data
        self.login_data = login_data
        # register user
        self.client.post("/api/user/v1/register", self.user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.login_data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
        self.user = User.objects.get(username=user_data['username'])
        self.delete_account_url = "/api/user/v1/user/delete-account"

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

    def test_register_again_after_deleting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.delete(self.delete_account_url)
        response = self.client.post("/api/user/v1/register", self.user_data)
        # weiter

    def test_delete_account_with_inactive_booking(self):
        user_id = self.user.pk
        # verify user to make booking
        response = self.client.post('/api/user/v1/' + str(self.user.pk) + '/' + str(self.user.verification_string))
        store_data = {
            'name': 'Store1',
            'address': 'Storestr. 1',
            'email': 'pse_email@gmx.de',
            'region': 'KA',
            'phone_number': '012345'
        }
        store = Store.objects.create(**store_data)
        store_flag = User_Status.custom_create_store_flags(store)
        store.store_flag = store_flag
        store.save()
        bike_data = {
            'name': 'Bike1',
            'description': 'Es ist schnell'
        }
        bike = Bike.create_bike(store, **bike_data)
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
        # make booking
        self.client.post('/api/booking/v1/bikes/' + str(bike.pk) + '/booking', booking_data, format='json')
        self.client.post('/api/booking/v1/bikes/' + str(bike.pk) + '/booking', booking_data_2, format='json')
        self.client.post('/api/booking/v1/bikes/' + str(bike.pk) + '/booking', booking_data_3, format='json')
        bookings = Booking.objects.filter(user=self.user)
        bookings[1].booking_status.clear()
        bookings[1].booking_status.add(Booking_Status.objects.get(booking_status='Returned'))
        bookings[1].save()
        bookings[2].booking_status.clear()
        bookings[2].booking_status.add(Booking_Status.objects.get(booking_status='Cancelled'))
        bookings[2].save()

        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        deleted_user = User.objects.get(pk=user_id)
        bookings_after_delete = Booking.objects.filter(user_id=deleted_user.pk)
        reordered_bookings =[bookings_after_delete[2], bookings_after_delete[0], bookings_after_delete[1]]
        # check if booking of deleted user is cancelled
        self.assertEqual(reordered_bookings[0].booking_status.all().first().booking_status, Booking_Status.objects.get(booking_status='Cancelled').booking_status)
        self.assertEqual(reordered_bookings[1].booking_status.all().first().booking_status, Booking_Status.objects.get(booking_status='Returned').booking_status)
        self.assertEqual(reordered_bookings[2].booking_status.all().first().booking_status, Booking_Status.objects.get(booking_status='Cancelled').booking_status)
        self.assertTrue(reordered_bookings[0].pk < reordered_bookings[1].pk)
        self.assertTrue(reordered_bookings[1].pk < reordered_bookings[2].pk)

   # def test_delete_account_with_active_booking(self):

