import glob
import copy
import re
import json
from django.apps import apps


from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.core import mail
from rest_framework import status
from Buchungssystem_Lastenkarle.settings import CANONICAL_HOST, BASE_DIR
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.test import APIClient, force_authenticate

from api.algorithm import split_availabilities_algorithm
from db_model.models import *
from knox.views import LoginView
from rest_framework import serializers
from django.template.loader import render_to_string

# TODO: sql injections handling

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class AvailabilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_Status
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    availability_status = AvailabilityStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Availability
        fields = '__all__'

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Status
        fields = '__all__'

class BikeSerializer(serializers.ModelSerializer):
    availability_set = AvailabilitySerializer(many=True, read_only=True)
    bike_equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Bike
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=False, read_only=True)
    bike_set = BikeSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

class UserFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Flag
        fields = '__all__'

class LocalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalData
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_flags = UserFlagSerializer(many=True, read_only=True)
    localdata = LocalDataSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    bike = BikeSerializer(many=False, read_only=True)
    booking_status = BookingStatusSerializer(many=True, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class APITestCase(TestCase):
    client = APIClient()
    factory = RequestFactory()
    user_manager = UserManager()
    url_template = 'api/v1/some/{}/some/not'
    http_method = 'GET'
    fields_to_include = []
    image_path_bike = os.path.join(BASE_DIR, 'media/test_image/', 'image.jpg')
    update_image_path_bike = os.path.join(BASE_DIR, 'media/test_image/', 'update_image.jpg')
    image_path_logo = os.path.join(BASE_DIR, 'media/logos/', 'lastenkarle_logo.png')


    user_data_new_user = {
        'username': 'Kai',
        'password': 'password',
        'contact_data': 'janderda@web.de',
    }

    user_data_customer_wildegard = {
        'username': 'Wildegard',
        'password': 'password',
        'contact_data': 'wilde.gard@gmx.de',
        'year_of_birth': '1965'
    }

    user_data_customer_taylor = {
        'username': 'Taylor',
        'password': 'password',
        'contact_data': 'pse_email@gmx.de',
        'year_of_birth': '1989'
    }

    user_data_store_manager_koeri = {
        'username': 'Koeri',
        'password': 'password',
        'contact_data': 'koeri_werk@gmx.de',
        'year_of_birth': '2016',
    }

    user_data_store_manager_gnocchi = {
        'username': 'Gnocchi',
        'password': 'password',
        'contact_data': 'gnocchi_werk@gmx.de',
    }

    user_data_administrator_caro = {
        'username': 'Caro',
        'password': 'password',
        'contact_data': 'bitte_toete_mich@gmx.de',
        'year_of_birth': '1999',
        'is_superuser': True
    }

    store_data_ikae = {
        "address": "Storestr. 1",
        "phone_number": "012345",
        "email": "pse_email@gmx.de",
        "name": "IKAE",
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

    store_data_graphs = {
        "address": "Str. 12",
        "phone_number": "012345",
        "email": "pse_email@gmx.de",
        "name": "Graphen",
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

    store_data_test = {
        "region": "Karlsruhe",
        "address": "Klagen-Str. 12",
        "phone_number": "0152553222",
        "email": "janderda@web.de",
        "name": "Mutter",
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
        'name': ['Fast'],
        'description': ['not yet furious']
    }

    bike_data_bike2 = {
        'name': ['not'],
        'description': ['not almost sounds like dot']
    }

    bike_data_bike3 = {
        'name': ['furious'],
        'description': ['really angry possibly about to explode']
    }

    bike_data_test = {
            'name': 'KI',
            'description': 'gki ist ne Blöde!',
    }

    equipment_data_onion = {
        'equipment': 'Onion'
    }

    equipment_data_gunde = {
        'equipment': 'Gudelgunde von Gonde'
    }

    booking_data = {
        "begin": "2123-10-02",
        "end": "2123-10-03",
        "equipment": []
    }

    booking_data_with_equipment = {
        "begin": "2123-10-04",
        "end": "2123-10-05",
        "equipment": ["Tarp", "Charger"]
    }

    booking_data_test = {
        "begin": "2124-01-12",
        "end": "2124-01-13",
    }

    booking_data_test_with_equipment = {
        "begin": "2124-01-14",
        "end": "2124-01-15",
        "equipment": ["Tarp", "Charger"]
    }

    regex_non_natural_numbers = r'a+^(?!0*[1-9]+\d*$)\d+$'

    def validate_mail(self, template_location, index, *args):
        self.assertGreaterEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[index]
        keys = []
        subject = ''
        if template_location == "email_templates/BookingMailTemplate.html":
            subject = f"Deine Buchung von {args[1]} bei {args[2]} von {args[3]} bis {args[4]}"
            keys = ['username', 'bike_name', 'store_name', 'start_date', 'end_date', 'booking_equipment', 'store_address', 'store_phone_number', 'store_email', 'spenden_link', 'lastenkarle_contact_data']
        if template_location == "email_templates/AdminUserWarningNotification.html":
            subject = f"Benutzer {args[0]} wurde ermahnt"
            keys = ['username', 'store_name', 'store_address', 'store_phone_number', 'store_email', 'comment']
        if template_location == "email_templates/BikeDropOffConfirmation.html":
            subject = f"Statuswechsel deiner Buchung: Lastenrad {args[1]} wurde zurückgegeben"
            keys = ['username', 'bike_name', 'store_name', 'store_address', 'store_phone_number', 'store_email']
        if template_location == "email_templates/BikePickUpConfirmation.html":
            subject = f"Statuswechsel deiner Buchung: Lastenrad {args[1]} wurde abgeholt"
            keys = ['username', 'bike_name', 'store_name', 'store_address', 'store_phone_number', 'store_email']
        if template_location == "email_templates/CancellationConfirmation.html":
            subject = f"Stornierung deiner Buchung von {args[3]} bis {args[4]}"
            keys = ['username', 'bike_name', 'store_name', 'start_date', 'end_date']
        if template_location == "email_templates/CancellationThroughStoreConfirmation.html":
            subject = f"Stornierung deiner Buchung von {args[3]} bis {args[4]}"
            keys = ['username', 'bike_name', 'store_name', 'start_date', 'end_date']
        if template_location == "email_templates/UserBannedMail.html":
            subject = "Statuswechsel deines Accounts: Du wurdest gebannt"
            keys = ['username', 'lastenkarle_contact_data']
        if template_location == "email_templates/UserRegisteredConfirmation.html":
            subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
            keys = ['username', 'registration_link']
        if template_location == "email_templates/UserVerifiedConfirmation.html":
            subject = "Statuswechsel deines Accounts: Du bist verifiziert"
            keys = ['username', 'lastenkarle_contact_data']
        if template_location == "email_templates/EmailChangedTemplate.html":
            subject = "Dein Account bei Lastenkarle: Bitte bestätige deine E-Mail"
            keys = ['username', 'verification_link']
        if template_location == "email_templates/UserWarning.html":
            subject = "Statuswechsel deines Accounts: Du wurdest ermahnt"
            keys = ['username', 'store_name', 'comment', 'store_address', 'store_phone_number', 'store_email']
        context = {key: value for key, value in zip(keys, args)}
        self.assertEqual(sent_mail.subject, subject)
        expected_html_content = render_to_string(template_location, context)
        self.assertHTMLEqual(sent_mail.body, expected_html_content)

    def make_request(self, url=None, data=None, **extra):
        if url is None:
            url = self.url_template
        if self.http_method == 'GET':
            return self.client.get(url, data, **extra)
        if self.http_method == 'POST':
            return self.client.post(url, data, **extra)
        if self.http_method == 'PATCH':
            return self.client.patch(url, data, **extra)
        if self.http_method == 'DELETE':
            return self.client.delete(url, data, **extra)

    def get_copy(self, dict):
        return copy.deepcopy(dict)

    def get_login_data_from_user_data(self, user_data):
        return {'username': user_data.get('username'), 'password': user_data.get('password')}

    def login_user(self, user, user_data):
        request = self.factory.generic('POST', '/', data=self.get_login_data_from_user_data(user_data))
        request.session = SessionStore(session_key='a')
        request.user = AnonymousUser()
        force_authenticate(request, user=user)
        return LoginView().as_view()(request)

    def create_user_obtain_token(self, user_data):
        user = User.objects.create_user(**user_data)
        return user, self.login_user(user, user_data).data.get('token')

    def create_store(self, store_data, region_name):
        region = Region.objects.get(name=region_name)
        store_data["region"] = region
        store = Store.objects.create(**store_data)
        store_flag = User_Flag.custom_create_store_flags(store)
        store.store_flag = store_flag
        store.save()
        return store

    def create_bike_of_store(self, store, bike_data):
        with open(self.image_path_bike, 'rb') as image_file:
            image = SimpleUploadedFile("bike_image.jpg", image_file.read(), content_type="image/jpg")
        bike = Bike.objects.create(name=bike_data.get('name')[0], description=bike_data.get('description')[0],
                                   image=image,
                                   store=store)
        Availability.create_availability(store, bike)
        return bike

    def create_booking_of_bike_with_flag(self, user, bike, booking_status_label, begin, end):
        booking_string = generate_random_string(5)
        booking = Booking.objects.create(
            user=user, bike=bike, string=booking_string,
            begin=datetime.strptime(begin, '%Y-%m-%d').date(),
            end=datetime.strptime(end, '%Y-%m-%d').date())
        booking.booking_status.add(Booking_Status.objects.filter(status=booking_status_label)[0].pk)
        if booking_status_label == 'Internal usage':
            booking.status.add(Booking_Status.objects.filter(status='Booked')[0].pk)
        booking_status_labels_split = ['Booked', 'Internal usage', 'Picked up']
        if booking_status_label in booking_status_labels_split:
            split_availabilities_algorithm(booking)
        return booking

    def add_equipment_to_bike(self, bike, equipment):
        bike.bike_equipment.add(Equipment.objects.get(equipment=equipment))
        bike.save()

    def add_flag_to_user(self, user, flag_name):
        user.user_flags.add(User_Flag.objects.get(flag=flag_name).pk)
        if flag_name.startswith('Banned') and user.is_active is True:
            user.is_active = False
            user.save()
        if flag_name.startswith('Store:') and user.is_staff is False:
            user.is_staff = True
            user.save()
        if flag_name.startswith('Administrator') and user.is_superuser is False:
            user.is_superuser = True
            user.save()

    def verify_user(self, user):
        user.user_flags.add(User_Flag.objects.get(flag='Verified'))
        user.verification_string = None
        user.save()

    def delete_user(self, user):
        user.anonymize().save()
        user.user_flags.clear()
        user.save()

    def random_exclude_key_value_pairs(self, data, num_to_exclude):
        keys_to_exclude = random.sample(list(data.keys()), num_to_exclude)
        ret_data = {key: data[key] for key in data if key not in keys_to_exclude}
        return ret_data

    def random_number_not_in_id_set(self, class_name):
        if class_name in globals() and isinstance(globals()[class_name], type):
            retrieved_class = globals()[class_name]
            id_list = []
            maximum = 0
            i = maximum
            for obj in retrieved_class.objects.all():
                id_list.append(obj.pk)
                if obj.pk > maximum:
                    maximum = obj.pk
            return random.randint(17*maximum, 20*maximum)

    def generate_random_regex_string(self, regex):
        #TODO actually use the regex
        length = random.randint(2, 5)
        chars = string.ascii_letters + string.digits
        rand_string = ''.join(random.choice(chars) for _ in range(length))
        return rand_string + 'a'

    def assign_values_to_placeholder_regex(self, regex, url_string):
        replaced_string = url_string
        placeholders = re.findall(r'\{(\w*)}', replaced_string)
        values = {
            placeholder: self.generate_random_regex_string(regex)
            for placeholder in placeholders
        }
        return re.sub(r'\{(\w*)}', lambda match: values.get(match.group(1), match.group(0)), replaced_string)

    def assign_values_to_placeholder(self, url_string, *args):
        if '{}' not in url_string:
            return url_string
        replaced_string = url_string
        for arg in args:
            replaced_string = replaced_string.replace('{}', str(arg), 1)
        return replaced_string

    def setUp(self, url, http_method, fields_to_include=None, fields_classes=None):
        super(APITestCase, self).setUp()
        if url is None:
            self.url_template = None
        else:
            self.url_template = url
        if http_method is None:
            self.http_method = None
        else:
            self.http_method = http_method
        if fields_to_include is None:
            self.fields_to_include = None
        else:
            self.fields_to_include = fields_to_include
        if fields_classes is None:
            self.fields_classes = None
        else:
            self.fields_classes = fields_classes
        self.client = APIClient()
        # initializing default test stores and bikes
        self.store_ikae = self.create_store(self.store_data_ikae, 'Karlsruhe')
        self.store_graphs = self.create_store(self.store_data_graphs, 'Bruchsal')
        self.bike1_of_ikae = self.create_bike_of_store(self.store_ikae, self.bike_data_bike1)
        self.bike2_of_ikae_with_equipment = self.create_bike_of_store(self.store_ikae, self.bike_data_bike2)
        self.bike1_of_graphs = self.create_bike_of_store(self.store_graphs, self.bike_data_bike3)
        self.add_equipment_to_bike(self.bike2_of_ikae_with_equipment, 'Tarp')
        self.bike_for_deletion = self.create_bike_of_store(self.store_ikae, self.bike_data_test)
        # initializing default test users
        self.user_customer_taylor, self.user_customer_taylor_token = self.create_user_obtain_token(
            self.user_data_customer_taylor)
        self.user_customer_wildegard, self.user_customer_wildegard_token = self.create_user_obtain_token(
            self.user_data_customer_wildegard)
        self.verify_user(self.user_customer_wildegard)
        self.user_manager_store_koeri, self.user_manager_store_koeri_token = self.create_user_obtain_token(
            self.user_data_store_manager_koeri)
        self.verify_user(self.user_manager_store_koeri)
        self.add_flag_to_user(self.user_manager_store_koeri, self.store_ikae.store_flag.flag)
        self.user_manager_store_gnocchi, self.user_manager_store_gnocchi_token = self.create_user_obtain_token(
            self.user_data_store_manager_gnocchi)
        self.verify_user(self.user_manager_store_gnocchi)
        self.add_flag_to_user(self.user_manager_store_gnocchi, self.store_graphs.store_flag.flag)
        self.user_administrator_caro, self.user_administrator_caro_token = self.create_user_obtain_token(
            self.user_data_administrator_caro)
        self.verify_user(self.user_administrator_caro)
        # initializing bookings
        self.booking_of_caro = self.create_booking_of_bike_with_flag(self.user_administrator_caro, self.bike1_of_graphs,
                                                                     'Booked', '2123-10-08', '2123-10-11')
        self.booking_picked_up = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike1_of_ikae,
                                                                       'Picked up', '2123-10-01', '2123-10-02')
        self.booking_cancel = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike1_of_ikae,
                                                                    'Booked', '2223-10-08', '2123-10-10')
        self.booking_returned = self.create_booking_of_bike_with_flag(self.user_customer_taylor, self.bike1_of_ikae,
                                                                      'Returned', '2223-10-15', '2123-10-17')
        self.taylor_bookings = [self.booking_picked_up, self.booking_cancel, self.booking_returned]

    def tearDown(self):
        bikes = glob.glob(os.path.join(BASE_DIR, 'media/bikes/', '*.jpg'))
        for bike in bikes:
            os.remove(bike)
        qr_codes = glob.glob(os.path.join(BASE_DIR, 'media/qr-codes/', '*.png'))
        for qr_code in qr_codes:
            os.remove(qr_code)
        forms = glob.glob(os.path.join(BASE_DIR, 'media/pdf/', '*.pdf'))
        for pdf in forms:
            os.remove(pdf)
        super(APITestCase, self).tearDown()

    def invalid_url_params(self, user_token, number_of_combinations, regex, **extra):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        for i in range(1, number_of_combinations):
            response = self.make_request(url=self.assign_values_to_placeholder_regex(regex, self.url_template), **extra)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def invalid_permissions(self, user_token, path=None, data=None, **extra):
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        if path is None:
            path = self.url_template
        response = self.make_request(url=path, data=data, **extra)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        if not user_token == ' ':
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
            response = self.make_request(url=path, data=data, **extra)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def serialize_booking_with_relations(self, booking_instance):
        serializer = BookingSerializer(booking_instance)
        return serializer.data

    def serialize_user_with_relations(self, user_instance):
        serializer = UserSerializer(user_instance)
        return serializer.data

    def serialize_bike_with_relations(self, bike_instance):
        serializer = BikeSerializer(bike_instance)
        return serializer.data

    def serialize_store_with_relations(self, store_instance):
        serializer = StoreSerializer(store_instance)
        return serializer.data

    def validate_integrity(self, response_data, db_data):
        ret = self._validate_integrity(response_data, db_data)
        if isinstance(ret, bool):
            self.assertTrue(False)

    def validate_integrity_list(self, db_data, url):
        response = self.make_request(url=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.validate_integrity({d['id']: d for d in response_data},
                                {d['id']: d for d in db_data})

    def _validate_integrity(self, response_data, db_data, path=""):
        differences = {}

        # Flag to track if all keys from response_data were found in db_data
        all_keys_found = True

        # Iterate over keys in the response data
        for key, value in response_data.items():
            full_key_path = f"{path}.{key}" if path else key

            # Check if the key exists in the db_data
            if key in db_data:
                # If the value is a dictionary, recursively compare it
                if isinstance(value, dict) and isinstance(db_data[key], dict):
                    nested_differences = self._validate_integrity(value, db_data[key], path=full_key_path)
                    differences.update(nested_differences)
                # If the value is a list, iterate over its elements
                elif isinstance(value, list) and isinstance(db_data[key], list):
                    if len(value) != len(db_data[key]):
                        self.assertTrue(False, f"Length of lists at {full_key_path} differs")
                    for index, (elem_resp, elem_db) in enumerate(zip(value, db_data[key])):
                        nested_differences = self._validate_integrity(elem_resp, elem_db,
                                                                     path=f"{full_key_path}[{index}]")
                        differences.update(nested_differences)
            else:
                # If the key doesn't exist in the db_data, set all_keys_found to False and break the loop
                all_keys_found = False
                break

        # If not all keys from response_data were found, return False
        if not all_keys_found:
            return False

        return differences
