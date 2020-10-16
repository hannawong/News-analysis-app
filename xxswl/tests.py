
from django.test import TestCase
import re,jieba
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
        self.assertEqual(response.json()['data'][0:40], response_data[0:40])

    def test_get_wordcloud(self):
       response = self.client.get("/news/wordcloud/2/5")
       self.assertEqual(response.status_code,200)
       word_dic={}
       for news in Articles.objects.filter(cluster_id=2).order_by('-pk'):
           text = news.title + " " + news.body
           text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
           seg_word = list(jieba.cut(text))
           for word in seg_word:
               if (len(word) == 1):
                   continue
               if (word in word_dic.keys()):
                   word_dic[word] += 1
               else:
                   word_dic[word] = 1
       L = sorted(word_dic.items(), key=lambda item: item[1], reverse=True)
       L = L[:int(5)]
       dic = {}
       for l in L:
           dic[l[0].encode("utf-8").decode("utf-8")] = l[1]
       self.assertEqual(response.json()['data'], dic)