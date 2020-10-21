#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
heatmapData:[{lng: 116.191031, lat: 39.988585, count: 98} , ......] 双引号的json格式 数据范围、in中国[不提供审查,大约为：经度lng 73.66至135.05,纬度lat 3.86至53.55] count大约0--100
中国城市和经纬度的对应表 echarts-china-cities-pypkg，echarts-china-provinces-pypkg

1. 获取一份中国城市地点表，按照到区的地点进行查找 【eg 北京海淀区，116.30，39.95】  
2. 在新闻数据库中【已经标注了舆情聚类的事件中】索引  
3. count = f(文章中提及的次数, 提及文章数)
4. 选做--查找结果存档，记录截止日期、事件   读写json文件or数据库 形式 --因而可以增量式进行 

参数*2  
 1-事件：default=all 某件事 or  所有事 
 2-时间：default=yesterday 不同截止日期查询结果不同，可以显示趋势  
 

'''

class DotData:
    '地图上一个点和它的热度' 
    def __init__(self, lng, lat, count):
        self.lng = lng
        self.lat = lat
        self.count = count
    def obj(self):
        if self.count<0 :
            self.count = 0
        if self.count>100 : 
            self.count = 100
        return {"lng":self.lng,"lat":self.lat,"count":self.count}
    



def dataGenerator(): 
    # naive version
    heatmapData = []
    lng = 80 # 50/20 2.5
    lat = 5 # 45/20 2.25
    count = 0 # 100/20 5
    for i in range(20) : # from DotData(80,5,0).obj()
        heatmapData.append(DotData(lng+i*2.5,lat+i*2.25,count+i*5).obj())
    return heatmapData
    