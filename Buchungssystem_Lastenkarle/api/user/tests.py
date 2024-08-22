from django.test import TestCase
from knox.models import AuthToken
from db_model.models import generate_random_string
from api.api_tests import APITestCase, BookingSerializer
from db_model.models import User_Flag, User, Equipment, Availability_Status, Booking_Status, Booking
from rest_framework import status
from django.core import mail
from django.template.loader import render_to_string
import json
from unittest import skip
from django.core import serializers
from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST
from configs.global_variables import lastenkarle_logo_url


class Test_default_migration(TestCase):
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
        self.find_and_test_terms_in_json(search_terms, booking_status_json, 'status')

        user_flags = User_Flag.objects.all()
        user_flags_json = serializers.serialize('json', user_flags)
        search_terms = ['Verified', 'Deleted', 'Reminded', 'Administrator', 'Banned', 'Customer']
        self.find_and_test_terms_in_json(search_terms, user_flags_json, 'flag')

    def find_and_test_terms_in_json(self, search_terms, search_json, field_name):
        list = json.loads(search_json)
        found_equipment = [item['fields'][field_name] for item in list]
        for term in search_terms:
            self.assertIn(term, found_equipment)


class Test_user_post_register(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/register', http_method='POST')

    def test_user_post_register_functionality(self):
        response = self.make_request(data=self.user_data_new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(User.objects.get(contact_data=self.user_data_new_user['contact_data']), User.objects.all())

    def test_user_post_register_handling_missing_credentials(self):
        user_count = User.objects.all().count()
        for i in range(len(self.user_data_new_user)):
            data = self.random_exclude_key_value_pairs(self.user_data_new_user, i + 1)
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(user_count, User.objects.all().count())

    def test_user_post_register_handling_register_twice(self):
        user_count = User.objects.all().count()
        response = self.make_request(data=self.user_data_customer_taylor)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_count, User.objects.all().count())

    def test_user_post_register_handling_invalid_request_payload(self):
        user_count = User.objects.all().count()
        for i in range(2):
            data = None
            if i == 0:
                data = {
                    'username': 'Swift',
                    'password': 'password',
                    'contact_data': 'gnocchi_werk@gmx.de',
                }
            if i == 1:
                data = {
                    'username': 'Gnocchi',
                    'password': 'password',
                    'contact_data': 'janderda@web.de',
                }
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(user_count, User.objects.all().count())


class Test_user_post_login(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/login', http_method='POST')

    def test_user_post_login_functionality(self):
        User.objects.create_user(**self.user_data_new_user)
        response = self.make_request(data=self.get_login_data_from_user_data(self.user_data_new_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_post_login_handling_trailing_whitespaces_username(self):
        copy = self.get_copy(self.user_data_customer_taylor)
        copy['username'] = 'Taylor    '
        response = self.make_request(data=self.get_login_data_from_user_data(copy))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_post_login_handling_login_twice(self):
        response = self.make_request(data=self.get_login_data_from_user_data(self.user_data_customer_taylor))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_post_login_handling_invalid_request_payload(self):
        user_data = {
            'username': 'Is me MARIO',
            'password': 'password'
        }
        response = self.make_request(data=user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_user_post_login_handling_missing_credentials(self):
        login_data_taylor = self.get_login_data_from_user_data(self.user_data_customer_taylor)
        for i in range(len(login_data_taylor)):
            data = self.random_exclude_key_value_pairs(login_data_taylor, i + 1)
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)

    def test_user_post_login_handling_incorrect_password(self):
        for i in range(1, 64):
            password = None
            while password is None or password == 'password':
                password = generate_random_string(i)
            login_data_taylor = {'username': 'Taylor', 'password': password}
            response = self.make_request(data=login_data_taylor)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)

    def test_user_post_login_handling_login_banned_user(self):
        self.add_flag_to_user(self.user_customer_wildegard, 'Banned')
        response = self.make_request(data=self.get_login_data_from_user_data(self.user_data_customer_wildegard))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_user_post_login_handling_deleted_user(self):
        self.delete_user(self.user_customer_wildegard)
        self.add_flag_to_user(self.user_customer_wildegard, 'Deleted')
        response = self.make_request(data=self.get_login_data_from_user_data(self.user_data_customer_wildegard))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_user_post_login_handling_username_case_sensitivity(self):
        for i in range(2):
            data = None
            if i == 0:
                data = self.get_copy(self.user_data_customer_taylor)
                data['username'] = data['username'].upper()
            if i == 1:
                data = self.get_copy(self.user_data_customer_taylor)
                data['username'] = data['username'].lower()
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)

    def test_user_post_login_handling_blank_username(self):
        copy = self.get_copy(self.user_data_customer_taylor)
        copy['username'] = ''
        response = self.make_request(data=self.get_login_data_from_user_data(copy))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class Test_user_post_logout(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/logout', http_method='POST')

    def test_user_post_logout_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.user_customer_taylor_token, AuthToken.objects.all())

    def test_user_post_logout_handling_single_logout(self):
        second_token = self.login_user(self.user_customer_taylor, self.user_data_customer_taylor).data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.user_customer_taylor_token, AuthToken.objects.all())

    def test_user_post_logout_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_logout_handling_invalid_auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Test_user_post_logout_all(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/logout-all', http_method='POST')

    def test_user_post_logout_all_functionality(self):
        for i in range(1, 4):
            self.login_user(self.user_customer_taylor, self.get_login_data_from_user_data(self.user_data_customer_taylor))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AuthToken.objects.filter(user=self.user_customer_taylor).exists())

    def test_user_post_logout_all_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post_logout_all_handling_invaild_auth_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Test_user_get_user_data(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/data', http_method='GET')

    def test_user_get_user_data_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_user_data_unauthorized(self):
        self.invalid_permissions(user_token=' ')

    def test_user_get_user_data_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.validate_integrity(response_data, self.serialize_user_with_relations(self.user_customer_taylor))


class Test_user_patch_user_data(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/update', http_method='PATCH')
        self.user_data_changed_taylor = {'username': 'Thailor', 'contact_data': 'janderda@web.de', 'password': 'jto'}
        self.invalid_change_data = {'username': 'Caro', 'contact_data': 'bitte_toete_mich@gmx.de', 'year_of_birth': '1999', 'is_staff': True, 'is_superuser': True}

    def test_user_patch_user_data_functionality_and_integrity(self):
        copy = self.get_copy(self.user_data_changed_taylor)
        for i in range(len(self.user_data_changed_taylor)):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request(data=self.random_exclude_key_value_pairs(copy, i))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.user_customer_taylor.refresh_from_db()
            db_data = self.serialize_user_with_relations(self.user_customer_taylor)
            self.validate_integrity(response_data, db_data)
            User.objects.filter(pk=self.user_customer_taylor.pk).update(
                **{attr_name: attr_value for attr_name, attr_value in self.user_data_customer_taylor.items() if
                   hasattr(User, attr_name)})

    def test_user_patch_user_data_unauthorized(self):
        self.invalid_permissions(user_token=' ', data=self.get_copy(self.user_data_changed_taylor))

    def test_user_patch_user_data_handling_empty_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_patch_user_data_handling_update_user_data_with_invalid_data(self):
        for i in range(len(self.invalid_change_data) - 1):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            data = self.random_exclude_key_value_pairs(self.get_copy(self.invalid_change_data), i)
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_user_delete_account(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/delete-account', http_method='DELETE')

    def test_user_delete_account_functionality(self):
        koeri = self.user_manager_store_koeri.contact_data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(contact_data=koeri).exists())

    def test_user_delete_account_unauthorized(self):
        self.invalid_permissions(user_token=' ')

    def test_user_delete_account_handling_single_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(User_Flag.objects.get(flag='Deleted'), self.user_administrator_caro.user_flags.all())

    def test_user_delete_account_handling_bike_picked_up(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(User_Flag.objects.get(flag='Deleted'), self.user_customer_taylor.user_flags.all())

    def test_user_delete_account_handling_bookings(self):
        self.booking_picked_up.booking_status.remove(Booking_Status.objects.get(status='Picked up'))
        self.booking_picked_up.booking_status.add(Booking_Status.objects.get(status='Returned'))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(User_Flag.objects.get(flag='Deleted'), self.user_customer_taylor.user_flags.all())
        for booking in Booking.objects.filter(user=self.user_customer_taylor):
            if not booking.booking_status.contains(Booking_Status.objects.get(status='Returned')):
                self.assertIn(Booking_Status.objects.get(status='Cancelled'), booking.booking_status.all())


class Test_user_post_confirm_mail(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/{}/{}', http_method='POST')

    def test_user_post_confirm_mail_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk,
                                                                       self.user_customer_taylor.verification_string))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(User_Flag.objects.get(flag='Verified'), self.user_customer_taylor.user_flags.all())
        self.user_customer_taylor.refresh_from_db()
        self.assertIsNone(self.user_customer_taylor.verification_string)

    def test_user_post_confirm_mail_handling_confirmation_twice(self):
        old_verification_string = self.user_customer_taylor.verification_string
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk,
                                                                       self.user_customer_taylor.verification_string))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk, old_verification_string))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(User_Flag.objects.get(flag='Verified'), self.user_customer_taylor.user_flags.all())

    def test_user_post_confirm_mail_handling_invalid_url(self):
        self.invalid_url_params(self.user_customer_taylor_token, 5, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk, ''))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_user_get_all_bookings(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/bookings', http_method='GET')

    def test_user_get_all_bookings_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BookingSerializer(Booking.objects.all(), many=True).data, self.url_template)

    def test_user_get_all_bookings_unauthorized(self):
        self.invalid_permissions(user_token=' ')


class Test_user_get_booking(APITestCase):

    def setUp(self):
        super().setUp(url='/api/user/v1/user/bookings/{}', http_method='GET')

    def test_user_get_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        for booking in self.taylor_bookings:
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_booking_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        for booking in self.taylor_bookings:
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            db_data = self.serialize_booking_with_relations(booking)
            self.validate_integrity(response_data, db_data)

    def test_user_get_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_customer_taylor_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_user_post_cancel_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/bookings/{}', http_method='POST')

    def test_user_post_cancel_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.booking_cancel.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(Booking_Status.objects.get(status='Cancelled'), self.booking_cancel.booking_status.all())

    def test_user_post_cancel_booking_handling_picked_up_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.booking_picked_up.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_cancel_booking_handling_bike_returned(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.booking_returned.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_cancel_booking_handling_foreign_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_post_cancel_booking_handling_cancel_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        url = self.assign_values_to_placeholder(self.url_template, self.booking_cancel.pk)
        response = self.make_request(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.make_request(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_cancel_booking_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_user_get_bike_of_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/bookings/{}/bike', http_method='GET')

    def test_user_get_bike_of_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        for booking in self.taylor_bookings:
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(booking.bike))

    def test_user_get_bike_of_booking_handling_foreign_booking(self):
        for booking in Booking.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.client.credentials(HTTP_AUTHORIZATION='Token ')
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_bike_of_booking_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_user_get_store_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/user/v1/user/bookings/{}/bike/store', http_method='GET')

    def test_user_get_store_of_bike_functionality(self):
        for booking in self.taylor_bookings:
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_store_of_bike_integrity(self):
        for booking in self.taylor_bookings:
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_store_with_relations(booking.bike.store))

    def test_user_get_store_of_bike_handling_foreign_booking(self):
        for booking in Booking.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.client.credentials(HTTP_AUTHORIZATION='Token ')
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_store_of_bike_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)