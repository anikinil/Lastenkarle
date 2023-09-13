from configs.global_variables import lastenkarle_logo_url
from django.test import TestCase
from rest_framework.test import APIClient


class GlobalVariableTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_logo_exists(self):
        response = self.client.get(lastenkarle_logo_url)
        print(response)
        self.assertEqual(True, False)