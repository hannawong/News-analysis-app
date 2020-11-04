#!/usr/bin/python
# -*- coding: UTF-8 -*-

##  log  setting中增加了ALLOWED_HOSTS   目前停用跨域保护 csrf_exempt 


import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .dataGenerator import data_generator

from django.views.decorators.csrf import csrf_exempt


# 在处理函数加此装饰器即可
@csrf_exempt
def heatmap(request, cluster_id, starttime, endtime):
    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    rspCode = 200  # responseCode
    if request.method == 'GET':
        if not cluster_id.isdigit():
            return gen_response(400, '{} is not a number'.format(cluster_id))
        if cluster_id >= 20 or cluster_id < 0:
            return gen_response(400, '{} range error'.format(cluster_id))
        # todo 参数审查 格式规整
        # cluster_id = 1
        # starttime = "2020-10-13"
        # endtime = "2020-10-13"
        print(cluster_id, starttime, endtime)
        heatmapData = data_generator(cluster_id, starttime, endtime)
        return JsonResponse({
            'code': rspCode,
            'data': heatmapData
        }, status=rspCode)
