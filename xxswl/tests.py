
from django.test import TestCase
import re,jieba

from news.models import Articles,WeiboHot,WeiboSocialEvents
from news.inverted_index.search import wordcloud
from news.inverted_index.search import search
class TestMeetingEndpoint(TestCase):
    def test_get_weibohot(self):
        response_data = [
            {
                'id': msg.id,
                'title': msg.title.split("@")[0],
                'hot': msg.hot,
                'url': msg.title.split("@")[1]
            }
            for msg in WeiboHot.objects.all()
        ]
        response = self.client.get("/news/index0")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'][0:40], response_data[0:40])

    def test_get_weibo_socialevent(self):
        response_data = [
            {
                'id': msg.id,
                'title': msg.title.split("@")[0],
                'url': msg.title.split("@")[1]
            }
            for msg in WeiboSocialEvents.objects.all()
        ]
        response = self.client.get("/news/index1")
        print(response.json()['data'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], response_data)

    def test_get_timeline(self):
        news_list = search("疫情", 0, 9999999999999999)
        response = self.client.get("/news/timeline/疫情/0/9999999999999999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], news_list)

    def test_get_wordcloud(self):
       response = self.client.get("/news/wordcloud/2/5")
       self.assertEqual(response.status_code,200)
       dic=wordcloud(2,5)
       self.assertEqual(response.json()['data'], dic)

    '''
        def test_get_latest_news(self):
            length = len(Articles.objects.all())
            response_data = [
                    {
                        'title': msg.title,
                        'url': msg.url,
                        'time': msg.time
                    }
                    for msg in Articles.objects.all().order_by('time')[length - 50:length]
                ]
            response = self.client.get("/news/index2")
            print(response.json()['data'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['data'], response_data)
    '''