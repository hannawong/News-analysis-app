#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
heatmapData:[{lng: 116.191031, lat: 39.988585, count: 98} , ......] 双引号的json格式 数据范围、in中国[不提供审查,大约为：经度lng 73.66至135.05,纬度lat 3.86至53.55] count大约0--100
中国城市和经纬度的对应表 echarts-china-cities-pypkg，echarts-china-provinces-pypkg
如果只到省级 显示省会； 看起来是到不了区了？

1. 获取一份中国城市地点表，按照到区的地点进行查找 【eg 北京海淀区，116.30，39.95】
2. 在新闻数据库中【已经标注了舆情聚类的事件中】索引  **Parameters：**cluster_id: 新闻簇的编号，[0,20)的整数；
3. count = f(文章中提及的次数, 提及文章数)
4. 选做--查找结果存档，记录截止日期、事件   读写json文件or数据库 形式 --因而可以增量式进行

参数*2
 1-事件：default=all 某件事 or  所有事
 2-时间：[begin, end]  default=yesterday? 不同截止日期查询结果不同，可以显示趋势


lnglat = {}
# {('北京市', '', ''): (116.39564503787867, 39.92998577808024), ('北京市', '北京市', ''): (116.39564503787867, 39.92998577808024), ('北京市', '北京市', '东城区'): (116.42188470126446, 39.93857401298612)}

# 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空

"""
import re
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


text1 = "云南封禁be，北京好嘛在三峡骑行，北京好嘛在三峡骑行，北京好嘛在三峡骑行，北京好嘛在三峡骑行，他第一次感受到，‘郦道元’“东三峡巫峡长，猿鸣三声泪沾裳”原来就是这样的景致。在南京，为了坐上人生第一次渡轮，他在码头长凳上过夜。在凉都利川，他发现9月暑天早晨的气温可以低到14度，冻得他用衣服包起了手。"


# (省名, 市名, 区名) -> (经度，纬度)
lnglat = {}
def loadLnglatDict() :
    import csv
    with open('pca.csv', 'r', encoding='utf8') as f:
        pca_csv = csv.DictReader(f)
        for record_dict in pca_csv:
            lnglat[(record_dict['sheng'], record_dict['shi'], record_dict['qu'])] = \
                (float(record_dict['lng']),float(record_dict['lat']))

# (省名, 市名, 区名) -> 出现次数
from collections import Counter
locationCounter = Counter() # ('北京市', '北京市', ''): 1, ('北京市', '北京市', '东城区'): 1} # they are different locations

def locationCount(oriText: str):  # 原文进入
    # 按标点拆分成list
    clauseList = re.split(punctuationPattern, oriText)
    # 在list中得到地点   地点处理--直接补全到default的3级获取经纬度
    from chinese_province_city_area_mapper.transformer import CPCATransformer
    locationDF = CPCATransformer().transform(clauseList) # dataFrame
    # 地点加入计数
    locationList = [tuple(x) for x in locationDF.values]
    locationCounter.update(locationList)

def heatmapDataGet():
    heatmapData = []
    for (pos,count) in locationCounter.items():
        pt = lnglat.get(pos)
        if pt != None:
            heatmapData.append(DotData(pt[0],pt[1],count).obj())
    return heatmapData


def dataGenerator():
    # not from database
    loadLnglatDict()
    locationCounter[('北京市', '北京市', '')] =  4
    locationCount(text1)  # 对数据库每一行进行
    # print(locationCounter)
    return heatmapDataGet()

if __name__ == '__main__':
    print(dataGenerator())
