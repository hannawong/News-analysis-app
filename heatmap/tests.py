from django.test import TestCase
from .dataGenerator import data_generator

# Create your tests here.
class TestHeatmap(TestCase):
    def test_get(self):
        print("hello")
        response_data =  data_generator()
        response = self.client.get('/heatmap/heatmap/1/"2020-10-13"/"2020-10-13"')
        print("hello")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], response_data)
