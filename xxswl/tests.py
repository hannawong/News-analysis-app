
from django.test import TestCase
from news.models import Articles,WeiboHot
class TestMeetingEndpoint(TestCase):
    def test_get(self):
        offset, limit = 0, 50
        response_data = [
                {
                    'id': msg.id,
                    'title': msg.title.split("@")[0],
                    'hot': msg.hot,
                    'url':msg.title.split('@')[1]
                }
                for msg in WeiboHot.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ]
        response = self.client.get("/news/index0")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        print(response_data[0:40])
        self.assertEqual(response.json()['data'][0:40], response_data[0:40])
