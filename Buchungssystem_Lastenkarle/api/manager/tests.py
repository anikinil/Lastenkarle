from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from knox.models import AuthToken

from db_model.models import Store, Bike, Equipment, User_Status, User


class RegisteredEquipmentTestCase(TestCase):
    def setUp(self):
        # Create a test user with the necessary permissions
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'contact_data': 'wilde.gard@gmx.de',
            'year_of_birth': '1901'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        # create User
        self.user = User.objects.create_user(**self.user_data)
        # login user
        response = self.client.post("/api/user/v1/login", self.login_data)
        # Parse the response content to get the token
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get('token', None)
        self.user.is_staff = True
        self.verified = User_Status.objects.create(user_status='Verified')
        self.user.user_status.add(self.verified)
        self.user.save()

        # Create a test store
        self.store = Store.objects.create(name='Test Store')

        # Create a bike associated with the store
        self.bike = Bike.objects.create(store=self.store, name='BoomBike', description='Explodiert')

        # Create equipment for bike
        self.equipment1 = Equipment.objects.create(equipment='Klingel')
        self.equipment2 = Equipment.objects.create(equipment='Schloss')

        # Add the equipment items to the bike's equipment field
        self.bike.equipment.add(self.equipment1, self.equipment2)
    def test_registered_equipment_api(self):
        # Set up the request headers with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Make a GET request to the API endpoint
        response = self.client.get('/api/manager/v1/equipment/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data is a list
        self.assertIsInstance(response.data, list)

        self.assertEqual(len(response.data), 2)  # We have to equipment items in the set up
        self.assertEqual(response.data[0]['equipment'], 'Klingel')
        self.assertEqual(response.data[1]['equipment'], 'Schloss')
