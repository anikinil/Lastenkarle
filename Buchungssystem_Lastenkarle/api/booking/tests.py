from api.api_tests import *
from db_model.models import *
from rest_framework import status


class Test_booking_get_all_regions(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/region', http_method='GET')

    def test_booking_get_all_regions_integrity(self):
        self.validate_integrity_list(RegionSerializer(Region.objects.all(), many=True).data, self.url_template)

    def test_booking_get_all_regions_functionality(self):
        for i in range(2):
            if i == 1:
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request()
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_booking_get_all_availabilities(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/availabilities', http_method='GET')

    def test_booking_get_all_availabilities_integrity(self):
        self.validate_integrity_list(AvailabilitySerializer(Availability.objects.all(), many=True).data,
                                     self.url_template)

    def test_booking_get_all_availabilities_functionality(self):
        for i in range(2):
            if i == 1:
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request()
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_booking_get_all_bikes(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/bikes', http_method='GET')

    def test_booking_get_all_bikes_integrity(self):
        self.validate_integrity_list(BikeSerializer(Bike.objects.all(), many=True).data, self.url_template)

    def test_booking_get_all_bikes_functionality(self):
        for i in range(2):
            if i == 1:
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request()
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_booking_get_all_stores(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/stores', http_method='GET')

    def test_booking_get_all_stores_integrity(self):
        self.validate_integrity_list(StoreSerializer(Store.objects.all(), many=True).data, self.url_template)

    def test_booking_get_all_stores_functionality(self):
        for i in range(2):
            if i == 1:
                self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
            response = self.make_request()
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_booking_get_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/bikes/{}', http_method='GET')

    def test_booking_get_bike_functionality(self):
        for bike in Bike.objects.all():
            for i in range(2):
                if i == 1:
                    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
                response = self.make_request(self.assign_values_to_placeholder(self.url_template, bike.pk))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                response_data = response.json()
                self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_booking_get_bike_integrity(self):
        for bike in Bike.objects.all():
            response = self.make_request(self.assign_values_to_placeholder(self.url_template, bike.pk))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_data = response.json()
            self.validate_integrity(response_data, self.serialize_bike_with_relations(bike))

    def test_booking_get_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_customer_taylor_token, 25, self.regex_non_natural_numbers)
        response = self.make_request(
            self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_booking_get_store_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/bikes/{}/store', http_method='GET')

    def test_booking_get_store_of_bike_functionality(self):
        for store in Store.objects.all():
            for bike in Bike.objects.filter(store=store):
                for i in range(2):
                    if i == 1:
                        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
                    response = self.make_request(self.assign_values_to_placeholder(self.url_template, bike.pk))
                    self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_get_store_of_bike_integrity(self):
        for store in Store.objects.all():
            for bike in Bike.objects.filter(store=store):
                response = self.make_request(self.assign_values_to_placeholder(self.url_template, bike.pk))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                response_data = response.json()
                self.validate_integrity(response_data, self.serialize_store_with_relations(store))

    def test_booking_get_store_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_customer_taylor_token, 25, self.regex_non_natural_numbers)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_booking_get_availability_of_bike(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/bikes/{}/availability', http_method='GET')

    def test_booking_get_availability_of_bike_functionality(self):
        for bike in Bike.objects.all():
            for i in range(2):
                if i == 1:
                    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_taylor_token)
                response = self.make_request(self.assign_values_to_placeholder(self.url_template, bike.pk))
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_get_availability_of_bike_integrity(self):
        for bike in Bike.objects.all():
            self.validate_integrity_list(AvailabilitySerializer(Availability.objects.filter(bike=bike), many=True).data,
                                         self.assign_values_to_placeholder(self.url_template, bike.pk))

    def test_booking_get_availability_of_bike_handling_invalid_url(self):
        self.invalid_url_params(self.user_customer_taylor_token, 25, self.regex_non_natural_numbers)
        response = self.make_request(self.assign_values_to_placeholder(self.url_template, self.random_number_not_in_id_set('Bike')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_booking_post_make_booking(APITestCase):
    def setUp(self):
        super().setUp(url='/api/booking/v1/bikes/{}/booking', http_method='POST')
        self.booking_count = Booking.objects.all().count()

    def test_booking_post_make_booking_functionality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk),
                                     data=self.booking_data_test)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.booking_count + 1, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_booked_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_graphs.pk),
                                     data={'begin': '2123-10-08', 'end': '2123-10-11', 'equipment': []})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_equipment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk),
                                     data=self.booking_data_test_with_equipment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.booking_count + 1, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_time_causality(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk),
                                     data={'begin': '1999-12-12', 'end': '1999-12-14'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk),
                                     data={'begin': '2124-01-12', 'end': '2124-01-11'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_maximum_duration(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_ikae.pk),
                                     data={'begin': '2124-01-12', 'end': '2124-01-20'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_begin_on_closed_day(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_graphs.pk),
                                     data={'begin': '2124-01-15', 'end': '2124-01-18'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())

    def test_booking_post_make_booking_handling_end_on_closed_day(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_customer_wildegard_token)
        response = self.make_request(url=self.assign_values_to_placeholder(self.url_template, self.bike1_of_graphs.pk),
                                     data={'begin': '2124-01-12', 'end': '2124-01-15'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking_count, Booking.objects.all().count())
