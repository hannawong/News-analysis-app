#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime
from heatmap.re_funcs import punc_clauseList

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")
django.setup()  # Ϊ����ȷʹ�����ݿ�
from news.models import Articles
from heatmap.models import HeatMapData


import json
from heatmap.data.lnglatDict import lnglat
from chinese_province_city_area_mapper.transformer import CPCATransformer

# (ʡ��, ����, ����) -> ���ִ���
from collections import Counter

class DotData:
    def __init__(self, lng, lat, count):
        self.lng = lng
        self.lat = lat
        self.count = count

    def obj(self):
        if self.count < 0:
            self.count = 0
        if self.count > 100:
            self.count = 100
        return {"lng": self.lng, "lat": self.lat, "count": self.count}


def location_count(oriText: str):  # ԭ�Ľ���
    # ������ֳ�list
    clauseList = punc_clauseList(oriText)
    # ��list�еõ��ص�   �ص㴦��--ֱ�Ӳ�ȫ��default��3����ȡ��γ��
    locationDF = CPCATransformer().transform(clauseList)  # dataFrame
    # �ص�������
    locationList = [repr(tuple(x)) for x in locationDF.values]
    dict2 = dict(Counter(locationList))
    dict2.pop("('', '', '')",0)
    return dict2
    # locationCounter.update(locationList)


def setloc_for_item(article):
    body = article.body  # text
    locdata = repr(location_count(body))
    article.keywords += "@@@" + locdata  # �ָ����
    article.save()


def setloc_in_articles():  # �����ݿ�ÿһ�н��еص�ɸѡ  ## ���ڳ�ʼ������������ �������ڼ���
    rollnews = Articles.objects.filter()
    for article in rollnews:
        totdata = article.keywords
        list = totdata.split("@@@")
        if len(list) > 1:  # had done
            continue
        setloc_for_item(article)
        print(article.id)


def readby_time_cluster(day, cluster_id):
    rollnews = Articles.objects.filter(cluster_id=cluster_id,time__contains=day)
    totcounter = Counter()
    for article in rollnews:
        list = article.keywords.split("@@@")
        if len(list) <= 1:  # not done
            setloc_for_item(article)
            newlist = article.keywords.split("@@@")
            list.append(newlist.pop())
        locdict = json.loads(list.pop())
        totcounter.update(locdict)
    # write into my database
    locdict = repr(dict(totcounter))
    heatMapData = HeatMapData(time=day, cluster_id=cluster_id,locdict=locdict)
    heatMapData.save()


def setloc_in_heatmapdb():  # �������ڡ�����洢���ҵ����ݿ�
    # ������Χ�ڵ�time, cluster_id
    for cluster_id in range(0,20):  # [0,19] # ���ڷ�Χ��Ŀǰֻ�ṩ��"2020-10-13"�����������
        d_beign = datetime.datetime.strptime("2020-10-13", '%Y-%m-%d')
        inc = datetime.timedelta(days=1)
        now = datetime.datetime.now()  # or end= now-inc
        d_end = datetime.datetime.strptime("2020-10-29", '%Y-%m-%d')
        delta = d_end - d_beign
        for i in range(0, delta.days + 1):  # [begin,end]
            date = d_beign.strftime('%Y-%m-%d')
            d_beign += inc
            readby_time_cluster(date,cluster_id)
            print(date,cluster_id)


def lnglat_data_get(locationCounter):  # ��������ĵص�ת��Ϊ��γ��
    lnglatData = []
    for (pos, count) in locationCounter.items():
        pt = lnglat.get(pos)
        if pt != None:
            lnglatData.append(DotData(pt[0], pt[1], count).obj())
    return lnglatData


def data_generator(cluster_id, d_begin,d_end):
    locationCounter = Counter()  # ('������', '������', ''): 1, ('������', '������', '������'): 1} # they are different locations
    inc = datetime.timedelta(days=1)
    delta = d_end - d_begin
    for i in range(0, delta.days + 1):  # [begin,end]
        day = d_begin.strftime('%Y-%m-%d')
        d_begin += inc
        rollnews = HeatMapData.objects.filter(cluster_id=cluster_id,time__contains=day)
        for article in rollnews:
            # print(article.time,article.cluster_id,article.locdict)
            locationCounter.update(json.loads(article.locdict))
    return lnglat_data_get(locationCounter)


def data_generator_ids(idlist):  # for ids input
    # idlst =[24,25,26,27]
    locationCounter = Counter()
    for id in idlist:  # [begin,end]
        rollnews = HeatMapData.objects.filter(id=id)
        for article in rollnews:
            # print(article.time,article.cluster_id,article.locdict)
            locationCounter.update(json.loads(article.locdict))
    return lnglat_data_get(locationCounter)


def init_data():
    # set loc for every item in articles-database
    setloc_in_articles()
    print("set loc in Articles-database, done")
    setloc_in_heatmapdb()
    print("collect locs into HeatMapData-database, done")



# '2015-08-28 16:43:37.283' --> 1440751417.283
# ���� '2015-08-28 16:43:37' --> 1440751417.0
def string2timestamp(strValue):
    import time
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        print(e)
        return 0


import time
# use time.localtime
def timestamp2date(timestamp):
    return datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(timestamp)),'%Y-%m-%d').date() # datetime.datetime.fromtimestamp(timeStamp).date()

if __name__ == '__main__':
    # now's starttime and endtime
    print(location_count("test , test, test..."))

    print(string2timestamp('2020-10-29 23:43:37'))
    print(string2timestamp('2020-10-13 0:43:37'))

    # init_data()
    # check
    rollnews = HeatMapData.objects.filter()
    for article in rollnews:
        print(article.time,article.cluster_id,article.locdict)
