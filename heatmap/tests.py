from django.test import TestCase
from .dataGenerator import dataGenerator

# Create your tests here.
class TestHeatmap(TestCase):
    def test_get(self):
        print("hello")
        response_data =  dataGenerator()
        response = self.client.get("/heatmap/heatmap")
        print("hello")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], response_data)
