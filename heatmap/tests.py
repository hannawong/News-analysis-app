from django.test import TestCase
from .dataGenerator import data_generator, string2timestamp,timestamp2date


# Create your tests here.
class TestHeatmap(TestCase):
    def test_get(self):
        def get_heatmap_rsp(cluster_id =6,starttime ='2020-10-13 0:43:37',endtime='2020-10-29 23:43:37' ):
            startt = string2timestamp(starttime)
            endt = string2timestamp(endtime)
            response = self.client.get('/heatmap/heatmap/{}/{}/{}'.format(cluster_id, startt, endt))
            return response

        def get_heatmap_db(cluster_id =6,starttime ='2020-10-13',endtime='2020-10-29' ): ## 无审查，直接调bd的函数
            import datetime
            d_begin = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            d_end = datetime.datetime.strptime(endtime, '%Y-%m-%d')
            heatmap_db = data_generator(cluster_id, d_begin, d_end)
            return heatmap_db

        # test case 1 all with default args
        response = get_heatmap_rsp()
        print(response.json()['data'])
        heatmap_db = get_heatmap_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], heatmap_db)

        # fail cases
        response = self.client.get('/heatmap/heatmap/{}/{}/{}'.format("cluster_id", 1602521017, 1602521017))
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/heatmap/heatmap/{}/{}/{}'.format(5, '160252adwd1017', 1602521017))
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/heatmap/heatmap/{}/{}/{}'.format(5, 1602521017, 16025))
        self.assertEqual(response.status_code, 400)
