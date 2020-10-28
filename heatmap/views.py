#!/usr/bin/python
# -*- coding: UTF-8 -*-

##  log  setting中增加了ALLOWED_HOSTS   目前停用跨域保护 csrf_exempt 

'''
http://0.0.0.0:8080/heatmap/heatmap
不管request长啥样
heatmapData:[{lng: 116.191031, lat: 39.988585, count: 98} , ......] 双引号的json格式, in中国[不提供审查] count[0,100]
'''
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .dataGenerator import data_generator

from django.views.decorators.csrf import csrf_exempt
    
#在处理函数加此装饰器即可
@csrf_exempt
def heatmap(request, cluster_id, starttime, endtime):
    # todo 参数审查 格式规整
    cluster_id = 1
    starttime = "2020-10-13"
    endtime = "2020-10-20"
    heatmapData = data_generator(cluster_id, starttime, endtime)
    rspCode =200 # responseCode
    return JsonResponse({
        'code':rspCode,
        'data':heatmapData 
        }, status=rspCode)