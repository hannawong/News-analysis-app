from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import re
import jieba
from .models import Articles,WeiboHot,WeiboSocialEvents
from django.core.exceptions import ValidationError
from news.inverted_index.search import wordcloud, search, Event
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as elasticsearch_excaptions
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
        response= gen_response(200, [
            {
                'id':msg.id,
                'title':msg.title.split("@")[0],
                'hot':msg.hot,
                'url':msg.title.split("@")[1]
            }
            for msg in WeiboHot.objects.all()
        ])
        return response

def message1(request):
    if request.method == 'GET':
        response= gen_response(200, [
            {
                'id':msg.id,
                'title':msg.title.split("@")[0],
                'url':msg.title.split("@")[1]
            }
            for msg in WeiboSocialEvents.objects.all()
        ])
        return response

def message2(request):
    length=len(Articles.objects.all())
    if request.method == 'GET':
        response= gen_response(200, [
            {
                'title':msg.title,
                'url':msg.url,
                'time':msg.time
            }
            for msg in Articles.objects.all().order_by('time')[length-50:]
        ])
        return response

def GetWordcloud(request,cluster_id,topk):  # 词云API
    if request.method == 'GET':
        dic=wordcloud(cluster_id,topk)
        return gen_response(200,dic)

def GetTimeline(request, keyword, starttime, endtime):
    if request.method == 'GET':
        news_list=search(keyword, starttime, endtime)
        return gen_response(200,news_list)

def GetEventTimeline(request,id):
    if request.method == 'GET':
        news_list=Event(id)
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

    try:
        response = searchNewsWithElasticsearch(q, time_from, time_to, 0, 10000)
    except Exception as e:
        if isinstance(e, elasticsearch_excaptions.ConnectionError):
            res = gen_response(400, {'error': "No Elasticsearch"})
        else:
            print(type(e))
            res = gen_response(400, {'error': str(e)})
        return res

    hits_id = []
    for item in response['hits']['hits']:
        hits_id.append(int(item['_source']['django_id']))

    res = {"heatmap": data_generator_ids(hits_id)}
    return gen_response(200, res)

def searchNews(request):
    if request.method == 'GET':
        q = request.GET.get('q', default='a')
        time_from = request.GET.get('from')
        time_to = request.GET.get('to')
        start_index = int(request.GET.get('start_index', default='0'))

    try:
        response = searchNewsWithElasticsearch(q, time_from, time_to, start_index, 10)
    except Exception as e:
        if isinstance(e, elasticsearch_excaptions.ConnectionError):
            res = gen_response(400, {'error': "No Elasticsearch"})
        else:
            print(type(e))
            res = gen_response(400, {'error': str(e)})
    else:
        res = gen_response(200, response['hits'])
    finally:
        pass
    return res


def search_date_cluster_info(request):
    if request.method == 'GET':
        q = request.GET.get('q', default='a')

    try:
        response = searchNewsWithElasticsearch(q, None, None, 0, 10000)
    except Exception as e:
        if isinstance(e, elasticsearch_excaptions.ConnectionError):
            res = gen_response(400, {'error': "No Elasticsearch"})
        else:
            print(type(e))
            res = gen_response(400, {'error': str(e)})
        return res

    date_num_cluster_keyword = {}

    for item in response['hits']['hits']:
        time_str = item['_source']['time'].split('T')[0]
        cluster_id = item['_source']['cluster_id']
        item_keyword = item['_source']['keywords'].split('@@@')[0]
        keywords_list = item_keyword.split(',')
        if time_str in date_num_cluster_keyword.keys():
            date_num_cluster_keyword[time_str]['num'] += 1
            if cluster_id in date_num_cluster_keyword[time_str]['cluster_ids'].keys():
                date_num_cluster_keyword[time_str]['cluster_ids'][cluster_id]['id_num'] += 1
                for words in keywords_list:
                    if words in date_num_cluster_keyword[time_str]['cluster_ids'][cluster_id]['keywords'].keys():
                        date_num_cluster_keyword[time_str]['cluster_ids'][cluster_id]['keywords'][words] += 1
                    else:
                        date_num_cluster_keyword[time_str]['cluster_ids'][cluster_id]['keywords'][words] = 1
            else:
                new_id = {
                    'id_num': 1,
                    'keywords':{}
                }
                for words in keywords_list:
                    if words in new_id['keywords'].keys():
                        new_id['keywords'][words] += 1
                    else:
                        new_id['keywords'][words] = 1
                date_num_cluster_keyword[time_str]['cluster_ids'][cluster_id] = new_id
        else:
            date_info = {
                'num': 1,
                'cluster_ids': {
                    cluster_id:{
                        'id_num': 1,
                        'keywords':{}
                    }
                }
            }
            for words in keywords_list:
                if words in date_info['cluster_ids'][cluster_id]['keywords'].keys():
                    date_info['cluster_ids'][cluster_id]['keywords'][words] += 1
                else:
                    date_info['cluster_ids'][cluster_id]['keywords'][words] = 1
            date_num_cluster_keyword[time_str] = date_info

    # 对关键词排序
    for date_item in date_num_cluster_keyword:
        for cluster_id_item in date_num_cluster_keyword[date_item]['cluster_ids']:

            words_list = date_num_cluster_keyword[date_item]['cluster_ids'][cluster_id_item]['keywords']

            sort_keywords = []
            temp = sorted(words_list.items(), key=lambda x: x[1], reverse=True)
            for item in temp:
                sort_keywords.append(item[0])

            date_num_cluster_keyword[date_item]['cluster_ids'][cluster_id_item]['keywords'] = sort_keywords

    return gen_response(200, date_num_cluster_keyword)
