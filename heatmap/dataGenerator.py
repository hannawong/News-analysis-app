#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
heatmapData:[{lng: 116.191031, lat: 39.988585, count: 98} , ......]
双引号的json格式 数据范围、in中国[不提供审查,大约为：经度lng 73.66至135.05,纬度lat 3.86至53.55] count大约0--100
中国城市和经纬度的对应表 echarts-china-cities-pypkg，echarts-china-provinces-pypkg
如果只到省级 显示省会； 看起来是到不了区了？

1. 获取一份中国城市地点表，按照到区的地点进行查找 【eg 北京海淀区，116.30，39.95】
2. 在新闻数据库中【已经标注了舆情聚类的事件中】索引  **Parameters：**cluster_id: 新闻簇的编号，[0,20)的整数；
3. count = f(文章中提及的次数, 提及文章数)
4. 选做--查找结果存档，记录截止日期、事件   读写json文件or数据库 形式 --因而可以增量式进行

参数*2
 1-事件：default=all 某件事 or  所有事
 2-时间：[begin, end]  default=yesterday? 不同截止日期查询结果不同，可以显示趋势


lnglat
# {('北京市', '', ''): (116.39564503787867, 39.92998577808024),
 ('北京市', '北京市', ''): (116.39564503787867, 39.92998577808024),
 ('北京市', '北京市', '东城区'): (116.42188470126446, 39.93857401298612)}

# 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空
todo 看地点提取结果而定？--may 改cvs 省级经纬==省会经纬  重复值处理—丢弃省份or存入时即处理？ 目前只能丢弃省份 or 改数据库 

"""
import datetime

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxswl.settings")
django.setup()  # 为了正确使用数据库
from news.models import Articles
from heatmap.models import HeatMapData

import re
import json
from heatmap.data.lnglatDict import lnglat
from chinese_province_city_area_mapper.transformer import CPCATransformer

# (省名, 市名, 区名) -> 出现次数
from collections import Counter

punctuationPattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|【|】|·|！| |…|（|）|‘|’|“|”'


class DotData:
    """地图上一个点和它的热度"""

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


text1 = "云南封禁be，北京好嘛在三峡骑行，北京好嘛在三峡骑行，北京好嘛在三峡骑行，北京好嘛在三峡骑行，他第一次感受到，‘郦道元’“东三峡巫峡长，猿鸣三声泪沾裳”原来就是这样的景致。在南京，为了坐上人生第一次渡轮，他在码头长凳上过夜。在凉都利川，他发现9月暑天早晨的气温可以低到14度，冻得他用衣服包起了手。 "


def location_count(oriText: str):  # 原文进入
    # 按标点拆分成list
    clauseList = re.split(punctuationPattern, oriText)
    # 在list中得到地点   地点处理--直接补全到default的3级获取经纬度
    locationDF = CPCATransformer().transform(clauseList)  # dataFrame
    # 地点加入计数
    locationList = [repr(tuple(x)) for x in locationDF.values]
    dict2 = dict(Counter(locationList))
    dict2.pop("('', '', '')",0)
    return dict2
    # locationCounter.update(locationList)


def setloc_for_item(article):
    body = article.body  # text
    locdata = repr(location_count(body))
    article.keywords += "@@@" + locdata  # 分割符号
    article.save()


def setloc_in_articles():  # 对数据库每一行进行地点筛选  ## 初期初始化好所有数据 按照日期计入
    rollnews = Articles.objects.filter()
    for article in rollnews:
        totdata = article.keywords
        list = totdata.split("@@@")
        if len(list) > 1:  # had done
            continue
        setloc_for_item(article)


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


def setloc_in_heatmapdb():  # 按照日期、聚类存储到我的数据库
    # 遍历范围内的time, cluster_id
    for cluster_id in range(0,20):  # [0,19] # 日期范围，目前只提供从"2020-10-13"到昨天的数据
        d_beign = datetime.datetime.strptime("2020-10-13", '%Y-%m-%d')
        inc = datetime.timedelta(days=1)
        now = datetime.datetime.now()  # or end= now-inc
        d_end = datetime.datetime.strptime("2020-10-20", '%Y-%m-%d')
        delta = d_end - d_beign
        for i in range(0, delta.days + 1):  # [begin,end]
            date = d_beign.strftime('%Y-%m-%d')
            d_beign += inc
            readby_time_cluster(date,cluster_id)


def lnglat_data_get(locationCounter):  # 将计数后的地点转化为经纬度
    lnglatData = []
    for (pos, count) in locationCounter.items():
        pt = lnglat.get(pos)
        if pt != None:
            lnglatData.append(DotData(pt[0], pt[1], count).obj())
    return lnglatData


def data_generator( cluster_id= 1 ,starttime= "2020-10-13",endtime= "2020-10-13"):
    # 简单示例 
    locationCounter = Counter()  # ('北京市', '北京市', ''): 1, ('北京市', '北京市', '东城区'): 1} # they are different locations
    day = "2020-10-13"
    cluster_id = 1  # 0-19
    rollnews = HeatMapData.objects.filter(cluster_id=cluster_id,time__contains=day) # 仅一个条目
    for article in rollnews:
        # print(article.time,article.cluster_id,article.locdict)
        locationCounter.update(json.loads(article.locdict))

    return lnglat_data_get(locationCounter)


if __name__ == '__main__':
    # set loc for every item in articles-database
    setloc_in_articles()
    print("set loc in Articles-database, done")
    setloc_in_heatmapdb()
    print("collect locs into HeatMapData-database, done")
    # check
    rollnews = HeatMapData.objects.filter()
    for article in rollnews:
        print(article.time,article.cluster_id,article.locdict)
