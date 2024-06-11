from api.api_tests import *
from db_model.models import *
from rest_framework import status


class Test_manager_get_all_equipment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/equipment', http_method='GET')

    def test_manager_get_all_equipment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_all_equipment_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(EquipmentSerializer(Equipment.objects.all(), many=True).data, self.url_template)

    def test_manager_get_all_equipment_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_administrator_caro_token)


class Test_manager_get_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/store-page', http_method='GET')

    def test_manager_get_store_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_store_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.validate_integrity(response_data, self.serialize_store_with_relations(self.store_ikae))

    def test_manager_get_store_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_administrator_caro_token)


class Test_manager_patch_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/store-page', http_method='PATCH')
        self.store_update_data = self.get_copy(self.store_data_test)
        del self.store_update_data['region']

    def test_manager_patch_store_functionality_and_integrity(self):
        data = self.get_copy(self.store_update_data)
        del data['address']
        del data['name']
        for i in range(1, len(data)):
            change = self.random_exclude_key_value_pairs(data, i)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(data=change)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.store_ikae.refresh_from_db()
            self.validate_integrity(response_data, self.serialize_store_with_relations(self.store_ikae))
            Store.objects.filter(pk=self.store_ikae.pk).update(
                **{attr_name: attr_value for attr_name, attr_value in data.items() if
                   hasattr(Store, attr_name)})

    def test_manager_patch_store_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, data=self.store_update_data)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, data=self.store_update_data)
        self.invalid_permissions(user_token=self.user_administrator_caro_token, data=self.store_update_data)

    def test_manager_patch_store_handling_illegal_updates(self):
        for i in range(4):
            data = None
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            if i == 0:
                data = {'region': 'Malsch'}
            if i == 1:
                data = {'store_flag': 37}
            if i == 2:
                data = {'address': 'Ren Str. 17'}
            if i == 3:
                data = {'name': 'Gudelgunde von Gonde'}
            response = self.make_request(data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_manager_post_user_enrollment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/enrollment', http_method='POST')
        self.enroll_taylor_data = {'contact_data': self.user_customer_taylor.contact_data}

    def test_manager_post_user_enrollment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(data=self.enroll_taylor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_customer_taylor.refresh_from_db()
        self.assertIn(self.store_ikae.store_flag, self.user_customer_taylor.user_flags.all())

    def test_manager_post_user_enrollment_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, data=self.enroll_taylor_data)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, data=self.enroll_taylor_data)
        self.invalid_permissions(user_token=self.user_administrator_caro_token, data=self.enroll_taylor_data)

    def test_manager_post_user_enrollment_handling_enrolled_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(data={'contact_data': self.user_manager_store_koeri.contact_data})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_post_user_enrollment_handling_invalid_request_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(data={'contact_data': 'adwawdhadawd'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(data={'contact_data': 'uqfol@student.kit.edu'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_all_bikes(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes', http_method='GET')

    def test_manager_get_all_bikes_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_all_bikes_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BikeSerializer(Bike.objects.all(), many=True).data, self.url_template)

    def test_manager_get_all_bikes_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_administrator_caro_token)


class Test_manager_post_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes', http_method='POST')

    def test_manager_post_bike_functionality(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_post_bike_integrity(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(Bike.objects.get(name='KI')))

    def test_manager_post_bike_unauthorized(self):
        for token in [self.user_customer_taylor_token, self.user_customer_wildegard_token, self.user_administrator_caro_token]:
            with open(self.image_path_bike, 'rb') as image_file:
                self.invalid_permissions(user_token=token,
                                         data={
                                             'name': 'KI',
                                             'description': 'gki ist ne Blöde!',
                                             'image': image_file
                                         },
                                         format='multipart')

    def test_manager_post_bike_handling_invalid_request_payload(self):
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
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
                response = self.make_request(data=data, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(bike_count, Bike.objects.all().count())


class Test_manager_post_add_equipment_to_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes/{}/equipment', http_method='POST')

    def test_manager_post_add_equipment_to_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk), data=self.equipment_data_gunde)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(Equipment.objects.get(equipment=self.equipment_data_gunde['equipment']), bike.bike_equipment.all())

    def test_manager_post_add_equipment_to_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                     data=self.equipment_data_gunde)

    def test_manager_post_add_equipment_to_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_manager_store_koeri_token, number_of_combinations=25,
                                regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes/{}', http_method='GET')

    def test_manager_get_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_bike_integrity(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_manager_get_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_manager_get_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_manager_store_koeri_token, number_of_combinations=25,
                                regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_patch_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes/{}/update', http_method='PATCH')

    def test_manager_patch_bike_functionality_and_integrity(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            for i in range(3):
                with open(self.update_image_path_bike, 'rb') as image_file:
                    data = self.random_exclude_key_value_pairs({
                        'name': 'calgon',
                        'description': 'Apfelbaum',
                        'image': image_file
                        }, i)
                    if 'image' in data:
                        image_file.seek(0)
                    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
                    response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk),
                                                 data=data, format='multipart')
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    response_data = response.json()
                    bike.refresh_from_db()
                    self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_manager_patch_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            with open(self.update_image_path_bike, 'rb') as image_file:
                data = {
                    'name': 'calgon',
                    'description': 'Apfelbaum',
                    'image': image_file
                }
                self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_administrator_caro_token, path=self.assign_values_to_placeholder(self.url_template, bike.pk), data=data, format='multipart')

    def test_manager_patch_bike_handling_invalid_url(self):
        with open(self.update_image_path_bike, 'rb') as image_file:
            data = {
                'name': 'Gott',
                'description': 'Nie wieder die Waschmaschine',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')), data=data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_patch_bike_handling_update_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk), data={'store': 4001})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_patch_bike_handling_update_equipment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk), data={'bike_equipment': 301})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_manager_get_availability_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bikes/{}/availability', http_method='GET')

    def test_manager_get_availability_of_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_availability_of_bike_integrity(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.validate_integrity_list(AvailabilitySerializer(Availability.objects.filter(bike=bike), many=True).data,
                                         self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_manager_get_availability_of_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_manager_get_availability_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_bookings_of_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bookings', http_method='GET')

    def test_manager_get_bookings_of_store_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_bookings_of_store_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_integrity_list(BookingSerializer(Booking.objects.filter(bike__store=self.store_ikae), many=True).data, url=self.url_template)

    def test_manager_get_bookings_of_store_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(user_token=self.user_administrator_caro_token)


class Test_manager_get_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bookings/{}', http_method='GET')

    def test_manager_get_booking_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_booking_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_get_booking_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))

    def test_manager_get_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_booking_by_qr(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bookings/by/{}', http_method='GET')

    def test_manager_get_booking_by_qr_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.string))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_booking_by_qr_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.string))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_get_booking_by_qr_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.string))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.string))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.string))

    def test_manager_get_booking_by_qr_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_patch_comment_of_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bookings/{}/comment', http_method='PATCH')
        self.comment_data = {'comment': 'Gojo x Geto huehuehue'}

    def test_manager_patch_comment_of_booking_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk),
                data=self.comment_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_patch_comment_of_booking_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk),
                data=self.comment_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_patch_comment_of_booking_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk),
                                     data=self.comment_data)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk),
                                     data=self.comment_data)
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk),
                                     data=self.comment_data)

    def test_manager_patch_comment_of_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_post_report_comment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/bookings/{}/comment/report', http_method='POST')

    def test_manager_post_report_comment_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_post_report_comment_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, booking.pk))

    def test_manager_post_report_comment_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)