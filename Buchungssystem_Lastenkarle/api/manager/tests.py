from api.api_tests import *
from db_model.models import *
from rest_framework import status


class Test_manager_get_all_equipment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/equipment', http_method='GET')

    def test_manager_get_all_equipment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_all_equipment_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        self.validate_integrity_list(EquipmentSerializer(Equipment.objects.all(), many=True).data, self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))

    def test_manager_get_all_equipment_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.invalid_permissions(user_token=self.user_administrator_caro_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))

    def test_manager_get_all_equipment_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_manager_get_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/store-page', http_method='GET')

    def test_manager_get_store_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_store_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.validate_integrity(response_data, self.serialize_store_with_relations(self.store_ikae))

    def test_manager_get_store_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.invalid_permissions(user_token=self.user_administrator_caro_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))

    def test_manager_get_store_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_manager_patch_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/store-page', http_method='PATCH')
        self.store_update_data = self.get_copy(self.store_data_test)
        del self.store_update_data['region']

    def test_manager_patch_store_functionality_and_integrity(self):
        data = self.get_copy(self.store_update_data)
        del data['address']
        del data['name']
        for i in range(1, len(data)):
            change = self.random_exclude_key_value_pairs(data, i)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=change)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.store_ikae.refresh_from_db()
            self.validate_integrity(response_data, self.serialize_store_with_relations(self.store_ikae))
            Store.objects.filter(pk=self.store_ikae.pk).update(
                **{attr_name: attr_value for attr_name, attr_value in data.items() if
                   hasattr(Store, attr_name)})

    def test_manager_patch_store_unauthorized(self):
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_taylor_token, data=self.store_update_data)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_wildegard_token, data=self.store_update_data)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_administrator_caro_token, data=self.store_update_data)

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
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_manager_post_user_enrollment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/enrollment', http_method='POST')
        self.enroll_taylor_data = {'contact_data': self.user_customer_taylor.contact_data}

    def test_manager_post_user_enrollment_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=self.enroll_taylor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_customer_taylor.refresh_from_db()
        self.assertIn(self.store_ikae.store_flag, self.user_customer_taylor.user_flags.all())

    def test_manager_post_user_enrollment_unauthorized(self):
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_taylor_token, data=self.enroll_taylor_data)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_wildegard_token, data=self.enroll_taylor_data)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_administrator_caro_token, data=self.enroll_taylor_data)

    def test_manager_post_user_enrollment_handling_enrolled_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data={'contact_data': self.user_manager_store_koeri.contact_data})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_post_user_enrollment_handling_invalid_request_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data={'contact_data': 'adwawdhadawd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data={'contact_data': 'uqfol@student.kit.edu'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_manager_get_all_bikes(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes', http_method='GET')

    def test_manager_get_all_bikes_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_all_bikes_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        self.validate_integrity_list(BikeSerializer(Bike.objects.all(), many=True).data, self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))

    def test_manager_get_all_bikes_unauthorized(self):
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_taylor_token)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_administrator_caro_token)


class Test_manager_post_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes', http_method='POST')

    def test_manager_post_bike_functionality(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_post_bike_integrity(self):
        with open(self.image_path_bike, 'rb') as image_file:
            data = {
                'name': 'KI',
                'description': 'gki ist ne Blöde!',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(Bike.objects.get(name='KI')))

    def test_manager_post_bike_unauthorized(self):
        for token in [self.user_customer_taylor_token, self.user_customer_wildegard_token, self.user_administrator_caro_token]:
            with open(self.image_path_bike, 'rb') as image_file:
                self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=token,
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
                response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), data=data, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(bike_count, Bike.objects.all().count())


class Test_manager_post_add_equipment_to_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}/equipment/add', http_method='POST')

    def test_manager_post_add_equipment_to_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk), data=self.equipment_data_gunde)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(Equipment.objects.get(equipment=self.equipment_data_gunde['equipment']), bike.bike_equipment.all())

    def test_manager_post_add_equipment_to_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk),
                                     data=self.equipment_data_gunde)
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk),
                                     data=self.equipment_data_gunde)

    def test_manager_post_add_equipment_to_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_manager_store_koeri_token, number_of_combinations=25,
                                regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}', http_method='GET')

    def test_manager_get_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_bike_integrity(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_manager_get_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))

    def test_manager_get_bike_handling_invalid_url(self):
        self.invalid_url_params(user_token=self.user_manager_store_koeri_token, number_of_combinations=25,
                                regex=self.regex_non_natural_numbers, data=self.equipment_data_gunde)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Bike')),
            data=self.equipment_data_gunde)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_patch_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}/update', http_method='PATCH')

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
                    response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk),
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
                self.invalid_permissions(user_token=self.user_customer_taylor_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_customer_wildegard_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk), data=data, format='multipart')
                self.invalid_permissions(user_token=self.user_administrator_caro_token, path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk), data=data, format='multipart')

    def test_manager_patch_bike_handling_invalid_url(self):
        with open(self.update_image_path_bike, 'rb') as image_file:
            data = {
                'name': 'Gott',
                'description': 'Nie wieder die Waschmaschine',
                'image': image_file
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Bike')), data=data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_patch_bike_handling_update_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike1_of_ikae.pk), data={'store': 4001})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manager_patch_bike_handling_update_equipment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike1_of_ikae.pk), data={'bike_equipment': 301})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_manager_post_remove_equipment_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}/equipment/remove', http_method='POST')
        self.eq = {'equipment': 'Tarp'}

    def test_manager_post_remove_equipment_of_bike_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike2_of_ikae_with_equipment.pk), self.eq)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bike2_of_ikae_with_equipment.refresh_from_db()
        self.assertNotIn(Equipment.objects.get(equipment='Tarp'), self.bike2_of_ikae_with_equipment.bike_equipment.all())

    def test_manager_post_remove_equipment_of_bike_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike2_of_ikae_with_equipment.pk),
                                 data=self.eq)
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike2_of_ikae_with_equipment.pk),
                                 data=self.eq)
        self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike2_of_ikae_with_equipment.pk),
                                 data=self.eq)

    def test_manager_post_remove_equipment_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Bike')), data=self.eq)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_delete_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}/delete', http_method='DELETE')
        self.booking1 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-01', '2123-10-02')
        self.booking2 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-08', '2123-10-09')
        self.booking3 = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike_for_deletion,
                                                             'Booked', '2123-10-15', '2123-10-16')

    def test_manager_delete_bike_functionality(self):
        bike_count = Bike.objects.all().count()
        bike = self.bike_for_deletion
        booking_of_bike = Booking.objects.filter(bike=bike)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike_for_deletion.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(bike, Bike.objects.all())
        self.assertEqual(bike_count - 1, Bike.objects.all().count())
        for booking in booking_of_bike:
            self.assertIn(Booking_Status.objects.get(status='Cancelled'), booking.booking_status.all())
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 0, self.booking1.user.username, self.booking1.bike.name, self.booking1.bike.store.name, self.booking1.begin, self.booking1.end)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 1, self.booking2.user.username, self.booking2.bike.name, self.booking2.bike.store.name, self.booking2.begin, self.booking2.end)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 2, self.booking3.user.username, self.booking3.bike.name, self.booking3.bike.store.name, self.booking3.begin, self.booking3.end)

    def test_manager_delete_bike_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike_for_deletion.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike_for_deletion.pk))
        self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.bike_for_deletion.pk))

    def test_manager_delete_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_manager_get_availability_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bikes/{}/availability', http_method='GET')

    def test_manager_get_availability_of_bike_functionality(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_availability_of_bike_integrity(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            self.validate_integrity_list(AvailabilitySerializer(Availability.objects.filter(bike=bike), many=True).data,
                                         self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))

    def test_manager_get_availability_of_bike_unauthorized(self):
        for bike in Bike.objects.filter(store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, bike.pk))

    def test_manager_get_availability_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_bookings_of_store(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings', http_method='GET')

    def test_manager_get_bookings_of_store_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_bookings_of_store_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        self.validate_integrity_list(BookingSerializer(Booking.objects.filter(bike__store=self.store_ikae), many=True).data, url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name))

    def test_manager_get_bookings_of_store_unauthorized(self):
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_taylor_token)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_customer_wildegard_token)
        self.invalid_permissions(path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name), user_token=self.user_administrator_caro_token)


class Test_manager_get_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}', http_method='GET')

    def test_manager_get_booking_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_booking_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_get_booking_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))

    def test_manager_get_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_get_booking_by_qr(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/by/{}', http_method='GET')

    def test_manager_get_booking_by_qr_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.string))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_get_booking_by_qr_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.string))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_get_booking_by_qr_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.string))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.string))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.string))

    def test_manager_get_booking_by_qr_handling_invalid_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_patch_comment_of_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}/comment', http_method='PATCH')
        self.comment_data = {'comment': 'Gojo x Geto huehuehue'}

    def test_manager_patch_comment_of_booking_functionality(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk),
                data=self.comment_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_patch_comment_of_booking_integrity(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
            response = self.make_request(
                url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk),
                data=self.comment_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_booking_with_relations(booking))

    def test_manager_patch_comment_of_booking_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk),
                                     data=self.comment_data)
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk),
                                     data=self.comment_data)
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk),
                                     data=self.comment_data)

    def test_manager_patch_comment_of_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_post_report_comment(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}/comment/report', http_method='POST')

    def test_manager_post_report_comment_functionality(self):
        booking = self.booking_picked_up
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_mail("email_templates/AdminUserWarningNotification.html", 0, booking.user.username, booking.bike.store.name, booking.bike.store.address, booking.bike.store.phone_number, booking.bike.store.email, booking.comment)

    def test_manager_post_report_comment_unauthorized(self):
        for booking in Booking.objects.filter(bike__store=self.store_ikae):
            self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))
            self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                     path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, booking.pk))

    def test_manager_post_report_comment_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_manager_post_cancel_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}', http_method='POST')

    def test_manager_post_cancel_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.validate_mail("email_templates/CancellationThroughStoreConfirmation.html", 0, self.booking_of_caro.user.username, self.booking_of_caro.bike.name, self.booking_of_caro.bike.store.name, self.booking_of_caro.begin, self.booking_of_caro.end)

    def test_manager_post_cancel_booking_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))

    def test_manager_post_cancel_booking_integrity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(Booking_Status.objects.get(status='Cancelled'), self.booking_of_caro.booking_status.all())

    def test_manager_post_cancel_booking_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_post_cancel_booking_handling_cancel_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 1)


class Test_manager_post_confirm_bike_handout(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}/hand-out', http_method='POST')

    def test_manager_post_confirm_bike_handout_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_gnocchi_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_graphs.name, self.booking_of_caro.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking_of_caro.refresh_from_db()
        self.assertIn(Booking_Status.objects.get(status='Picked up'), self.booking_of_caro.booking_status.all())
        self.validate_mail("email_templates/BikePickUpConfirmation.html", 0, self.booking_of_caro.user.username, self.booking_of_caro.bike.name, self.booking_of_caro.bike.store.name, self.booking_of_caro.bike.store.address, self.booking_of_caro.bike.store.phone_number, self.booking_of_caro.bike.store.email)

    def test_manager_post_confirm_bike_handout_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))

    def test_manager_post_confirm_bike_handout_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class Test_manager_post_confirm_bike_return(APITestCase):
    def setUp(self):
        super().setUp(url='/api/manager/v1/{}/bookings/{}/return', http_method='POST')

    def test_manager_post_confirm_bike_return_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_picked_up.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking_of_caro.refresh_from_db()
        self.assertIn(Booking_Status.objects.get(status='Returned'), self.booking_picked_up.booking_status.all())
        self.validate_mail("email_templates/BikeDropOffConfirmation.html", 0, self.booking_picked_up.user.username, self.booking_picked_up.bike.name, self.booking_picked_up.bike.store.name, self.booking_picked_up.bike.store.address, self.booking_picked_up.bike.store.phone_number, self.booking_picked_up.bike.store.email)

    def test_manager_post_confirm_bike_return_unauthorized(self):
        self.invalid_permissions(user_token=self.user_customer_taylor_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_customer_wildegard_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))
        self.invalid_permissions(user_token=self.user_administrator_caro_token,
                                 path=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.booking_of_caro.pk))

    def test_manager_post_confirm_bike_return_handling_invalid_url(self):
        self.invalid_url_params(self.user_manager_store_koeri_token, 25, self.regex_non_natural_numbers)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_manager_store_koeri_token)
        response = self.make_request(
            url=self.assign_values_to_placeholder(self.url_template, self.store_ikae.name, self.random_number_not_in_id_set('Booking')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
