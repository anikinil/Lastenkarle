from django.test import TestCase
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.test import APIRequestFactory
from db_model.models import User_Status, User
from api.user.v1.views import RegistrateUser
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json

from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from configs.global_variables import lastenkarle_logo_url
from configs.global_variables import spenden_link
from configs.global_variables import lastenkarle_contact_data

from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class RegistrateUserTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_data = {
            'username': 'Wildegard',
            'password': 'password',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        self.registrate_url = '/api/user/v1/register'

    def test_user_registration(self):
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
        registration_link = CANONICAL_HOST + "/email-verification/" + str(user.pk) + "/" + user.verification_string
        html_message = render_to_string("email_templates/UserRegisteredConfirmation.html",
                                        {'username': self.user_data['username'],
                                         'lastenkarle_logo_url': lastenkarle_logo_url,
                                         'registration_link': registration_link})
        self.assertEqual(first_message.body, html_message)

    def test_invalid_user_registration(self):
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
        response = RegistrateUser.as_view()(request)
        # missing credentials
        invalid_user_data = {
            'username': 'testuser',
        }
        request = self.factory.post(self.registrate_url, invalid_user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to register same user for the second time
        request = self.factory.post(self.registrate_url, self.user_data, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if User is doubled in database
        user_count = User.objects.filter(username=self.user_data['username']).count()
        self.assertEqual(user_count, 1)

        # Check that no emails are sent
        self.assertEqual(0, len(mail.outbox))

        # Try to register user with same username but different contact data
        user_data_with_same_username = {
            'username': 'Wildegard',
            'password': 'password',
            'contact_data': 'ich_bin_fag@gmx.de',
            'year_of_birth': '1901'
        }
        request = self.factory.post(self.registrate_url, user_data_with_same_username, format='json')
        response = RegistrateUser.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user_data = {
            'username': 'Wildegard',
            'password': 'password',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        self.login_data = {
            'username': 'Wildegard',
            'password': 'password',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token, _ = AuthToken.objects.create(self.user)
        self.login_url = '/api/user/v1/login'

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_user(self):
        # Check what happens when logging in nonexistentuser
        invalid_user_data = {
            'username': 'nonexistentuser',
            'password': 'invalidpassword'
        }
        response = self.client.post(self.login_url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertNotIn('user', response.data)

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
        self.user_data = {
            'username': 'Wildegard',
            'password': 'password',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        self.login_data = {
            'username': 'Wildegard',
            'password': 'password',
        }
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

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token TtX84Me4RjFscdABKX60dh4Lj8cjtvPzJSubcfJ6IoB3FMAWydcHlgoycfxEddiw')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_token_of_other_user(self):
        self.second_user_data = {
            'username': 'Wilderich',
            'password': 'password',
            'contact_data': 'ich_bin_fag@gmx.de',
            'year_of_birth': '1901'
        }
        self.second_login_data = {
            'username': 'Wilderich',
            'password': 'password'
        }
        # create second user
        self.second_user = User.objects.create_user(**self.second_user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.second_login_data)
        # Parse the response content to get the token
        response_data = json.loads(response.content.decode('utf-8'))
        self.second_token = response_data.get('token', None)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
