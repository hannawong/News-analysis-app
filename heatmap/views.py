#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .dataGenerator import data_generator,timestamp2date


def heatmap(request, cluster_id, starttime, endtime):
    global d_begin,d_end

    def gen_response(code: int, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        if not cluster_id.isdigit():
            return gen_response(400, '{} is not a number'.format(cluster_id))
        cluster_id2 = int(cluster_id)
        if cluster_id2 >= 20 or cluster_id2 < 0:
            return gen_response(400, '{} range error'.format(cluster_id))
        try:
            starttime2 = float(starttime)
            endtime2 = float(endtime)
            if starttime2 > endtime2:
                return gen_response(400, 'starttime > endtime')
            if starttime2 < 1602521017: # starttime = "2020-10-13"  1602521017
                starttime2 = 1602521017
            if endtime2 > 1603986217:  # endtime = "2020-10-29" 1603986217
                endtime2 = 1603986217
            # convert to   d_beign = datetime.datetime.strptime("2020-10-13", '%Y-%m-%d')
            d_begin = timestamp2date(starttime2)
            d_end = timestamp2date(endtime2)
        except Exception as e:
            print(e)
            return gen_response(400, str(e))
        print(starttime, endtime,starttime2, endtime2)
        print(cluster_id2, d_begin,d_end)
        heatmapData = data_generator(cluster_id2, d_begin,d_end)
        return JsonResponse({
            'code': 200,
            'data': heatmapData
        }, status=200)
