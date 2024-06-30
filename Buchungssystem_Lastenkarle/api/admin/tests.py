from api.api_tests import *
from db_model.models import *
from rest_framework import status
from configs.global_variables import lastenkarle_contact_data
from django.core import mail

class Test_admin_get_equipment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/equipment', http_method='GET')

    def test_admin_get_equipment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_equipment_unauthorized(self):
        self.invalid_permissions(self.user_customer_taylor_token)
        self.invalid_permissions(self.user_customer_wildegard_token)
        self.invalid_permissions(self.user_manager_store_koeri_token)

    def test_admin_get_equipment_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        self.validate_integrity_list(EquipmentSerializer(Equipment.objects.all(), many=True).data, self.url_template)


class Test_admin_get_user_flags(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/user-flags', http_method='GET')

    def test_admin_get_user_flags_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_user_flags_unauthorized(self):
        self.invalid_permissions(self.user_customer_taylor_token)
        self.invalid_permissions(self.user_customer_wildegard_token)
        self.invalid_permissions(self.user_manager_store_koeri_token)

    def test_admin_get_user_flags_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        self.validate_integrity_list(UserFlagSerializer(User_Flag.objects.all(), many=True).data, self.url_template)


class Test_admin_post_user_enrollment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/user-flags', http_method='POST')
        self.enrollment_data_wildegard_ikae = {'contact_data': self.user_customer_wildegard.contact_data, 'flag': self.store_ikae.store_flag.flag}

    def test_admin_post_user_enrollment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data=self.enrollment_data_wildegard_ikae)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.store_ikae.store_flag, self.user_customer_wildegard.user_flags.all())

    def test_admin_post_user_enrollment_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, data=self.enrollment_data_wildegard_ikae)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, data=self.enrollment_data_wildegard_ikae)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token, data=self.enrollment_data_wildegard_ikae)

    def test_admin_post_user_enrollment_handling_enroll_twice(self):
        flag_count = self.user_manager_store_koeri.user_flags.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data={'contact_data': self.user_manager_store_koeri, 'flag': self.store_ikae.store_flag.flag})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(flag_count, self.user_manager_store_koeri.user_flags.all().count())

    def test_admin_post_user_enrollment_handling_invalid_user_flags(self):
        invalid_flags = ['Verified', 'Deleted', 'Reminded', 'Banned', 'Customer']
        flag_count = self.user_customer_wildegard.user_flags.all().count()
        for flag in invalid_flags:
            data = self.get_copy(self.enrollment_data_wildegard_ikae)
            data['flag'] = User_Flag.objects.get(flag=flag).flag
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(flag_count, self.user_customer_wildegard.user_flags.all().count())

    def test_admin_post_user_enrollment_handling_invalid_request_payload(self):
        flag_count = self.user_customer_wildegard.user_flags.all().count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data={'contact_data': self.user_customer_wildegard.contact_data, 'flag': 'Why do we exist?'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(flag_count, self.user_customer_wildegard.user_flags.all().count())
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            data={'contact_data': 'Till the end of time', 'flag': self.store_ikae.store_flag.flag})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_post_user_banning(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/ban-user', http_method='POST')
        self.ban_taylor = {'contact_data': self.user_customer_taylor.contact_data}

    def test_admin_post_user_banning_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data=self.ban_taylor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(User_Flag.objects.get(flag='Banned'), self.user_customer_taylor.user_flags.all())
        self.validate_mail("email_templates/UserBannedMail.html", 0, self.user_customer_taylor.username, lastenkarle_contact_data)

    def test_admin_post_user_banning_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, data=self.ban_taylor)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, data=self.ban_taylor)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token, data=self.ban_taylor)

    def test_admin_post_user_banning_handling_ban_twice(self):
        for i in range(2):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(data=self.ban_taylor)
            if i == 0:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
            if i == 1:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(User_Flag.objects.get(flag='Banned'), self.user_customer_taylor.user_flags.all())

    def test_admin_post_user_banning_handling_invalid_request_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data={'contact_data': 'Ich glaube schon, ja'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data={'contact_data': 'the_voices_in_my_head@gmx.de'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_post_store_creation(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/create/store', http_method='POST')

    def test_admin_post_store_creation_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data=self.store_data_test, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_post_store_creation_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, data=self.store_data_test, format='json')
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, data=self.store_data_test, format='json')
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token, data=self.store_data_test, format='json')

    def test_admin_post_store_creation_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(data=self.store_data_test, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.validate_integrity(response_data, self.serialize_store_with_relations(Store.objects.get(name='Mutter')))

    def test_admin_post_store_creation_handling_invalid_request_payload(self):
        store_count = Store.objects.all().count()
        for i in range(8):
            data = self.get_copy(self.store_data_test)
            if i == 0:
                data['name'] = self.store_ikae.name
            if i == 1:
                del data['region']
            if i == 2:
                data['region'] = {'name': 'Dune 2'}
            if i == 3:
                del data['address']
            if i == 4:
                del data['email']
            if i == 5:
                data['email'] = 'Schaltjahre! Ja ja.'
            if i == 6:
                data['email'] = self.store_ikae.email
            if i == 7:
                del data['name']
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(data=data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(store_count, Store.objects.all().count())


class Test_admin_post_create_bike_of_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/create/store/{}/bike', http_method='POST')

    def test_admin_post_create_bike_of_store_functionality(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk),
                                         data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_post_create_bike_of_store_integrity(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk),
                                         data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(Bike.objects.get(name='KI')))

    def test_admin_post_create_bike_of_store_unauthorized(self):
        for token in [self.user_customer_taylor_token, self.user_customer_wildegard_token, self.user_manager_store_koeri_token]:
            with open(self.image_path_bike, 'rb') as image_file:
                self.invalid_permissions(user_token=token,
                                         path=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk),
                                         data={
                                                'name': 'KI',
                                                'description': 'gki ist ne Blöde!',
                                                'image': image_file
                                                },
                                         format='multipart')

    def test_admin_post_create_bike_of_store_handling_invalid_url(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Store')), data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_post_create_bike_of_store_handling_invalid_request_payloads(self):
        bike_count = Bike.objects.all().count()
        for i in range(4):
            with open(self.image_path_bike, 'rb') as image_file:
                data = {
                    'name': 'KI',
                    'description': 'gki ist ne Blöde!',
                    'image': image_file
                }
                if i == 0:
                    del data['name']
                if i == 1:
                    del data['description']
                if i == 2:
                    del data['image']
                if i == 3:
                    data['image'] = ['KEIN BILD']
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
                response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk), data=data, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(bike_count, Bike.objects.all().count())


class Test_admin_delete_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/delete/bike/{}', http_method='DELETE')
        self.booking1 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-01', '2123-10-02')
        self.booking2 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-08', '2123-10-09')
        self.booking3 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-15', '2123-10-16')

    def test_admin_delete_bike_functionality(self):
        bike_count = Bike.objects.all().count()
        bike = self.bike_for_deletion
        booking_of_bike = Booking.objects.filter(bike=bike)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike_for_deletion.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(bike, Bike.objects.all())
        self.assertEqual(bike_count - 1, Bike.objects.all().count())
        for booking in booking_of_bike:
            self.assertIn(Booking_Status.objects.get(status='Cancelled'), booking.booking_status.all())
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 0, self.booking1.user.username, self.booking1.bike.name, self.booking1.bike.store.name, self.booking1.begin, self.booking1.end)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 1, self.booking2.user.username, self.booking2.bike.name, self.booking2.bike.store.name, self.booking2.begin, self.booking2.end)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 2, self.booking3.user.username, self.booking3.bike.name, self.booking3.bike.store.name, self.booking3.begin, self.booking3.end)

    def test_admin_delete_bike_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike_for_deletion.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike_for_deletion.pk))
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike_for_deletion.pk))

    def test_admin_delete_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_delete_bike_handling_deletion_picked_up_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.booking_picked_up.bike.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_delete_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/delete/store/{}', http_method='DELETE')

    def test_admin_delete_store_functionality(self):
        store = self.store_graphs
        args = [self.booking_of_caro.user.username, self.booking_of_caro.bike.name, self.booking_of_caro.bike.store.name, self.booking_of_caro.begin, self.booking_of_caro.end]
        bike_count = Bike.objects.all().count()
        bike_count_store = Bike.objects.filter(store=store).count()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(store, Store.objects.all())
        self.assertEqual(bike_count - bike_count_store, Bike.objects.all().count())
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 0, *args)

    def test_admin_delete_store_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk))
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk))

    def test_admin_delete_store_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Store')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_delete_store_handling_bike_picked_up(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.booking_picked_up.bike.store.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_get_all_users(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/users', http_method='GET')

    def test_admin_get_all_users_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_all_users_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token)

    def test_admin_get_all_users_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(UserSerializer(User.objects.all(), many=True).data, self.url_template)


class Test_admin_get_user(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/users/{}', http_method='GET')

    def test_admin_get_user_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_user_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token, path=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))

    def test_admin_get_user_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.validate_integrity(response_data, self.serialize_user_with_relations(self.user_customer_taylor))

    def test_admin_get_user_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('User')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_get_all_bookings_of_user(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/users/{}/bookings', http_method='GET')

    def test_admin_get_all_bookings_of_user_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_all_bookings_of_user_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template,
                                                                        self.user_customer_taylor.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template,
                                                                        self.user_customer_taylor.pk))
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                 path=self.assign_values_to_placeholder(self.url_template,
                                                                        self.user_customer_taylor.pk))

    def test_admin_get_all_bookings_of_user_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BookingSerializer(Booking.objects.all(), many=True).data,
                                     self.assign_values_to_placeholder(self.url_template, self.user_customer_taylor.pk))

    def test_admin_get_all_bookings_of_user_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('User')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_get_all_bookings(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bookings', http_method='GET')

    def test_admin_get_all_bookings_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_all_bookings_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token)

    def test_admin_get_all_bookings_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BookingSerializer(Booking.objects.all(), many=True).data, self.url_template)


class Test_admin_get_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bookings/{}', http_method='GET')

    def test_admin_get_booking_functionality(self):
        for booking in Booking.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_booking_unauthorized(self):
        for booking in Booking.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))

    def test_admin_get_booking_integrity(self):
        for booking in Booking.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_admin_get_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_post_cancel_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bookings/{}', http_method='POST')

    def test_admin_post_cancel_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 0, self.booking_of_caro.user.username, self.booking_of_caro.bike.name, self.booking_of_caro.bike.store.name, self.booking_of_caro.begin, self.booking_of_caro.end)

    def test_admin_post_cancel_booking_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))

    def test_admin_post_cancel_booking_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(Booking_Status.objects.get(status='Cancelled'), self.booking_of_caro.booking_status.all())

    def test_adming_post_cancel_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_post_cancel_booking_handling_cancel_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_post_cancel_booking_handling_not_cancellable_cases(self):
        for i in range(2):
            booking = None
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            if i == 0:
                booking = self.booking_returned
            if i == 1:
                booking = self.booking_picked_up
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn(Booking_Status.objects.get(status='Cancelled'), booking.booking_status.all())


class Test_admin_get_all_bikes(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes', http_method='GET')

    def test_admin_get_all_bikes_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_all_bikes_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BikeSerializer(Bike.objects.all(), many=True).data, self.url_template)

    def test_admin_get_all_bikes_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token)


class Test_admin_get_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes/{}', http_method='GET')

    def test_admin_get_bike_functionality(self):
        for bike in Bike.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_bike_integrity(self):
        for bike in Bike.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_admin_get_bike_unauthorized(self):
        for bike in Bike.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_admin_get_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_get_availabilities_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes/{}/availability', http_method='GET')

    def test_admin_get_availabilities_of_bike_functionality(self):
        for bike in Bike.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_availabilities_of_bike_integrity(self):
        for bike in Bike.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.validate_integrity_list(AvailabilitySerializer(Availability.objects.filter(bike=bike), many=True).data, self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_admin_get_availabilities_of_bike_unauthorized(self):
        for bike in Bike.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_admin_get_availabilities_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_get_all_stores(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/stores', http_method='GET')

    def test_admin_get_all_stores_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_all_stores_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(StoreSerializer(Store.objects.all(), many=True).data, self.url_template)

    def test_admin_get_all_stores_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token)


class Test_admin_get_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/stores/{}', http_method='GET')

    def test_admin_get_store_functionality(self):
        for store in Store.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_store_integrity(self):
        for store in Store.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_store_with_relations(store))

    def test_admin_get_store_unauthorized(self):
        for store in Store.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))

    def test_admin_get_store_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Store')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_get_availabilities_of_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/stores/{}/availability', http_method='GET')

    def test_admin_get_availabilities_of_store_functionality(self):
        for store in Store.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_availabilities_of_store_integrity(self):
        for store in Store.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.validate_integrity_list(AvailabilitySerializer(Availability.objects.all(), many=True).data,
                                         self.assign_values_to_placeholder(self.url_template, store.pk))

    def test_admin_get_availabilities_of_store_unauthorized(self):
        for store in Store.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk))

    def test_admin_get_availabilities_of_store_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Store')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_patch_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/stores/{}/update', http_method='PATCH')
        self.store_update_data = self.get_copy(self.store_data_test)
        del self.store_update_data['region']

    def test_admin_patch_store_functionality_and_integrity(self):
        for store in Store.objects.all():
            old_data = self.get_copy(store.__dict__)
            del old_data['address']
            del old_data['name']
            data = self.get_copy(self.store_update_data)
            del data['address']
            del data['name']
            for i in range(22):
                change = self.random_exclude_key_value_pairs(data, i)
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
                response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, store.pk), data=change)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                response_data = response.json()
                store.refresh_from_db()
                self.validate_integrity(response_data, self.serialize_store_with_relations(store))
                Store.objects.filter(pk=store.pk).update(
                    **{attr_name: attr_value for attr_name, attr_value in old_data.items() if
                       hasattr(Store, attr_name)})

    def test_admin_patch_store_unauthorized(self):
        for store in Store.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk),
                                     data=self.store_update_data)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk),
                                     data=self.store_update_data)
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, store.pk),
                                     data=self.store_update_data)

    def test_admin_patch_store_handling_invalid_url(self):
        self.invalid_url_params(self.user_administrator_caro_token, 25, self.regex_non_natural_numbers, data=self.store_update_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Store')),
            data=self.store_update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_patch_store_handling_illegal_updates(self):
        for i in range(4):
            data = None
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            if i == 0:
                data = {'region': 73}
            if i == 1:
                data = {'address': 'Labertanten Str. 17'}
            if i == 2:
                data = {'store_flag': 37}
            if i == 3:
                data = {'name': 'Gudelgunde von Gonde'}
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.pk),
                                         data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_patch_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes/{}/update', http_method='PATCH')

    def test_admin_patch_bike_functionality_and_integrity(self):
        for bike in Bike.objects.all():
            for i in range(3):
                with open(self.update_image_path_bike, 'rb') as image_file:
                    data = self.random_exclude_key_value_pairs({
                        'name': 'Kartoffeln',
                        'description': 'Sehr Salatisch',
                        'image': image_file
                        }, i)
                    if 'image' in data:
                        image_file.seek(0)
                    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
                    response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                                 data=data, format='multipart')
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    response_data = response.json()
                    bike.refresh_from_db()
                    self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_admin_patch_bike_unauthorized(self):
        for bike in Bike.objects.all():
            with open(self.update_image_path_bike, 'rb') as image_file:
                data = {
                    'name': 'Kartoffeln',
                    'description': 'Sehr Salatisch',
                    'image': image_file
                }
                self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_manager_store_koeri_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')

    def test_admin_patch_bike_handling_invalid_url(self):
        with open(self.update_image_path_bike, 'rb') as image_file:
            data = {
                'name': 'Gott',
                'description': 'Nie wieder die Waschmaschine',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')), data=data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_patch_bike_handling_update_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk), data={'store': 4001})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_patch_bike_handling_update_equipment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk), data={'bike_equipment': 301})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_admin_post_add_equipment_to_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes/{}/equipment', http_method='POST')

    def test_admin_post_add_equipment_to_bike_functionality(self):
        for bike in Bike.objects.all():
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk), data=self.equipment_data_gunde)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(Equipment.objects.get(equipment=self.equipment_data_gunde['equipment']), bike.bike_equipment.all())

    def test_admin_post_add_equipment_to_bike_unauthorized(self):
        for bike in Bike.objects.all():
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)

    def test_admin_post_add_equipment_to_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_administrator_caro_token, number_of_combinations=25, regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_admin_delete_equipment_from_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/admin/v1/bikes/{}/equipment', http_method='DELETE')

    def test_admin_delete_equipment_from_bike_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk), data={'equipment': 'Tarp'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete_equipment_from_bike_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk),
                                 data={'equipment': 'Tarp'})
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk),
                                 data={'equipment': 'Tarp'})
        self.invalid_permissions(user_token=self.user_manager_store_koeri_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk),
                                 data={'equipment': 'Tarp'})

    def test_admin_delete_equipment_from_bike_handling_equipment_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk), data={'equipment': 'We\'ve been told.'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_equipment_from_bike_handling_equipment_not_on_bike(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike2_of_ikae_with_equipment.pk), data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_equipment_from_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_administrator_caro_token, number_of_combinations=25,
                                regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_administrator_caro_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)