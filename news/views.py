from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import re
import jieba
from .models import Articles,WeiboHot
from django.core.exceptions import ValidationError
from news.inverted_index.search import wordcloud, search
from elasticsearch import Elasticsearch
from heatmap.dataGenerator import data_generator_ids

import sys
import os

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

def gen_response(code: int, data):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)

def message(request):
    if request.method == 'GET':
        limit = request.GET.get('limit', default='100')
        offset = request.GET.get('offset', default='0')
        if not limit.isdigit():
            return gen_response(400, '{} is not a number'.format(limit))
        if not offset.isdigit():
            return gen_response(400, '{} is not a number'.format(offset))
        response= gen_response(200, [
                {
                    'id':msg.id,
                    'title':msg.title.split("@")[0],
                    'hot':msg.hot,
                    'url':msg.title.split("@")[1]
                }
                for msg in WeiboHot.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ])
        return response

def GetWordcloud(request,cluster_id,topk):  ###词云API
    if request.method == 'GET':
        dic=wordcloud(cluster_id,topk)
        return gen_response(200,dic)


def GetTimeline(request, keyword, starttime, endtime):
    if request.method == 'GET':
        news_list=search(keyword, starttime, endtime)
        return gen_response(200,news_list)

def searchNewsWithElasticsearch(q, time_from, time_to, from_index=0, size=10):
    q_body = {
        "query":{
            "bool":{
                "must":[{
                    "match":{
                        "text":q
                    }}],
                "must_not":[],
                "should":[]
            }
        },
        "from":from_index,
        "size":size,
        "sort":[],
        "aggs":{}
    }

    if time_from and time_to:
        q_range = {
                "range": {
                    "time": {
                        "gt": time_from,
                        "lte": time_to
                        }
                    }
                }
        q_body["query"]["bool"]["must"].append(q_range)
    elif time_from:
        q_range = {
                "range": {
                    "time": {
                        "gt": time_from,
                        }
                    }
                }
        q_body["query"]["bool"]["must"].append(q_range)
    elif time_to:
        q_range = {
                "range": {
                    "time": {
                        "lte": time_to
                        }
                    }
                }
        q_body["query"]["bool"]["must"].append(q_range)

    es = Elasticsearch()

    response = es.search(
        index="xxswl",
        body=q_body
    )

    return response

def searchNewsWithHeatmap(request):

    if request.method == 'GET':
        q = request.GET.get('q', default='a')
        time_from = request.GET.get('from')
        time_to = request.GET.get('to')

    response = searchNewsWithElasticsearch(q, time_from, time_to, 0, 10000)

    hits_id = []
    for item in response['hits']['hits']:
        hits_id.append(int(item['_source']['django_id']))

    print(hits_id)

    res = {"search_res": response['hits']['hits'], "heatmap": data_generator_ids(hits_id)}
    return gen_response(200, res)

def searchNews(request):
    if request.method == 'GET':
        q = request.GET.get('q', default='a')
        time_from = request.GET.get('from')
        time_to = request.GET.get('to')
        start_index = int(request.GET.get('start_index', default='0'))

    response = searchNewsWithElasticsearch(q, time_from, time_to, start_index, 10)

    res = gen_response(200, response['hits'])
    return res