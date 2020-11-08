from django.test import TestCase
import requests

# Create your tests here.
class TestNews(TestCase):
    def test_get(self):
        def get_search_news(q=None, time_from=None, time_to=None, from_index=None):
            para_list = []
            if q is not None:
                para_list.append("q=" + q)
            if time_from is not None:
                para_list.append("from=" + time_from)
            if time_to is not None:
                para_list.append("to=" + time_to)
            if from_index is not None:
                para_list.append("start_index=" + from_index)

            if para_list.__len__ == 0:
                para = ""
            else:
                para = ("?" + "&".join(para_list))

            response = requests.get('http://62.234.121.168:30000/news/search/' + para)
            return response

        def get_search_date_cluster_info(q=None):
            para_list = []
            if q is not None:
                para_list.append("q=" + q)

            if para_list.__len__ == 0:
                para = ""
            else:
                para = ("?" + "&".join(para_list))

            response = requests.get('http://62.234.121.168:30000/news/search_date_cluster_info/' + para)
            return response

        # test case 1 with default args
        response = get_search_news()
        self.assertEqual(response.status_code, 200)
