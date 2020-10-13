'''
Test suite for meeting
'''

from django.test import TestCase
from news.models import Articles
class TestMeetingEndpoint(TestCase):
    def setUp(self):
        Articles.objects.create(url="", title="abc", time="2020-10-08 19:41:00",author="Alice",body="dfg")

    def test_get(self):
        offset, limit = 0, 20
        response_data = [
                {
                    'url': msg.url,
                    'title': msg.title,
                    'time': msg.time,
                    'author': msg.author,
                    'body':msg.body
                }
                for msg in Articles.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ]
        response = self.client.get("/news/index0")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        print(response_data)
        self.assertEqual(response.json()['data'], response_data)